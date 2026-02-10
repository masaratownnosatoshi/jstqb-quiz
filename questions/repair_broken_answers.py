import json
import os
import glob
import difflib

# カレントディレクトリを対象
TARGET_DIR = "."

def find_closest_option(target_answer, options):
    """
    正解テキスト(target_answer)に最も似ている選択肢を探す関数
    """
    if not options:
        return None
        
    # 1. 完全一致チェック（念のため）
    if target_answer in options:
        return target_answer
        
    # 2. 類似度判定 (difflibを使用)
    # cutoff=0.4 は「40%以上似ていれば候補とする」という意味。
    # 括弧の有無程度なら0.8以上になるので、確実にヒットします。
    matches = difflib.get_close_matches(target_answer, options, n=1, cutoff=0.4)
    
    if matches:
        return matches[0]
        
    # 3. 部分一致チェック (正解が選択肢の一部、あるいはその逆)
    for opt in options:
        if target_answer in opt or opt in target_answer:
            return opt
            
    return None

def repair_broken_answers():
    print("=== 正解データ修復処理（再リンク）を開始 ===")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    fixed_files_count = 0
    total_repaired = 0
    
    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        file_modified = False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    # 正解データが存在し、かつ選択肢が存在する場合
                    if "answer" in q and q["answer"] and "options" in q:
                        current_ans = q["answer"][0]
                        options = q["options"]
                        
                        # 正解が選択肢に含まれていない場合（＝ログに出ていたエラー状態）
                        if current_ans not in options:
                            
                            # 最も似ている選択肢を探す
                            best_match = find_closest_option(current_ans, options)
                            
                            if best_match:
                                # 修正実行
                                q["answer"] = [best_match]
                                file_modified = True
                                total_repaired += 1
                                print(f"  [修復] {filename}")
                                print(f"    旧: {current_ans[:30]}...")
                                print(f"    新: {best_match[:30]}...")
                            else:
                                print(f"  [警告] 自動修復不能: {filename} - {current_ans[:20]}...")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                # print(f"  => 保存しました: {filename}")
                fixed_files_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("=" * 40)
    print(f"完了: {fixed_files_count} ファイル、合計 {total_repaired} 箇所のリンク切れを修復しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    repair_broken_answers()
    input()
import json
import os
import glob
import difflib

# 処理対象のディレクトリ（カレントディレクトリ）
TARGET_DIR = "."

def remove_explanation(text):
    """
    文字列の末尾にある（）または()で囲まれた部分を削除する関数
    """
    original_text = text
    text = text.rstrip() # 末尾の空白削除
    
    # 全角カッコの処理
    if text.endswith('）'):
        start_index = text.rfind('（')
        if start_index != -1:
            return text[:start_index].rstrip()

    # 半角カッコの処理
    if text.endswith(')'):
        start_index = text.rfind('(')
        if start_index != -1:
            return text[:start_index].rstrip()
            
    return original_text

def find_best_match(target, options):
    """
    選択肢の中から、targetに最も似ている文字列を探す
    """
    if not options:
        return None
    
    # 1. 完全一致
    if target in options:
        return target
        
    # 2. 前方一致 (緩め: 最初の10文字)
    for opt in options:
        if len(target) > 5 and opt.startswith(target[:10]):
            return opt

    # 3. 類似度判定 (difflib) - 表記揺れや微妙なカットミス対策
    # 最も類似度が高いものを取得
    matches = difflib.get_close_matches(target, options, n=1, cutoff=0.6)
    if matches:
        return matches[0]
        
    return None

def force_clean_final():
    print("=== 最終版クリーニング＆同期処理を開始 ===")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    fixed_files_count = 0
    
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
                    # 1. 選択肢(options)の修正
                    if "options" in q:
                        new_options = []
                        for opt in q["options"]:
                            cleaned = remove_explanation(opt)
                            if cleaned != opt:
                                # ログは出さずにフラグだけ立てる（量が多いので）
                                file_modified = True
                            new_options.append(cleaned)
                        q["options"] = new_options

                    # 2. 正解(answer)の修正と同期
                    if "answer" in q and len(q["answer"]) > 0:
                        original_ans = q["answer"][0]
                        cleaned_ans = remove_explanation(original_ans)
                        
                        # クリーニングした正解に最も近い選択肢を探す
                        best_match = find_best_match(cleaned_ans, q["options"])
                        
                        if best_match:
                            # 見つかった場合、正解データをその選択肢で上書きする
                            if original_ans != best_match:
                                q["answer"] = [best_match]
                                file_modified = True
                                print(f"  [修正・同期] {filename} (ID:{q.get('id')})")
                        else:
                            # どうしても見つからない場合でも、クリーニング結果で上書き保存する
                            # (選択肢側もクリーニングされているはずなので、次回一致する可能性が高い)
                            if original_ans != cleaned_ans:
                                q["answer"] = [cleaned_ans]
                                file_modified = True
                                print(f"  [強制置換] {filename} (ID:{q.get('id')}) - 選択肢不一致のため強制クリーニング")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                # print(f"  => 保存: {filename}")
                fixed_files_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("=" * 40)
    print(f"処理終了: 合計 {fixed_files_count} ファイルを修正・更新しました。")

if __name__ == "__main__":
    force_clean_final()
    print("\nエンターキーを押して終了してください...")
    input()
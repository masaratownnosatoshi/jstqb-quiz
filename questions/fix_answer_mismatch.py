import json
import os
import glob

# カレントディレクトリの全jsonファイルを対象
TARGET_DIR = "."

def fix_answer_mismatch():
    print("--- 正解データの同期修正（アンマッチ解消）を開始 ---")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    
    fixed_files = 0
    fixed_count = 0

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            
            if isinstance(data, list):
                for q in data:
                    # 正解データがあり、かつ選択肢がある場合
                    if "answer" in q and "options" in q and len(q["answer"]) > 0:
                        current_answer = q["answer"][0]
                        
                        # 現状の正解文言が、選択肢リストの中に存在するかチェック
                        if current_answer not in q["options"]:
                            # 存在しない場合（不一致）、似ている選択肢を探して同期する
                            # ここでは「先頭の10文字」が一致する選択肢を正解とみなして上書きする
                            # （括弧削除などで末尾が変わっているだけの可能性が高いため）
                            
                            match_found = False
                            for opt in q["options"]:
                                # 前方一致（15文字程度）で判定
                                if opt.startswith(current_answer[:15]):
                                    q["answer"] = [opt]
                                    print(f"修正 ({q['id']}): 正解データを同期しました")
                                    match_found = True
                                    modified = True
                                    fixed_count += 1
                                    break
                            
                            if not match_found:
                                # 前方一致も見つからない場合はログだけ出す（手動確認用）
                                print(f"警告 ({q['id']}): 正解に対応する選択肢が見つかりません。")

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"ファイル保存: {filename}")
                fixed_files += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"完了: {fixed_files} ファイル、計 {fixed_count} 箇所の不整合を修正しました。")

if __name__ == "__main__":
    fix_answer_mismatch()
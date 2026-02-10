import json
import os
import re
import glob

# カレントディレクトリの全jsonファイルを対象
TARGET_DIR = "."

# 削除パターンの強化
# 末尾にある ( ) や （ ） を検出して削除する（中身は何でもよい）
# 行末の空白も見込んで削除
REMOVE_PATTERN = re.compile(r'[（\(].+?[）\)]\s*$')

def final_fix_v2():
    print("--- 最終完全修正処理を開始します ---")
    
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
                    # 1. 選択肢(options)のクリーニング
                    if "options" in q:
                        new_options = []
                        for opt in q["options"]:
                            # 正規表現で末尾の（）を削除
                            cleaned_opt = REMOVE_PATTERN.sub('', opt).rstrip()
                            if cleaned_opt != opt:
                                file_modified = True
                            new_options.append(cleaned_opt)
                        q["options"] = new_options

                    # 2. 正解(answer)のクリーニング
                    if "answer" in q and len(q["answer"]) > 0:
                        original_ans = q["answer"][0]
                        cleaned_ans = REMOVE_PATTERN.sub('', original_ans).rstrip()
                        
                        if cleaned_ans != original_ans:
                            q["answer"] = [cleaned_ans]
                            file_modified = True
                        
                        # 3. 正解が選択肢にあるか確認（アンマッチ修正）
                        if cleaned_ans not in q["options"]:
                            # 完全一致がない場合、前方一致で探す
                            found = False
                            for opt in q["options"]:
                                # 最初の20文字が一致すれば同一とみなす
                                if opt.startswith(cleaned_ans[:20]):
                                    q["answer"] = [opt]
                                    file_modified = True
                                    found = True
                                    break
                            
                            if not found:
                                print(f"警告: {filename} - ID:{q.get('id')} の正解が選択肢に見つかりません。")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"修正完了: {filename}")
                fixed_files_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"処理終了: 合計 {fixed_files_count} ファイルを修正・同期しました。")

if __name__ == "__main__":
    final_fix_v2()
import json
import os
import re
import glob

# カレントディレクトリの全jsonファイルを対象
TARGET_DIR = "."

# 正規表現の解説:
# [（\(]      : 全角または半角の開きカッコで始まる
# [^）\)]+    : 閉じカッコ以外の文字が1文字以上続く（中身）
# [）\)]      : 全角または半角の閉じカッコで終わる
# \s* : その後ろに空白（改行含む）があってもよい
# $           : 文字列の末尾であること
CLEAN_PATTERN = re.compile(r'[（\(][^）\)]+[）\)]\s*$')

def cleanup_all_files():
    print("--- 全ファイル一括クリーニング開始 ---")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    fixed_files = 0
    fixed_items = 0

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
                            # 正規表現で削除
                            cleaned_opt = CLEAN_PATTERN.sub('', opt).rstrip()
                            
                            if cleaned_opt != opt:
                                file_modified = True
                                fixed_items += 1
                                # 修正ログを表示（確認用）
                                print(f"修正[ID:{q.get('id')}]: {opt[-15:]} -> {cleaned_opt[-15:]}")
                                
                            new_options.append(cleaned_opt)
                        q["options"] = new_options

                    # 2. 正解(answer)のクリーニング & 同期
                    if "answer" in q and len(q["answer"]) > 0:
                        original_ans = q["answer"][0]
                        cleaned_ans = CLEAN_PATTERN.sub('', original_ans).rstrip()
                        
                        if cleaned_ans != original_ans:
                            q["answer"] = [cleaned_ans]
                            file_modified = True
                        
                        # 正解が選択肢にあるか確認（アンマッチ修正）
                        if cleaned_ans not in q["options"]:
                            # 完全一致がない場合、前方一致で探す
                            for opt in q["options"]:
                                if opt.startswith(cleaned_ans[:20]):
                                    q["answer"] = [opt]
                                    file_modified = True
                                    break

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"ファイル保存: {filename}")
                fixed_files += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"完了: {fixed_files} ファイル、合計 {fixed_items} 箇所の不要な括弧記述を削除しました。")

if __name__ == "__main__":
    cleanup_all_files()
import json
import os
import glob

# 処理対象のディレクトリ（カレントディレクトリ）
TARGET_DIR = "."

def remove_explanation(text):
    """
    文字列の末尾にある（）または()で囲まれた部分を削除する関数
    正規表現を使わず、文字の位置検索で処理します。
    """
    original_text = text
    text = text.rstrip() # 末尾の空白削除
    
    # 全角カッコの処理
    if text.endswith('）'):
        # 後ろから検索して最初の '（' を探す
        start_index = text.rfind('（')
        if start_index != -1:
            return text[:start_index].rstrip()

    # 半角カッコの処理
    if text.endswith(')'):
        start_index = text.rfind('(')
        if start_index != -1:
            return text[:start_index].rstrip()
            
    return original_text

def force_clean_v4():
    print("=== 強力クリーニング処理（文字コード検索版）を開始 ===")
    
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
                                print(f"  [削除検知] {filename} (ID:{q.get('id')})")
                                print(f"    前: {opt}")
                                print(f"    後: {cleaned}")
                                file_modified = True
                            
                            new_options.append(cleaned)
                        q["options"] = new_options

                    # 2. 正解(answer)の修正と同期
                    if "answer" in q and len(q["answer"]) > 0:
                        original_ans = q["answer"][0]
                        cleaned_ans = remove_explanation(original_ans)
                        
                        # 正解データが選択肢の中に存在するか確認
                        if cleaned_ans not in q["options"]:
                            found = False
                            for opt in q["options"]:
                                if len(cleaned_ans) > 5 and opt.startswith(cleaned_ans[:10]):
                                    q["answer"] = [opt]
                                    file_modified = True
                                    found = True
                                    break
                            if not found:
                                print(f"  [警告] 正解データが選択肢に見つかりません: {cleaned_ans}")
                        else:
                            if cleaned_ans != original_ans:
                                q["answer"] = [cleaned_ans]
                                file_modified = True

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  => ファイルを更新しました: {filename}")
                fixed_files_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("=" * 40)
    print(f"処理終了: {fixed_files_count} ファイルを修正しました。")

if __name__ == "__main__":
    force_clean_v4()
    # ▼▼▼ 追加部分: 入力があるまでウィンドウを閉じないようにする ▼▼▼
    print("\n確認が終わったらエンターキーを押して終了してください...")
    input()
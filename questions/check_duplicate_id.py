import json
import os
import glob

def check_duplicate_id():
    target_id = "Q2-MED-V18-01"
    print(f"--- ID: {target_id} の重複チェックを開始 ---")
    
    json_files = glob.glob(os.path.join(".", "*.json"))
    found_files = []

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    if q.get("id") == target_id:
                        filename = os.path.basename(file_path)
                        options = q.get("options", [])
                        print(f"\n★ 発見！ ファイル名: {filename}")
                        print(f"   - 選択肢の状態: {options}")
                        
                        if not options or options == [""]:
                            print("   - ⚠️ 状態: 空（修正されていません！）")
                        else:
                            print("   - ✅ 状態: 修正済み")
                            
                        found_files.append(filename)

        except Exception as e:
            continue

    print("-" * 30)
    if len(found_files) == 0:
        print("❌ このIDを持つ問題はどこにも見つかりませんでした。")
    elif len(found_files) == 1:
        print(f"✅ 重複はありません。{found_files[0]} だけに存在します。")
        print("   -> 原因は「ブラウザのキャッシュ」で確定です。")
    else:
        print(f"⚠️ 重複しています！ {len(found_files)} 個のファイルに存在します。")
        print(f"   ファイル一覧: {found_files}")
        print("   -> アプリが「修正されていない方のファイル」を読み込んでいるのが原因です。")

    print("\nエンターキーを押して終了してください...")

if __name__ == "__main__":
    check_duplicate_id()
    input()
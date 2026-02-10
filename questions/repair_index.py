import json
import os
import glob

# 設定
OUTPUT_DIR = "."
INDEX_FILE = "index.json"
# 除外するファイル
EXCLUDE_FILES = [INDEX_FILE, "package.json", "manifest.json", "tsconfig.json", "vercel.json"]

def repair_index():
    print("=== index.json の修復と再生成を開始します ===")
    
    all_questions = []
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
    
    success_count = 0
    error_count = 0
    
    if not json_files:
        print("❌ エラー: .json ファイルが1つも見つかりません！")
        print("   このスクリプトを、ch1_...json などがあるフォルダと同じ場所に置いてください。")
        return

    print(f"📂 検出されたJSONファイル数: {len(json_files)}")

    for file_path in json_files:
        filename = os.path.basename(file_path)
        
        # 除外ファイルはスキップ
        if filename in EXCLUDE_FILES:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                count = len(data)
                if count > 0:
                    all_questions.extend(data)
                    success_count += 1
                    print(f"  ✅ 読込成功: {filename} ({count}問)")
                else:
                    print(f"  ⚠️ 警告（0問）: {filename} は空です。スキップします。")
            else:
                print(f"  ⚠️ 警告（形式不正）: {filename} はリスト形式ではありません。")

        except json.JSONDecodeError as e:
            print(f"  ❌ JSON読込エラー: {filename}")
            print(f"     -> 原因: カンマ漏れやカッコ不足の可能性があります ({e})")
            error_count += 1
        except Exception as e:
            print(f"  ❌ 読込エラー: {filename} ({e})")
            error_count += 1

    # 結果の保存
    if len(all_questions) > 0:
        try:
            with open(os.path.join(OUTPUT_DIR, INDEX_FILE), 'w', encoding='utf-8') as f:
                json.dump(all_questions, f, ensure_ascii=False, indent=2)
            
            print("-" * 30)
            print(f"🎉 修復完了！")
            print(f"■ 成功ファイル: {success_count}")
            print(f"■ エラーファイル: {error_count}")
            print(f"■ 合計問題数: {len(all_questions)} 問")
            print(f"■ 保存先: {os.path.abspath(INDEX_FILE)}")
            print("-" * 30)
            print("👉 これでブラウザをリロード（F5）してください。")
            
        except Exception as e:
            print(f"❌ 書き込みエラー: index.json を保存できませんでした ({e})")
    else:
        print("-" * 30)
        print("❌ 失敗: 有効な問題が1つも見つかりませんでした。")
        print("   フォルダの場所を確認するか、JSONファイルの中身を確認してください。")

if __name__ == "__main__":
    repair_index()
    input("\nエンターキーを押して終了...")
import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード（表記ゆれに対応するため、数値部分で検索）
SEARCH_KEYS = ["43,200", "43200", "エラーバジェット"]

def fix_error_budget():
    print("--- エラーバジェット計算問題の修正を開始 ---")
    
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
    found = False

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_modified = False
            
            if isinstance(data, list):
                for q in data:
                    q_text = q.get("question", "")
                    
                    # 問題文に「43,200」かつ「エラーバジェット」が含まれているか確認
                    if ("43,200" in q_text or "43200" in q_text) and "エラーバジェット" in q_text:
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # 正しい選択肢と正解に書き換え
                        q["options"] = [
                            "13.2分",  # 正解
                            "43.2分",  # 引っかけ：総バジェット
                            "30分",    # 引っかけ：消費済み
                            "0分"      # 引っかけ：バジェット枯渇
                        ]
                        q["answer"] = [
                            "13.2分"
                        ]
                        # 解説の微調整（念のため）
                        q["explanation"] = "【解説】\n総エラーバジェット = 43,200分 × 0.1% = 43.2分。\n残りのバジェット = 43.2分 - 30分 = 13.2分 となります。"
                        
                        file_modified = True
                        found = True
                        print("  => 選択肢と正解を「13.2分」に修正しました。")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                break # 見つかったらループ終了

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    if not found:
        print("警告: 該当する問題が見つかりませんでした。")
        print("検索条件: '43,200' または '43200' かつ 'エラーバジェット'")

    print("-" * 30)
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_error_budget()
    input()
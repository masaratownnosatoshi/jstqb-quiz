import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード
SEARCH_KEYWORDS = ["テスト自動化のROI", "50万円", "200万円"]

# 正しい選択肢（回数）
NEW_OPTIONS = [
    "4回目",
    "5回目", # 損益分岐点（コストが並ぶ）
    "6回目", # 正解（コストメリットが出る）
    "10回目"
]

# 正解
NEW_ANSWER = [
    "6回目"
]

def fix_roi_calculation():
    print("--- 自動化ROI計算問題の修正を開始 ---")
    
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
                    
                    # キーワード一致確認
                    if all(k in q_text for k in SEARCH_KEYWORDS):
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # 選択肢と正解を修正
                        q["options"] = NEW_OPTIONS
                        q["answer"] = NEW_ANSWER
                        
                        # 解説をわかりやすく更新
                        q["explanation"] = "【解説】\n損益分岐点をx回とすると、手動コスト ＞ 自動化コスト となる条件を求めます。\n50x ＞ 200 + 10x\n40x ＞ 200\nx ＞ 5\n\nしたがって、5回目でコストが同等になり、6回目から自動化のメリットが出ます。"
                        
                        file_modified = True
                        found = True
                        print("  => 選択肢を「回数」に修正し、正解を「6回目」に設定しました。")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                break # 見つかったら終了

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    if not found:
        print("警告: 該当する問題が見つかりませんでした。")

    print("-" * 30)
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_roi_calculation()
    input()
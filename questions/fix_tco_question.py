import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード
SEARCH_KEYWORDS = ["テストツールのTCO", "5年間", "ツールA"]

# 正しい選択肢
NEW_OPTIONS = [
    "ツールBの方が安い",
    "ツールAの方が安い", # 正解
    "両方同じ",
    "計算不能"
]

# 正解
NEW_ANSWER = [
    "ツールAの方が安い"
]

def fix_tco_question():
    print("--- TCO計算問題の修正を開始 ---")
    
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
                        
                        # 解説の微調整（見やすく）
                        q["explanation"] = "【解説】\n・ツールA（商用）：300万 + (50万 × 5年) = 550万円\n・ツールB（OSS）：0円 + (120万 × 5年) = 600万円\n\nしたがって、550万円 < 600万円 で「ツールA」の方が安くなります。\n「無料のOSS」でも、人的サポートコスト（人件費）を計算に入れると商用より高くなるケースがあります。"
                        
                        file_modified = True
                        found = True
                        print("  => 正解を「ツールAの方が安い」に設定しました。")

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
    fix_tco_question()
    input()
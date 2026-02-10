import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード
SEARCH_KEYWORDS = ["レビュー効率の分析", "延べ 50時間", "欠陥発見効率"]

# 新しい選択肢（正解の 2.0 を含める）
NEW_OPTIONS = [
    "2.0 件/時間",    # 正解 (100件 ÷ 50時間)
    "0.5 時間/件",    # 引っかけ (50時間 ÷ 100件：1件見つけるのにかかる時間)
    "4.0 ページ/時間", # 引っかけ (レビュー速度：200ページ ÷ 50時間)
    "50 件/時間"      # 引っかけ (ただの数字)
]

# 正しい正解
NEW_ANSWER = [
    "2.0 件/時間"
]

def fix_review_efficiency():
    print("--- レビュー効率問題の修正を開始 ---")
    
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
                        
                        # 解説の微調整
                        q["explanation"] = "【解説】\n欠陥発見効率 = 発見した欠陥数 ÷ レビュー時間\n$$100 \\text{件} \\div 50 \\text{時間} = 2.0 \\text{件/時間}$$\n\n1時間あたり2個のバグを見つけており、非常に効率が良い（あるいは対象の品質が極端に悪い）ことが分かります。"
                        
                        file_modified = True
                        found = True
                        print("  => 選択肢に「2.0 件/時間」を追加し、正解に設定しました。")

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
    fix_review_efficiency()
    input()
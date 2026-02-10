import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード
SEARCH_KEYWORDS = ["ファンクションポイント法", "100 FP", "チームの生産性"]

# 正しい選択肢（単位を「人」に修正）
NEW_OPTIONS = [
    "2人",
    "3人", # 正解（2.5人の切り上げ）
    "5人",
    "10人"
]

# 正しい正解
NEW_ANSWER = [
    "3人"
]

def fix_fp_estimation():
    print("--- FP見積もり問題の修正を開始 ---")
    
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
                        q["explanation"] = "【解説】\n総工数 = 100 FP × 0.5 人日/FP = 50 人日。\n必要人数 = 50人日 ÷ 20日 = 2.5人。\n\n2.5人では足りないため、期間内に完了させるには切り上げて「3人」必要です。"
                        
                        file_modified = True
                        found = True
                        print("  => 選択肢を「人数」に修正し、正解を「3人」に設定しました。")

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
    fix_fp_estimation()
    input()
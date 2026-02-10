import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."

# 検索キー
SEARCH_KEY = "【計算】3点見積もりの標準偏差（SD）"

# 新しい正しいデータ
NEW_OPTIONS = [
    "2日",   # 正解 (SD)
    "4日",   # 分散 (2の2乗)
    "6日",   # 加重平均値 ((2 + 4*5 + 14) / 6)
    "12日"   # 単純な範囲 (14 - 2)
]
NEW_ANSWER = ["2日"]
NEW_EXPLANATION = "【解説】\n3点見積もりの標準偏差（Standard Deviation）の公式は、「(悲観値 - 楽観値) ÷ 6」です。\n今回のケースでは、(14 - 2) ÷ 6 = 2日 となります。\nちなみに「6日」は加重平均値（期待値）、「4日」は分散となります。"

def fix_pert_sd_question():
    print("--- 3点見積もり（標準偏差）問題の修正を開始 ---")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    fixed_count = 0

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
                    q_text = q.get("question", "")
                    
                    # 該当の問題を発見
                    if SEARCH_KEY in q_text:
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # データを修正
                        q["options"] = NEW_OPTIONS
                        q["answer"] = NEW_ANSWER
                        q["explanation"] = NEW_EXPLANATION
                        
                        file_modified = True
                        print("  => 選択肢と正解を修正しました。")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                fixed_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"完了: {fixed_count} ファイルを修正しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_pert_sd_question()
    input()
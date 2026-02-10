import json
import os
import glob

OUTPUT_DIR = "."

# 検索条件
SEARCH_KEYWORDS = ["欠陥密度の算出", "50 KLOC"]

# 正しい選択肢（解説の計算 200/50=4.0 に合わせる）
NEW_OPTIONS = [
    "4.0 件/KLOC",    # 正解
    "0.25 件/KLOC",   # 引っかけ（逆数：50÷200）
    "40 件/KLOC",     # 引っかけ（桁ミス）
    "250 件/KLOC"     # 引っかけ（足し算）
]

# 正しい正解
NEW_ANSWER = [
    "4.0 件/KLOC"
]

def fix_defect_density():
    print("--- 欠陥密度計算問題の修正を開始 ---")
    
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
                    
                    # 問題文の一致確認
                    if all(k in q_text for k in SEARCH_KEYWORDS):
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # 選択肢と正解を修正
                        q["options"] = NEW_OPTIONS
                        q["answer"] = NEW_ANSWER
                        
                        # 解説も念のため微調整
                        q["explanation"] = "【解説】\n欠陥密度 ＝ 欠陥数 ÷ 規模 です。\n今回の場合は 200件 ÷ 50 KLOC ＝ 4.0 件/KLOC となります。\n他モジュールや過去基準と比較して、品質の良し悪しを判断する材料にします。"
                        
                        file_modified = True
                        found = True
                        print("  => 選択肢を修正し、正解を「4.0」に設定しました。")

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
    fix_defect_density()
    input()
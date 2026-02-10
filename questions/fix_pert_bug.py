import json
import os

# 対象ファイル
TARGET_FILE = "ch1_general_vol77.json"
OUTPUT_DIR = "."

def fix_pert_calculation_bug():
    file_path = os.path.join(OUTPUT_DIR, TARGET_FILE)
    
    if not os.path.exists(file_path):
        print(f"エラー: {TARGET_FILE} が見つかりません。")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = False
        
        if isinstance(data, list):
            for q in data:
                # IDが一致する問題を特定
                if q.get("id") == "Q1-GEN-V77-03":
                    print(f"修正対象を発見: {q.get('id')}")
                    
                    # 選択肢をきれいな数値に直す
                    # (2 + 4*5 + 8) / 6 = 30 / 6 = 5日 が正解
                    q["options"] = [
                        "4日",
                        "5日",
                        "6日",
                        "7日"
                    ]
                    
                    # 正解を「5日」に設定
                    q["answer"] = [
                        "5日"
                    ]
                    
                    # 解説の数式と整合性が取れるように微調整（念のため）
                    q["explanation"] = "【解説】\n3点見積もりの期待値(E) = (楽観値 + 4×最頻値 + 悲観値) ÷ 6\nE = (2 + 4×5 + 8) ÷ 6 = 30 ÷ 6 = 5日 となります。"
                    
                    modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"修正完了: {TARGET_FILE} を保存しました。")
        else:
            print("警告: 対象のIDが見つかりませんでした。")

    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    fix_pert_calculation_bug()
    input("\nエンターキーを押して終了してください...")
import json
import os

# 修正対象ファイル
TARGET_FILE = "ch1_finance_vol74.json"
OUTPUT_DIR = "."

def fix_sla_penalty():
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
                if q.get("id") == "Q1-FIN-V74-01":
                    print(f"修正対象を発見: {q.get('id')}")
                    
                    # 選択肢を明確な内容（金額入り）に修正
                    q["options"] = [
                        "発生しない（稼働率99.9%は達成しているため）",
                        "発生する（1億円の返金）",
                        "発生する（10億円の全額返金）",
                        "データ不足のため計算不能"
                    ]
                    
                    # 正解を設定
                    q["answer"] = [
                        "発生する（1億円の返金）"
                    ]
                    
                    # 解説文も少し整理（自己修正コメントを削除して綺麗にする）
                    q["explanation"] = "【解説】\n1ヶ月 = 30日 × 24時間 = 720時間。\n99.9%の稼働率における許容ダウンタイムは、720時間 × 0.1% = 0.72時間（約43分）です。\n今回の実績ダウンタイムは1時間（60分）で許容値を超えているため、SLA違反となりペナルティが発生します。\n返金額 = 月額10億円 × 10% = 1億円 となります。"
                    
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
    fix_sla_penalty()
    input("\nエンターキーを押して終了してください...")
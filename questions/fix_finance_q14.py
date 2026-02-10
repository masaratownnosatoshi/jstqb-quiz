import json
import os
import glob

OUTPUT_DIR = "."

# 修正対象のファイルとID
TARGET_FILE = "ch1_finance_vol14.json"
TARGET_ID = "Q1-FIN-V14-01"

# 新しい正しい問題データ（1円誤差の原因）
NEW_QUESTION_DATA = {
    "question": "【背景】銀行システムで「金額計算が1円合わない」バグが見つかった。\n調査の結果、特定の小数を含む計算（消費税や利息計算など）において、期待値と実行結果に微細な差異が発生していることが判明した。\n\n【課題】このバグの技術的な原因として、最も可能性が高いものはどれか。",
    "options": [
        "金額計算に「浮動小数点数型（float/double）」を使用しており、2進数表現による丸め誤差が発生している",
        "データベースのトランザクション分離レベルが「Read Committed」に設定されており、ファントムリードが発生している",
        "サーバー間の時刻同期（NTP）がずれており、計算処理の実行タイミングにラグが生じている",
        "ネットワークの帯域幅が不足しており、計算データの一部がパケットロスにより欠落している"
    ],
    "answer": [
        "金額計算に「浮動小数点数型（float/double）」を使用しており、2進数表現による丸め誤差が発生している"
    ],
    "explanation": "【解説】\n金融システムにおける「1円の誤差」の典型的な原因は、コンピュータが小数を扱う際の「浮動小数点数の誤差（IEEE 754）」です。\n0.1などの小数を2進数で正確に表現できないため、計算を繰り返すと誤差が蓄積します。\nこれを防ぐため、金融計算では必ず「固定小数点数型（Decimal型）」や整数型を使用する必要があります。",
    "type": "単一選択",
    "style": "文章"
}

def fix_finance_q14():
    print(f"--- {TARGET_FILE} の修正を開始 ---")
    
    file_path = os.path.join(OUTPUT_DIR, TARGET_FILE)
    
    if not os.path.exists(file_path):
        print(f"❌ エラー: ファイルが見つかりません ({file_path})")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        found = False
        if isinstance(data, list):
            for i, q in enumerate(data):
                # IDまたは問題文の一部で特定
                if q.get("id") == TARGET_ID or "金額計算が1円合わない" in q.get("question", ""):
                    print(f"発見: ID {q.get('id')}")
                    
                    # データを上書き更新
                    # IDや章情報は元のまま維持し、中身だけ更新
                    q["question"] = NEW_QUESTION_DATA["question"]
                    q["options"] = NEW_QUESTION_DATA["options"]
                    q["answer"] = NEW_QUESTION_DATA["answer"]
                    q["explanation"] = NEW_QUESTION_DATA["explanation"]
                    
                    found = True
                    print("  => 問題文と選択肢を「浮動小数点数の誤差」に関する内容に修正しました。")
                    break
        
        if found:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 保存完了: {TARGET_FILE}")
        else:
            print("⚠️ 警告: 該当する問題が見つかりませんでした。")

    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    fix_finance_q14()
    input("エンターキーを押して終了...")
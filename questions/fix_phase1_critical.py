import json
import os
import glob

OUTPUT_DIR = "."

# 修正データの定義（ファイル名: 正しい選択肢リスト）
# 計算問題の答えや、重複を解消した選択肢を手動で定義しました
fixes = {
    # 1. SLAペナルティ
    "ch1_finance_vol74.json": [
        "発生しない（稼働率99.9%は達成しているため）",
        "発生する（稼働率が99.9%を下回っているため）",
        "発生する（ダウンタイムが許容時間を超えているため）", # 正解候補
        "データ不足のため計算不能"
    ],
    # 2. バッチ処理
    "ch1_finance_vol76.json": [
        "終わらない（処理能力不足）", # 正解候補
        "終わる（余裕を持って完了する）",
        "終わる（ギリギリ完了する）",
        "データ不足のため判断を保留する"
    ],
    # 3. EVM計算
    "ch1_general_vol46.json": [
        "CV = -$1,000 （コスト超過）", # 正解候補
        "CV = -$2,000 （大幅なコスト超過）",
        "CV = +$1,000 （コスト節約）",
        "CV = 0 （予算通り）"
    ],
    # 4. FP見積もり
    "ch1_general_vol51.json": [
        "5人月", # 正解候補
        "10人月",
        "15人月",
        "20人月"
    ],
    # 5. 3点見積もり期待値
    "ch1_general_vol77.json": [
        "5日 （(2 + 4*5 + 14) / 6）", # 正解候補
        "5.33日",
        "6日",
        "7日"
    ],
    # 6. リスクRPN
    "ch1_general_vol9.json": [
        "リスクA （RPNが最も高い）",
        "リスクB （RPNが最も高い）", # 正解候補（計算結果によるが仮置き）
        "リスクC （RPNが最も高い）",
        "すべて同じ"
    ],
    # 7. AI診断（空選択肢）
    "ch1_medical_vol30.json": [
        "(1), (2), (5) のみ",
        "(2), (5) のみ",
        "(1)〜(5) すべて",
        "(1) と (4) のみ"
    ],
    # 8. 予防コスト
    "ch2_general_vol90.json": [
        "妥当である（ROIがプラスになるため）", # 正解候補
        "妥当ではない（ROIがマイナスになるため）",
        "どちらとも言えない",
        "教育はコストではなく投資なので無条件に実施すべき"
    ],
    # 9. ツールTCO
    "ch2_general_vol92.json": [
        "ツールAの方が安い",
        "ツールBの方が安い", # 正解候補
        "両方同じ",
        "計算不能"
    ],
    # 10. SLA稼働率計算
    "ch3_cloud_vol41.json": [
        "約43分（99.9%）",
        "約7時間（99%）",
        "約72時間（90%）",
        "約3.5日"
    ]
}

def fix_phase1_critical():
    print("--- フェーズ1: 致命的な不具合（重複・空）の修正を開始 ---")
    
    count = 0
    for filename, new_options in fixes.items():
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(file_path):
            print(f"スキップ（ファイルなし）: {filename}")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            if isinstance(data, list):
                for q in data:
                    # 選択肢を上書き
                    # ※正解データ(answer)との整合性が崩れる可能性がありますが、
                    # まずは選択肢を表示可能な状態にすることを優先します。
                    # 必要であれば後で正解データのリンク張り直し(repair_broken_answers)を行ってください。
                    q["options"] = new_options
                    modified = True
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"修正完了: {filename}")
                count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"フェーズ1完了: {count} ファイルを修正しました。")
    print("※注意: 選択肢の内容を書き換えたため、正解判定がずれている可能性があります。")
    print("　念のため、この後に `repair_broken_answers.py` を実行することをお勧めします。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_phase1_critical()
    input()
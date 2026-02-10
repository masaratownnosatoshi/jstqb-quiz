import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第43弾・Vol.80-83 最終仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第3章 一般 Vol.82 (ch3_general_vol82.json)
    # ---------------------------
    "Q3-GEN-V82-01": { # スキル不足対策
        "options": [
            "外部のコンサルタントや専門家を一時的に招聘し、知識移転（メンタリング）を受ける",
            "リスクベースでテスト対象を絞り込み、現有人数・スキルでカバーできる範囲に集中する（スコープ調整）", # 「諦める」を修正
            "開発者にテストを丸投げする",
            "社内の有識者によるOJTや、ペアリング（ペアテスト）を通じて、実務の中でスキル移転を進める（内部育成）" # 「独学」を修正
        ],
        "answer": ["外部のコンサルタントや専門家を一時的に招聘し、知識移転（メンタリング）を受ける"]
    },

    # ---------------------------
    # 第2章 一般 Vol.81 (ch2_general_vol81.json)
    # ---------------------------
    "Q2-GEN-V81-01": { # 自動化アーキテクチャ
        "options": [
            "100個のテストスクリプトをコピー＆ペーストで作る（メンテナンス地獄）",
            "「データ駆動テスト（Data-Driven Testing）」を採用し、テストロジック（スクリプト）とテストデータ（CSV/Excel等）を分離して、1つのスクリプトでデータをループ処理させる",
            "テストデータとロジックを分離せず、スクリプト内に値をハードコーディングして実装する（保守性が低いアンチパターン）", # 「手動」を修正
            "「キーワード駆動テスト（Keyword-Driven Testing）」を採用し、アクションワードを定義してスクリプトを構造化する" # 「ランダム」を修正
        ],
        "answer": ["「データ駆動テスト（Data-Driven Testing）」を採用し、テストロジック（スクリプト）とテストデータ（CSV/Excel等）を分離して、1つのスクリプトでデータをループ処理させる"]
    },

    # ---------------------------
    # 第1章 一般 Vol.82 (ch1_general_vol82.json)
    # ---------------------------
    "Q1-GEN-V82-02": { # 終了報告書の内容
        "options": [
            "テスト活動のサマリ（計画と実績の対比）",
            "残存リスクの評価",
            "学習した教訓（Lessons Learned）",
            "テスト実行者の詳細な勤怠記録や休憩時間のログ（マイクロマネジメント情報）" # 「反省文」を修正
        ],
        "answer": ["テスト実行者の詳細な勤怠記録や休憩時間のログ（マイクロマネジメント情報）"]
    },

    # ---------------------------
    # 第1章 一般 Vol.80 (ch1_general_vol80.json)
    # ---------------------------
    "Q1-GEN-V80-01": { # バグが少ない時の対応
        "options": [
            "品質が良いと判断し、テスト期間を短縮して早期リリースを提案する",
            "テストケースが「欠陥を見つける能力」に欠けている（ザルである）可能性や、テスト環境の設定ミス（偽陰性）を疑い、探索的テストを追加して検証する",
            "テストケースの消化状況だけでなく、カバレッジ（コード網羅率）や機能網羅率を確認し、テストの抜け漏れがないか分析する", # 「全員入れ替え」を修正
            "過去の類似プロジェクトの欠陥密度と比較し、統計的に異常値であるか客観的に判断する" # 「問い詰める」を修正
        ],
        "answer": ["テストケースが「欠陥を見つける能力」に欠けている（ザルである）可能性や、テスト環境の設定ミス（偽陰性）を疑い、探索的テストを追加して検証する"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第43弾：Vol.80-83の最終修正を開始します...")

    for file_path in all_files:
        filename = os.path.basename(file_path)
        if filename.endswith(".py") or filename == "index.json":
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                continue

            file_modified = False
            
            for q in data:
                q_id = q.get("id")
                
                if q_id in fixes:
                    fix_data = fixes[q_id]
                    
                    if "options" in fix_data:
                        q["options"] = fix_data["options"]
                    if "answer" in fix_data:
                        q["answer"] = fix_data["answer"]
                    if "explanation" in fix_data:
                        q["explanation"] = fix_data["explanation"]

                    print(f"  修正適用: {q_id} ({filename})")
                    file_modified = True

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                updated_count += 1
                
        except Exception as e:
            print(f"  読み込みエラー: {filename} - {e}")

    print("-" * 30)
    print(f"完了: 合計 {updated_count} ファイルを最適化しました。")

if __name__ == "__main__":
    refine_questions()
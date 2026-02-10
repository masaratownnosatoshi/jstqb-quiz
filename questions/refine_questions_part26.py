import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第26弾・Vol.25, 35, 36 最終調整）
# ==========================================
fixes = {
    # ---------------------------
    # 第1章 一般 Vol.25 (ch1_general_vol25.json)
    # ---------------------------
    "Q1-GEN-V25-01": { # レビュー効果分析
        "options": [
            "A: 「レビュー時間（工数）」と「ページあたりの指摘数」\nB: レビュー時間が短すぎた、または形式的なチェックに終始しており、内容に踏み込んだ指摘ができていない（形骸化している）可能性があるため、レビューアのスキル構成見直しや、シナリオベースのレビュー導入を提案する",
            "A: 「テスト実行数」と「バグ発見数」\nB: テスト実行のペースが遅いことが原因なので、レビューを廃止して、その工数をすべてテスト実行に回すことで発見数を稼ぐ（予防コストの削減による品質悪化リスク）",
            "A: 「開発者の残業時間」\nB: 開発者が疲れているので、休暇を与える",
            "A: 「ドキュメントのページ数」\nB: ドキュメントが厚すぎるので、読むのをやめる"
        ],
        "answer": [
            "A: 「レビュー時間（工数）」と「ページあたりの指摘数」\nB: レビュー時間が短すぎた、または形式的なチェックに終始しており、内容に踏み込んだ指摘ができていない（形骸化している）可能性があるため、レビューアのスキル構成見直しや、シナリオベースのレビュー導入を提案する"
        ]
    },
    "Q1-GEN-V25-02": { # アジャイルテスト戦略
        "options": [
            "スプリント内では「単体テスト」と「自動化された回帰テスト」に集中し、QAチームは開発と並走して探索的テストを行い、フィードバックループを回す（Shift Left & Continuous Testing）",
            "スプリント内では機能実装を優先し、テストは全て翌スプリント以降の「安定化期間（Hardening Sprint）」にまとめて実施する（ウォーターフォール化）",
            "開発者はコードを書くことに専念すべきなので、単体テストは廃止し、全てのバグ出しをQAチームのシステムテストに委ねる",
            "バグを出した開発者に罰金を科し、品質意識を高める"
        ],
        "answer": [
            "スプリント内では「単体テスト」と「自動化された回帰テスト」に集中し、QAチームは開発と並走して探索的テストを行い、フィードバックループを回す（Shift Left & Continuous Testing）"
        ]
    },

    # ---------------------------
    # 第1章 一般 Vol.35 (ch1_general_vol35.json)
    # ---------------------------
    "Q1-GEN-V35-01": { # TMMiレベル定義
        "options": [
            "A: 戦略、B: テストプロセス、C: 欠陥予防",
            "A: ツール導入、B: 自動化スクリプト、C: AIによる自律テスト（ツール偏重）",
            "A: 予算管理、B: 人事評価制度、C: コスト削減（マネジメント偏重）",
            "A: 日程表、B: テストケース数、C: バグ出し競争"
        ],
        "answer": [
            "A: 戦略、B: テストプロセス、C: 欠陥予防"
        ]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第26弾：Vol.25/35/36の修正を開始します...")

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
    print(f"完了: 合計 {updated_count} ファイルの問題を修正しました。")

if __name__ == "__main__":
    refine_questions()
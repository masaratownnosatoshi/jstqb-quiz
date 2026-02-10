import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第40弾・Vol.72-73 最終仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 AWS Vol.73 (ch2_aws_vol73.json)
    # ---------------------------
    "Q2-AWS-V73-01": { # コスト最適化アンチパターン
        "options": [
            "開発者に「帰るときに停止する」よう毎日メールする",
            "AWS Instance Scheduler等を導入し、業務時間外（夜間・休日）に自動でインスタンスを停止・起動するスケジュールを設定する",
            "コスト削減を優先し、開発環境のインスタンスタイプを要件を無視して最も安価なもの（t2.nano等）に統一する（業務効率の低下）", # 「全削除」を修正
            "リザーブドインスタンスを購入する"
        ],
        "answer": ["AWS Instance Scheduler等を導入し、業務時間外（夜間・休日）に自動でインスタンスを停止・起動するスケジュールを設定する"]
    },

    # ---------------------------
    # 第1章 一般 Vol.72 (ch1_general_vol72.json)
    # ---------------------------
    "Q1-GEN-V72-02": { # 見積もり精度向上
        "options": [
            "マネージャが予算枠（Design to Cost）に合わせてトップダウンで決定し、現場の工数積算を行わない（デスマーチの要因）", # 「新人に任せる」を修正
            "経験豊富な実務者が、過去の類似プロジェクトの実績データ（メトリクス）や自身の経験に基づいて見積もる",
            "常に「楽観値」を採用する",
            "テスト対象ソフトウェアの品質を考慮しない"
        ],
        "answer": ["経験豊富な実務者が、過去の類似プロジェクトの実績データ（メトリクス）や自身の経験に基づいて見積もる"]
    },

    # ---------------------------
    # 第2章 一般 Vol.72_2 (ch2_general_vol72_2.json)
    # ---------------------------
    "Q2-GEN-V72-02": { # 欠陥分析
        "options": [
            "設計レビューの有効性（DRE）が低く、多くの欠陥を見逃して後工程（単体テスト）に流出させてしまっている",
            "単体テストの品質が低い",
            "設計者のスキルが高い",
            "テスト実行の進捗が予定通りであるため、欠陥の質には問題がないと判断する（質より量の誤り）" # 「正常」を修正
        ],
        "answer": ["設計レビューの有効性（DRE）が低く、多くの欠陥を見逃して後工程（単体テスト）に流出させてしまっている"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第40弾：Vol.72-73の最終修正を開始します...")

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
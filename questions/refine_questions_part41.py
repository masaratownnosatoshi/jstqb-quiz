import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第41弾・Vol.74-75 最終仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第1章 金融 Vol.75 (ch1_finance_vol75.json)
    # ---------------------------
    "Q1-FIN-V75-01": { # リスク軽減策
        "options": [
            "テスト実行時にランダムに金額を入力してみる（網羅性の欠如）",
            "境界値分析とデシジョンテーブルを用いて、手数料テーブルの境界（3万円以上/未満など）と顧客区分（一般/優遇）の組み合わせを網羅するテストケースを設計する",
            "開発者のセルフチェックに依存し、テストケースとしての明文化を行わない（品質保証の放棄）", # 「気をつけて」を修正
            "リリース後にログを監視する（予防になっていない）"
        ],
        "answer": ["境界値分析とデシジョンテーブルを用いて、手数料テーブルの境界（3万円以上/未満など）と顧客区分（一般/優遇）の組み合わせを網羅するテストケースを設計する"]
    },

    # ---------------------------
    # 第2章 医療 Vol.75 (ch2_medical_vol75.json)
    # ---------------------------
    "Q2-MED-V75-01": { # 医療機器欠陥分類
        "options": [
            "機能は動くので、Severity：低、Priority：低",
            "患者の安全に関わるユーザビリティ問題（使用エラー誘発）であるため、Severity：高（または中）、Priority：高として扱う",
            "ユーザビリティの問題は「好みの問題」として処理し、安全性リスクとして評価しない（ハザードの見落とし）", # 「バグではない」を修正
            "マニュアルで補足するので修正不要（根本対策の放棄）"
        ],
        "answer": ["患者の安全に関わるユーザビリティ問題（使用エラー誘発）であるため、Severity：高（または中）、Priority：高として扱う"]
    },

    # ---------------------------
    # 第3章 AWS Vol.75 (ch3_aws_vol75.json)
    # ---------------------------
    "Q3-AWS-V75-01": { # クラウドスキル教育
        "options": [
            "全員に基本情報技術者試験を受けさせる（ドメインが異なる）",
            "「AWS Certified Cloud Practitioner」または「Solutions Architect Associate」の取得を推奨し、学習会やハンズオン（GameDay等）を実施して、共通言語とクラウドアーキテクチャの基礎を習得させる",
            "OJTのみに依存し、体系的な知識習得の機会を与えない（知識の偏り）", # 「ヘルプ読ませる」修正
            "特定の有識者に依存した体制を維持し、ドキュメント化や知識移転への投資を行わない（属人化・バス係数リスクの無視）" # 「一人に任せる」修正
        ],
        "answer": ["「AWS Certified Cloud Practitioner」または「Solutions Architect Associate」の取得を推奨し、学習会やハンズオン（GameDay等）を実施して、共通言語とクラウドアーキテクチャの基礎を習得させる"]
    },

    # ---------------------------
    # 第1章 一般 Vol.74 (ch1_general_vol74.json)
    # ---------------------------
    "Q1-GEN-V74-02": { # 重大バグ発見時の対応
        "options": [
            "ログ出力機能のリスクレベルを「高」に引き上げ、追加の負荷テストや長時間稼働テストをスケジュールに組み込む（テスト計画の更新）",
            "偶然のバグとして処理し、計画は変更しない（正常性バイアス）",
            "ログ出力機能を削除するよう開発に依頼する（安易な機能削減）",
            "根本原因分析を行わず、担当者の個人的なミスとして処理する（再発防止の失敗）" # 「叱責」を修正
        ],
        "answer": ["ログ出力機能のリスクレベルを「高」に引き上げ、追加の負荷テストや長時間稼働テストをスケジュールに組み込む（テスト計画の更新）"]
    },

    # ---------------------------
    # 第2章 AWS Vol.74 (ch2_aws_vol74.json)
    # ---------------------------
    "Q2-AWS-V74-01": { # コスト管理ツール
        "options": [
            "AWS Cost Explorerでレポートを見るだけ（アクションにつながらない）",
            "AWS Instance Scheduler（またはEventBridge + Lambda）を導入し、金曜夜に自動停止・月曜朝に自動起動する仕組みを実装する",
            "運用担当者が手動で停止・起動する手順書を作成し、毎週実行させる（トイルの制度化）", # 「メール」を修正
            "リザーブドインスタンスを購入する（開発環境などの短期間利用には不向きな場合がある）"
        ],
        "answer": ["AWS Instance Scheduler（またはEventBridge + Lambda）を導入し、金曜夜に自動停止・月曜朝に自動起動する仕組みを実装する"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第41弾：Vol.74-75の最終修正を開始します...")

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
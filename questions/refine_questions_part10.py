import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第10弾・Vol.7 & 残存修正）
# ==========================================
fixes = {
    # ---------------------------
    # 第1章 AWS Vol.7 (ch1_aws_vol7.json)
    # ---------------------------
    "Q1-AWS-V7-01": { # コスト分析アクション
        "options": [
            "AWS Cost Explorerでタグ別のコスト推移を分析し、使用されていないEBSボリュームや、夜間稼働し続けているテスト環境（EC2/RDS）を特定して、自動停止ルールの導入効果を試算する",
            "開発チームの予算を一律10%カットし、具体的な削減方法は現場に丸投げする",
            "すべてのデータをS3 Glacier（アーカイブ）に移動し、取り出しに時間がかかる状態にする",
            "リザーブドインスタンス（RI）を全サーバー分購入し、柔軟性（スケーリング）を犠牲にして固定費化する"
        ],
        "answer": ["AWS Cost Explorerでタグ別のコスト推移を分析し、使用されていないEBSボリュームや、夜間稼働し続けているテスト環境（EC2/RDS）を特定して、自動停止ルールの導入効果を試算する"]
    },

    # ---------------------------
    # 第3章 一般 Vol.6 (ch3_general_vol6.json)
    # ---------------------------
    "Q3-GEN-V6-03": { # リテンションヒアリング
        "options": [
            "「給料を上げるから残ってくれ」と、金銭条件（衛生要因）のみで引き留めようとする",
            "「仕事に成長の実感や裁量権、達成感があったか？ 将来どうなりたいか？」を聞き、動機付け要因の不足を確認する",
            "「契約期間中は辞められないはずだ」と、就業規則を盾に強引に引き留める",
            "「どこの会社に行くんだ？競合他社なら訴えるぞ」と圧力をかける"
        ],
        "answer": ["「仕事に成長の実感や裁量権、達成感があったか？ 将来どうなりたいか？」を聞き、動機付け要因の不足を確認する"]
    },
    "Q3-GEN-V6-04": { # TPI成功要因
        "options": [
            "マネジメント層のコミットメント（支援）を得て、ビジネス目標と整合させること",
            "現場だけでこっそりと改善活動を行い、成果が出てから報告すること（ボトムアップ偏重）",
            "高価なテスト管理ツールを導入すれば、プロセスは自動的に改善されると信じること",
            "TPIモデルのすべての項目を満たすために、重厚長大なプロセス定義書を作成すること"
        ],
        "answer": ["マネジメント層のコミットメント（支援）を得て、ビジネス目標と整合させること"]
    },

    # ---------------------------
    # 第2章 一般 Vol.6 (ch2_general_vol6.json) - 補完
    # ---------------------------
    "Q2-GEN-V6-02": { # 静的解析の限界
        "options": [
            "メモリリークの可能性（リソース管理ミス）",
            "初期化されていない変数の使用",
            "顧客の潜在的なニーズや、仕様書自体の論理的矛盾（バリデーション観点）",
            "コーディング規約違反（インデントや命名規則）"
        ],
        "answer": ["顧客の潜在的なニーズや、仕様書自体の論理的矛盾（バリデーション観点）"]
    },

    # ---------------------------
    # 第3章 クラウド Vol.6 (ch3_cloud_vol6.json)
    # ---------------------------
    "Q3-CLD-V6-01": { # QAの役割変化
        "options": [
            "「品質保証（Gatekeeper）」から「品質支援（Quality Assistance / Coach）」へシフトし、開発者がテストできる環境を整える",
            "テスト工程を増やし、開発者から納品されたコードを厳格に検査する「門番」としての権限を強化する",
            "インフラ構築作業をすべて引き受け、SREチームに統合される",
            "開発者の生産性を監視し、コード行数で評価する管理者になる"
        ],
        "answer": ["「品質保証（Gatekeeper）」から「品質支援（Quality Assistance / Coach）」へシフトし、開発者がテストできる環境を整える"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第10弾：ファイナル修正を開始します...")

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
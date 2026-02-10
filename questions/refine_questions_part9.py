import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第9弾・Vol.6対応）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.6 (ch2_general_vol6.json)
    # ---------------------------
    "Q2-GEN-V6-04": { # テストハーネス
        "options": [
            "テスト対象を実行するために必要なスタブやドライバ、ツールを含んだ環境一式",
            "テスト担当者が高所作業で着用する安全帯",
            "テストケースとテスト手順、および期待結果を記述したドキュメント",
            "発見された欠陥を管理するためのチケット管理システム"
        ],
        "answer": ["テスト対象を実行するために必要なスタブやドライバ、ツールを含んだ環境一式"]
    },

    # ---------------------------
    # 第1章 金融 Vol.6 (ch1_finance_vol6.json)
    # ---------------------------
    "Q1-FIN-V6-01": { # 境界値分析の対象
        "options": [
            "顧客の氏名（漢字・カナ）",
            "口座残高と適用金利の閾値（100万円以上、1000万円以上など）",
            "支店コード（3桁の数字）",
            "取引種別（振込、振替、預入）"
        ],
        "answer": ["口座残高と適用金利の閾値（100万円以上、1000万円以上など）"]
    },
    "Q1-FIN-V6-02": { # 状態遷移テストの対象
        "options": [
            "ローン審査プロセス（申込→審査中→承認/却下→融資実行）",
            "ログイン画面の入力フィールドの最大文字数",
            "日次バッチ処理のデータ処理速度",
            "利息計算の計算式の正確性"
        ],
        "answer": ["ローン審査プロセス（申込→審査中→承認/却下→融資実行）"]
    },

    # ---------------------------
    # 第1章 一般 Vol.6 (ch1_general_vol6.json)
    # ---------------------------
    "Q1-GEN-V6-05": { # デシジョンテーブル
        "options": [
            "複雑なビジネスロジック（条件の組み合わせ）の漏れ抜けを防げる",
            "仕様書の矛盾（あり得ない組み合わせ等）を発見できる",
            "UIのレイアウト崩れや配色の誤りを自動的に発見できる",
            "テスト実行にかかる時間を短縮し、自動化を不要にする"
        ],
        "answer": [
            "複雑なビジネスロジック（条件の組み合わせ）の漏れ抜けを防げる",
            "仕様書の矛盾（あり得ない組み合わせ等）を発見できる"
        ]
    },

    # ---------------------------
    # 第2章 AWS Vol.6 (ch2_aws_vol6.json)
    # ---------------------------
    "Q2-AWS-V6-01": { # JMeterボトルネック
        "options": [
            "分散負荷テスト（複数のEC2から負荷をかける）を行う",
            "クライアントマシンのスペック（CPU/メモリ）を垂直スケーリングで増強する",
            "テスト対象のサーバーを一時的に停止する",
            "WiFiを有線LANに切り替える"
        ],
        "answer": ["分散負荷テスト（複数のEC2から負荷をかける）を行う"]
    },
    "Q2-AWS-V6-02": { # CodePipelineメリット
        "options": [
            "コードコミットのたびに自動でテストが走り、フィードバックループが高速化する（CI/CD）",
            "AIがテストコードを自動生成し、人間が書く必要がなくなる",
            "本番環境へのデプロイ承認プロセスを強制し、誤リリースを防ぐ",
            "AWS利用料が自動的に割引される"
        ],
        "answer": ["コードコミットのたびに自動でテストが走り、フィードバックループが高速化する（CI/CD）"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第9弾：問題データの修正を開始します...")

    for file_path in all_files:
        filename = os.path.basename(file_path)
        # スクリプトファイルなどは除外
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
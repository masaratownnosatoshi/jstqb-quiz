import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第18弾・Vol.14 仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第1章 一般 Vol.14 (ch1_general_vol14.json)
    # ---------------------------
    "Q1-GEN-V14-01": { # Works on my machine
        "options": [
            "開発者の主張を鵜呑みにし、「再現せず」としてチケットを即座にクローズする",
            "テスト環境と開発環境の差異（OS、ブラウザ、データ、設定）を確認し、再現手順を再検証して、より詳細なログやスクリーンショットを添付して再オープンする",
            "開発者の席まで行き、開発者のPC上でデバッグしてもらうよう強要する（根本解決にならない）",
            "バグではないとみなし、要望（Enhancement）チケットとして登録し直す"
        ],
        "answer": ["テスト環境と開発環境の差異（OS、ブラウザ、データ、設定）を確認し、再現手順を再検証して、より詳細なログやスクリーンショットを添付して再オープンする"]
    },

    # ---------------------------
    # 第1章 金融 Vol.14 (ch1_finance_vol14.json)
    # ---------------------------
    "Q1-FIN-V14-01": { # 1円バグのトリアージ
        "options": [
            "発生確率が低いため、「既知の不具合（Known Issue）」としてリリースノートに記載し、修正を次期バージョンに先送りする",
            "金額の不整合は「信用リスク」に直結するため、発生確率に関わらず「Severity: High（最重要）」として扱い、原因究明と修正を行う",
            "ユーザー影響が軽微であると判断し、運用チームに手動での補正対応を依頼する",
            "テストデータの誤りであると仮定し、再テストを行わずに様子を見る"
        ],
        "answer": ["金額の不整合は「信用リスク」に直結するため、発生確率に関わらず「Severity: High（最重要）」として扱い、原因究明と修正を行う"]
    },

    # ---------------------------
    # 第2章 AWS Vol.14 (ch2_aws_vol14.json)
    # ---------------------------
    "Q2-AWS-V14-01": { # CodeBuild高速化
        "options": [
            "CIでのテスト実行をスキップし、開発者のローカル環境でのテスト結果を正とする（品質リスク）",
            "CodeBuildの「コンピューティングタイプ」を上げる、またはテスト分割設定（Batch Build / Parallel）を利用して並列実行する",
            "ビルドキャッシュを無効化し、毎回クリーンな状態から依存関係をインストールし直す（逆効果）",
            "テストケースをランダムに間引いて実行する（サンプリング検査）"
        ],
        "answer": ["CodeBuildの「コンピューティングタイプ」を上げる、またはテスト分割設定（Batch Build / Parallel）を利用して並列実行する"]
    },

    # ---------------------------
    # 第2章 クラウド Vol.14 (ch2_cloud_vol14.json)
    # ---------------------------
    "Q2-CLD-V14-01": { # サービス仮想化
        "options": [
            "Dockerコンテナを用いて、接続先のデータベースやAPIサーバーの本物を毎回立ち上げる（起動コスト高）",
            "利用できない、またはコストが高い外部システム（API、メインフレーム等）の振る舞いをシミュレートし、テストをブロックさせない",
            "本番環境の外部システムに直接接続してテストを行う（データ汚染リスク）",
            "外部システムとの連携部分はテストせず、結合テストまで先送りする"
        ],
        "answer": ["利用できない、またはコストが高い外部システム（API、メインフレーム等）の振る舞いをシミュレートし、テストをブロックさせない"]
    },

    # ---------------------------
    # 第2章 一般 Vol.14 (ch2_general_vol14.json)
    # ---------------------------
    "Q2-GEN-V14-01": { # キーワード駆動テスト
        "options": [
            "すべてのテスト手順をプログラミング言語（Java/Python等）でハードコードする（スクリプト駆動）",
            "アクションワード（例：「ログインする」「商品を追加する」）を定義し、スクリプト知識がない人でもテストを構築できるようにする",
            "自然言語処理（NLP）を用いて、要件定義書からテストケースを自動生成する（モデルベースドテスト等）",
            "画面操作を録画し、それを再生することでテストとする（キャプチャ＆リプレイ）"
        ],
        "answer": ["アクションワード（例：「ログインする」「商品を追加する」）を定義し、スクリプト知識がない人でもテストを構築できるようにする"]
    },

    # ---------------------------
    # 第3章 一般 Vol.14 (ch3_general_vol14.json)
    # ---------------------------
    "Q3-GEN-V14-01": { # ツール導入失敗原因
        "options": [
            "ツール自体に致命的なバグがあり、動作しなかった",
            "現場の課題やプロセス適合性を無視して、マネージャがトップダウンで「機能の多さ」だけで選定・導入してしまった",
            "ツールの導入教育（トレーニング）を行わず、現場の自主性に任せた結果、使い方が分からず放置された",
            "オープンソースのツールを選定したため、サポートが得られなかった"
        ],
        "answer": ["現場の課題やプロセス適合性を無視して、マネージャがトップダウンで「機能の多さ」だけで選定・導入してしまった"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第18弾：問題データの修正を開始します...")

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
import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.103 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol103.json)
q3_gen = [
    {
        "id": "Q3-GEN-V103-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストプロセス改善計画の策定。\n現状のテストプロセスにおいて「回帰テストの実行に時間がかかりすぎる」という課題がある。\n改善のためのアクションプランとして、最も効果的かつ持続可能なアプローチはどれか。",
        "options": [
            "テスト担当者を倍増させ、手動テストを並列で実行することで時間短縮を図る（コスト増であり、プロセスの効率化にはならない）",
            "リスクベースでテストケースの優先順位付けを行い、高リスクなテストケースを自動化することで、効率的な回帰テストを実現する",
            "回帰テストの実施頻度を減らし、リリース直前の1回のみ実行することで、全体のテスト時間を短縮する（品質リスクの増大）",
            "テストケースの内容を簡略化し、詳細な手順を省略することで、テスト実行にかかる時間を短縮する（テストの信頼性低下）"
        ],
        "answer": [
            "リスクベースでテストケースの優先順位付けを行い、高リスクなテストケースを自動化することで、効率的な回帰テストを実現する"
        ],
        "explanation": "【解説】\n回帰テストの効率化には「自動化」と「リスクベースの選定」が有効です。単なる増員や実施頻度の削減は、コストや品質リスクの問題を解決しません。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol103.json)
q1_gen = [
    {
        "id": "Q1-GEN-V103-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テスト設計技法の選択。\n「ユーザーの年齢」と「会員ランク」の組み合わせによって割引率が決まるシステムにおいて、網羅的なテストを行いたい。\n最も効率的かつ効果的なテスト技法はどれか。",
        "options": [
            "全ての可能な年齢と会員ランクの組み合わせをリストアップし、それぞれのケースについてテストを実行する（全網羅は非効率）",
            "デシジョンテーブル（決定表）を作成し、条件の組み合わせと期待される動作（割引率）を整理してテストケースを導出する",
            "年齢と会員ランクの値をランダムに入力し、システムがエラーを出さないことを確認する（ロジックの網羅性が低い）",
            "開発者にロジックの実装内容を確認し、コードレビューのみでテストを代替する（動的な動作確認が不足）"
        ],
        "answer": [
            "デシジョンテーブル（決定表）を作成し、条件の組み合わせと期待される動作（割引率）を整理してテストケースを導出する"
        ],
        "explanation": "【解説】\n条件の組み合わせによるロジックテストには、デシジョンテーブルが最適です。全網羅はコストがかかりすぎ、ランダムテストは漏れが発生しやすいため不適切です。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol103.json)
q2_gen = [
    {
        "id": "Q2-GEN-V103-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】欠陥レポートの品質評価。\n提出された欠陥レポートの中に、「システムが時々フリーズする」という記述のみのものがあった。\nこのレポートの問題点と、改善のためのフィードバックとして適切なものはどれか。",
        "options": [
            "再現手順や発生条件が記載されていないため、開発者が調査・修正を行うことが困難である。具体的な手順、環境情報、発生頻度などを追記するよう指示する",
            "フリーズという現象は重大な欠陥であるため、詳細な情報がなくても直ちに修正作業に着手するよう開発チームに命じる（情報不足で修正不可）",
            "再現性が低いバグは修正の優先度が低いため、このレポートはクローズし、再現手順が確立されるまで放置する（潜在リスクの無視）",
            "テスターの個人的な感覚による報告である可能性が高いため、レポート自体を無効とし、客観的なデータに基づく報告のみを受け付けるようにする（報告の機会損失）"
        ],
        "answer": [
            "再現手順や発生条件が記載されていないため、開発者が調査・修正を行うことが困難である。具体的な手順、環境情報、発生頻度などを追記するよう指示する"
        ],
        "explanation": "【解説】\n欠陥レポートには「再現性」が不可欠です。詳細情報がない報告は開発者の負担を増やすだけであり、具体的な情報の追記を求めるのが適切なフィードバックです。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol103.json)
q1_aws = [
    {
        "id": "Q1-AWS-V103-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】AWS Lambdaのパフォーマンスチューニング。\nLambda関数の実行時間が長く、タイムアウトエラーが頻発している。\nパフォーマンスを改善するためのアプローチとして、最も適切かつ効果的なものはどれか。",
        "options": [
            "タイムアウト時間を最大値（15分）に設定し、処理が終わるまで待つようにする（根本解決にならず、コスト増のリスク）",
            "Lambda関数のメモリ割り当て量を増やすことで、CPUパワーも比例して増加させ、処理速度を向上させる",
            "処理をEC2インスタンスに移行し、常時稼働させることでコールドスタートの影響を回避する（サーバーレスのメリットを捨てる）",
            "Lambda関数のコードを全面的に書き直し、処理ロジックを簡素化することで実行時間を短縮する（工数がかかりすぎる）"
        ],
        "answer": [
            "Lambda関数のメモリ割り当て量を増やすことで、CPUパワーも比例して増加させ、処理速度を向上させる"
        ],
        "explanation": "【解説】\nAWS Lambdaでは、メモリ割り当て量を増やすとCPUパワーも比例して増加します。コード修正なしでパフォーマンスを改善できる有効な手段です。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol103.json)
q2_fin = [
    {
        "id": "Q2-FIN-V103-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】金融システムのセキュリティテスト。\nインターネットバンキングシステムにおいて、SQLインジェクション攻撃に対する脆弱性を検証したい。\n最も効果的かつ安全なテスト方法はどれか。",
        "options": [
            "本番環境に対して自動攻撃ツールを実行し、脆弱性を検出する（本番データ破壊のリスクが高く危険）",
            "テスト環境において、静的解析ツール（SAST）と動的アプリケーションセキュリティテスト（DAST）ツールを組み合わせて脆弱性を診断する",
            "開発者にコードレビューを依頼し、SQL文の構築箇所を目視で確認してもらう（見落としのリスクがある）",
            "WAF（Web Application Firewall）を導入し、全てのSQLインジェクション攻撃をブロックすることで、アプリケーション側の修正を不要にする（根本対策ではない）"
        ],
        "answer": [
            "テスト環境において、静的解析ツール（SAST）と動的アプリケーションセキュリティテスト（DAST）ツールを組み合わせて脆弱性を診断する"
        ],
        "explanation": "【解説】\nセキュリティテストはテスト環境で行うのが原則です。SASTとDASTを組み合わせることで、コードレベルと動作レベルの両面から脆弱性を検出できます。",
        "tags": ["第2章", "金融", "シナリオ", "K3"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol103.json": q3_gen,
    "ch1_general_vol103.json": q1_gen,
    "ch2_general_vol103.json": q2_gen,
    "ch1_aws_vol103.json": q1_aws,
    "ch2_finance_vol103.json": q2_fin
}

def generate_and_update():
    # 1. ファイル生成
    new_entries = []
    
    print("--- ファイル生成開始 ---")
    for filename, content in files_content.items():
        file_path = os.path.join(OUTPUT_DIR, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            print(f"作成: {filename}")
            
            # メタデータ抽出（Index用）
            first_q = content[0]
            entry = {
                "path": f"questions/{filename}", # アプリの仕様に合わせたパス
                "chapter": first_q.get("chapter", "不明"),
                "category": first_q.get("category", "不明"),
                "klevel": first_q.get("level", "K2"),
                "qCount": len(content)
            }
            new_entries.append(entry)
            
        except Exception as e:
            print(f"エラー作成中 {filename}: {e}")

    # 2. Index更新
    print("\n--- Index更新開始 ---")
    if not os.path.exists(INDEX_FILE):
        print(f"エラー: {INDEX_FILE} が見つかりません。")
        return

    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        existing_paths = {item.get("path") for item in index_data.get("chunks", [])}
        added_count = 0
        
        for entry in new_entries:
            if entry["path"] not in existing_paths:
                index_data["chunks"].append(entry)
                print(f"Index追加: {entry['path']}")
                added_count += 1
            else:
                print(f"Indexスキップ（登録済）: {entry['path']}")
        
        if added_count > 0:
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
            print(f"Index保存完了: {added_count}件追加")
        else:
            print("Index更新なし")

    except Exception as e:
        print(f"Index更新エラー: {e}")

if __name__ == "__main__":
    generate_and_update()
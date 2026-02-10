import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.133 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol133.json)
q3_gen = [
    {
        "id": "Q3-GEN-V133-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】欠陥ライフサイクルの管理。\n開発者が「修正完了（Fixed）」ステータスに変更したバグチケットに対し、テスト担当者が確認テスト（Re-test）を行ったところ、バグが直っていないことが判明した。\nこの時点でテスト担当者が取るべき、バグ追跡システム上のアクションはどれか。",
        "options": [
            "そのチケットのステータスを「再オープン（Re-opened）」に戻し、テスト結果のコメントとして再現手順やログを追記して開発者に差し戻す",
            "既存のチケットは履歴として残すために「クローズ（Closed）」し、同じ内容で新しいチケットを新規作成して開発者に割り当てる",
            "開発者が直したと言っているため、テスターの環境設定ミスである可能性が高いと判断し、チケットの状態は変更せずに様子を見る",
            "チケットのステータスを「却下（Rejected）」に変更し、このバグは修正不可能であることを記録する"
        ],
        "answer": [
            "そのチケットのステータスを「再オープン（Re-opened）」に戻し、テスト結果のコメントとして再現手順やログを追記して開発者に差し戻す"
        ],
        "explanation": "【解説】\n修正確認でNGだった場合は、ステータスを「Re-opened（差し戻し）」にするのが標準的なフローです。新規作成してしまうと、そのバグの経緯（修正履歴や議論）が分断されてしまいます。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol133.json)
q1_gen = [
    {
        "id": "Q1-GEN-V133-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ユーザー受入テスト（UAT）の主体。\n基幹システムの刷新プロジェクトにおいて、開発ベンダーによるシステムテストが完了し、本番移行前の最終段階である「ユーザー受入テスト（UAT）」を開始することになった。\nこのテストフェーズにおける適切な実施体制はどれか。",
        "options": [
            "実際の業務を行う利用部門（ユーザー）が主体となり、本番に近い環境とデータを用いて、実際の業務シナリオに沿った操作を行う",
            "開発ベンダーのプログラマーが主体となり、単体テストコードを本番環境で再実行して、機能的な不具合がないことを技術的に保証する",
            "システム運用担当者が主体となり、サーバーの電源投入やバックアップ取得の手順のみを確認し、業務機能の確認は省略する",
            "外部の第三者検証会社のみで実施し、業務知識を持たないテスターが探索的テストを行って、ユーザーの代わりに合否を判定する"
        ],
        "answer": [
            "実際の業務を行う利用部門（ユーザー）が主体となり、本番に近い環境とデータを用いて、実際の業務シナリオに沿った操作を行う"
        ],
        "explanation": "【解説】\nUAT（User Acceptance Testing）の目的は、システムが「ビジネスの要件を満たし、業務で使えるか」を確認することです。したがって、業務を知っている実際のユーザーが主体となって実施する必要があります。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol133.json)
q2_gen = [
    {
        "id": "Q2-GEN-V133-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】経験ベースのテスト技法（エラー推測）。\n仕様書には記載されていないが、経験豊富なテスターが「この入力欄に特殊文字を入れると文字化けしそうだ」と直感し、そのケースを実行したところバグを発見した。\nこのテスト技法に該当するものはどれか。",
        "options": [
            "エラー推測（Error Guessing）：テスターの知識、経験、過去の失敗事例などに基づいて、欠陥が発生しそうな箇所を予測してテストする技法",
            "境界値分析（Boundary Value Analysis）：仕様で定義された入力範囲の境界とその前後を機械的にテストする技法",
            "状態遷移テスト（State Transition Testing）：システムの状態変化図に基づいて、遷移パスを網羅する技法",
            "デシジョンテーブルテスト（Decision Table Testing）：条件と動作の組み合わせを表に整理して網羅する技法"
        ],
        "answer": [
            "エラー推測（Error Guessing）：テスターの知識、経験、過去の失敗事例などに基づいて、欠陥が発生しそうな箇所を予測してテストする技法"
        ],
        "explanation": "【解説】\n「直感」や「経験」に基づいてバグを探すアプローチは「エラー推測」と呼ばれます。仕様ベースの技法（境界値など）を補完する重要な技法です。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol133.json)
q1_aws = [
    {
        "id": "Q1-AWS-V133-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】Route 53のフェイルオーバー・ルーティング。\nプライマリサイト（東京）とセカンダリサイト（大阪）でDR（災害復旧）構成を組んでいる。\n通常時は東京にアクセスさせ、東京のサーバーがダウンした時のみ大阪にトラフィックを切り替えたい。\nRoute 53で設定すべきルーティングポリシーとヘルスチェックの組み合わせはどれか。",
        "options": [
            "フェイルオーバールーティングポリシーを選択し、プライマリとセカンダリのレコードを作成した上で、プライマリ側にヘルスチェックを関連付けて監視させる",
            "加重ルーティングポリシー（Weighted Routing）を選択し、東京と大阪に50:50の重みを設定して、アクセスを均等に分散させる",
            "レイテンシールーティングポリシーを選択し、ユーザーにとってネットワーク遅延が少ない方のリージョンに自動的に接続させる",
            "シンプルルーティングポリシーを選択し、一つのレコードに東京と大阪の両方のIPアドレスを登録して、ブラウザ側に選択させる"
        ],
        "answer": [
            "フェイルオーバールーティングポリシーを選択し、プライマリとセカンダリのレコードを作成した上で、プライマリ側にヘルスチェックを関連付けて監視させる"
        ],
        "explanation": "【解説】\nActive-Standby構成で自動切り替えを行うには「フェイルオーバールーティング」を使用します。ヘルスチェックが失敗（Unhealthy）になると、自動的にセカンダリへDNS回答が切り替わります。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol133.json)
q2_fin = [
    {
        "id": "Q2-FIN-V133-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】銀行勘定調整（Bank Reconciliation）の不整合原因。\n経理システムの「当座預金出納帳」の残高と、銀行から届いた「残高証明書」の残高が一致しない。\n原因を調査したところ、自社が振り出した小切手が、まだ受取人によって銀行に持ち込まれていないことが判明した。\nこの「未取立小切手（Outstanding Check）」に関するシステムの正しい挙動または解釈はどれか。",
        "options": [
            "これは正常な「時間的差異（Timing Difference）」であるため、銀行残高から未取立小切手の金額を差し引くことで、自社の帳簿残高と一致することを検証する（調整表の作成）",
            "自社の帳簿残高が間違っていると判断し、銀行残高に合わせて帳簿の数字を強制的に修正する仕訳を自動生成する",
            "小切手が紛失された可能性が高いため、直ちにその小切手を無効化（Void）し、帳簿上の出金記録を取り消す処理を行う",
            "銀行側のシステムミスであるため、銀行に対して残高証明書の再発行を依頼し、小切手分が差し引かれた証明書を入手する"
        ],
        "answer": [
            "これは正常な「時間的差異（Timing Difference）」であるため、銀行残高から未取立小切手の金額を差し引くことで、自社の帳簿残高と一致することを検証する（調整表の作成）"
        ],
        "explanation": "【解説】\n銀行勘定調整の典型的なパターンです。自社は出金済みだが銀行は未引落し（未呈示小切手/未取立）の場合、両者の残高は一時的にズレますが、調整表（Reconciliation Report）を作成して差異理由を説明できれば「照合OK」となります。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol133.json": q3_gen,
    "ch1_general_vol133.json": q1_gen,
    "ch2_general_vol133.json": q2_gen,
    "ch1_aws_vol133.json": q1_aws,
    "ch2_finance_vol133.json": q2_fin
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
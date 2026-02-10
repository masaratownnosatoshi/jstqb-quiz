import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.121 新規問題データ定義（括弧なし版）
# ==========================================

# 1. 第3章 一般 (ch3_general_vol121.json)
q3_gen = [
    {
        "id": "Q3-GEN-V121-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】リスクベーステスト（RBT）におけるリスク評価。\nプロジェクトのリスク分析会議において、「機能A」のリスクレベルを決定したい。\n「機能A」は滅多に使われない管理機能だが、もしバグがあると全社員の給与計算が停止し、甚大な損害が発生する。\nこの場合のリスク評価として、一般的に最も適切なものはどれか。",
        "options": [
            "発生頻度が極めて低いため、障害が発生してもすぐに対応すれば問題ないと考え、リスクレベルは「低（Low）」と評価してテストの優先度を下げる",
            "発生確率は低いが、発生した際の影響度（インパクト）が極大であるため、リスクレベルは「高（High）」または「最高（Critical）」と評価し、重点的にテストを行う",
            "発生確率と影響度の数値を足して2で割り、平均値をとってリスクレベルを「中（Medium）」とする",
            "過去にバグが出たことがない機能であれば、将来もバグは出ないと仮定できるため、リスク分析の対象外とする"
        ],
        "answer": [
            "発生確率は低いが、発生した際の影響度（インパクト）が極大であるため、リスクレベルは「高（High）」または「最高（Critical）」と評価し、重点的にテストを行う"
        ],
        "explanation": "【解説】\nリスクは「発生確率 × 影響度」で評価されます。たとえ発生頻度が低くても、ビジネスへのインパクトが壊滅的であれば、それは高リスクとして扱うのがRBTの鉄則です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol121.json)
q1_gen = [
    {
        "id": "Q1-GEN-V121-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】探索的テスト（Exploratory Testing）の管理。\nセッションベースドテスト管理（SBTM）を導入して探索的テストを行っている。\n各セッションの記録として残すべき情報の組み合わせとして、後から第三者がテスト内容を追跡・評価するために不可欠なものはどれか。",
        "options": [
            "発見したバグのスクリーンショットのみをフォルダに保存し、どのような操作を行ったかの記録や感想は一切残さない",
            "テストの開始時間と終了時間だけをタイムカードのように記録し、時間内に何をしたかはテスターの記憶に留める",
            "実施した「チャーター（目的）」、実際にカバーした「エリア」、発見した「バグ」、および次回のテストへの「提案（機会）」を含むセッションシートを作成する",
            "操作したすべてのキー入力とマウスクリックをキーロガーで記録し、数ギガバイトのログファイルとして保存する"
        ],
        "answer": [
            "実施した「チャーター（目的）」、実際にカバーした「エリア」、発見した「バグ」、および次回のテストへの「提案（機会）」を含むセッションシートを作成する"
        ],
        "explanation": "【解説】\nSBTMでは、セッションシート（レポート）が成果物となります。単なるバグ報告だけでなく、「何をテストしたか（Coverage）」「何を感じたか」を残すことで、管理と説明責任を果たします。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol121.json)
q2_gen = [
    {
        "id": "Q2-GEN-V121-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】原因結果グラフ（Cause-Effect Graphing）。\n複雑な論理仕様を持つシステムのテスト設計において、デシジョンテーブルを作成しようとしたが、条件の組み合わせが膨大になりすぎて扱いきれない。\n条件間の制約（例：条件Aが真なら条件Bは必ず偽になる）を整理してテストケースを削減するために有効な、原因結果グラフの表記法はどれか。",
        "options": [
            "条件Aと条件Bの間に「排他（Exclusive）」や「包含（Inclusive）」といった制約関係の記号を記述し、論理的にあり得ない組み合わせをグラフ段階で排除する",
            "すべての条件を「OR」で結合し、どれか一つでも真になれば結果が真になるようにグラフを簡略化する",
            "条件間の関係性は無視し、原因ノードと結果ノードをランダムに線で結んで、見た目が綺麗なグラフを作成する",
            "原因結果グラフ法は制約条件を扱えないため、あきらめてすべての組み合わせ（2のn乗）をテストする"
        ],
        "answer": [
            "条件Aと条件Bの間に「排他（Exclusive）」や「包含（Inclusive）」といった制約関係の記号を記述し、論理的にあり得ない組み合わせをグラフ段階で排除する"
        ],
        "explanation": "【解説】\n原因結果グラフ（CEG）の大きな利点は、制約（Constraint）を明記できることです。E（排他）、I（包含）、O（唯一）、R（要求）などの制約記号を使って、無効な組み合わせをテスト設計段階で削除できます。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol121.json)
q1_aws = [
    {
        "id": "Q1-AWS-V121-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】VPCネットワークのトラブルシューティング。\nプライベートサブネットにあるEC2インスタンスからインターネットへの通信が繋がらない。\nルートテーブルの設定やNAT Gatewayの状態を確認するために、パケットの拒否/許可情報を時系列で調査したい。\n有効化すべきAWS機能はどれか。",
        "options": [
            "AWS CloudTrailを有効化し、APIの呼び出し履歴から通信パケットの中身を確認する",
            "VPC Flow Logsを有効化し、ネットワークインターフェースを行き来するIPトラフィックのメタデータ（送信元、宛先、アクションACCEPT/REJECT）を取得して分析する",
            "Amazon Inspectorを実行し、OS内部の脆弱性スキャンを行うことでネットワークの問題を特定する",
            "AWS Trusted Advisorを確認し、コスト削減の推奨事項の中にネットワークエラーの記載がないかを探す"
        ],
        "answer": [
            "VPC Flow Logsを有効化し、ネットワークインターフェースを行き来するIPトラフィックのメタデータ（送信元、宛先、アクションACCEPT/REJECT）を取得して分析する"
        ],
        "explanation": "【解説】\nネットワークの接続問題（SGやNACLによる拒否など）を調査するには、VPC Flow Logsが最適です。CloudTrailは「誰が設定変更したか（管理操作）」のログであり、通信パケット自体は見えません。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol121.json)
q2_fin = [
    {
        "id": "Q2-FIN-V121-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】為替予約（Forward Exchange）の期日管理。\n輸入企業向けのシステムで、将来の特定日に外貨を購入する「為替予約」機能をテストしている。\n「予約実行日（受渡日）」が銀行休業日（土日祝）に当たった場合の処理として、金融慣行に基づき検証すべき挙動はどれか。",
        "options": [
            "銀行が休みであってもシステムは24時間稼働しているため、土日祝日の日付のまま決済処理が実行されることを確認する",
            "休業日に当たった場合は、翌営業日（Following）または前営業日（Preceding）、あるいは修正翌営業日（Modified Following）など、契約で定められたルールに従って日付が自動調整されることを確認する",
            "休業日の予約は無効となるため、エラーメッセージを表示して予約自体を自動的にキャンセルすることを確認する",
            "休業日の判定は複雑であるため、ユーザーが手動で日付を変更するまでシステムは何もしない（待機状態になる）ことを確認する"
        ],
        "answer": [
            "休業日に当たった場合は、翌営業日（Following）または前営業日（Preceding）、あるいは修正翌営業日（Modified Following）など、契約で定められたルールに従って日付が自動調整されることを確認する"
        ],
        "explanation": "【解説】\n金融システムでは「休日調整（Business Day Convention）」が極めて重要です。単純に翌営業日にずらすのか（Following）、月を跨ぐなら前倒しするのか（Modified Following）など、仕様通りのロールロジックをテストします。",
        "tags": ["第2章", "金融", "シナリオ", "K3"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol121.json": q3_gen,
    "ch1_general_vol121.json": q1_gen,
    "ch2_general_vol121.json": q2_gen,
    "ch1_aws_vol121.json": q1_aws,
    "ch2_finance_vol121.json": q2_fin
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
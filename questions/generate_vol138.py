import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.138 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol138.json)
q3_gen = [
    {
        "id": "Q3-GEN-V138-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】構成管理（CM）とテストの整合性。\nテスト実行中に「バージョン1.0」のバグ修正パッチが適用されたが、どの環境にどのパッチが当たっているかが管理されておらず、テスト結果の信頼性が揺らいでいる。\nテスト環境の完全性（Integrity）を取り戻すための構成管理プロセスとして、最も適切なアクションはどれか。",
        "options": [
            "すべてのテスト環境を一旦初期化し、ビルドサーバーから正規の「バージョン1.1」を一斉にデプロイし直して、環境ごとの差異をなくしてからテストを再開する",
            "開発者に口頭で確認し、「たぶん当たっているはずだ」という回答が得られた環境については、そのままテストを続行する",
            "本番環境は構成管理がしっかりしているため、開発環境やテスト環境のバージョン管理は諦めて、本番環境で直接テストを行うことにする",
            "バージョン管理ツール（Git等）のログを確認し、コミットメッセージに「修正済み」と書いてあれば、実際の環境確認は省略して合格とする"
        ],
        "answer": [
            "すべてのテスト環境を一旦初期化し、ビルドサーバーから正規の「バージョン1.1」を一斉にデプロイし直して、環境ごとの差異をなくしてからテストを再開する"
        ],
        "explanation": "【解説】\nテスト対象のバージョンが不明確な状態（Configuration Drift）でのテストは無意味です。不確実な場合は、クリーンな状態にリセットし、識別されたビルドを再デプロイするのが唯一の解決策です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol138.json)
q1_gen = [
    {
        "id": "Q1-GEN-V138-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】静的解析ツールの誤検知（False Positive）。\nCI/CDパイプラインにセキュリティ静的解析（SAST）を導入したところ、大量の警告が出たが、その多くは実際には問題のないコード（誤検知）であった。\n開発チームが警告を無視するようになるのを防ぐために、テストエンジニアが取るべき対策はどれか。",
        "options": [
            "ツールの検出ルールをチューニングして誤検知パターンを除外設定（Suppress/Ignore）にし、本当に修正すべき重要な警告だけが通知されるように最適化する",
            "ツールが警告を出している以上、すべてが潜在的なバグである可能性があるため、開発者に対して全ての警告を修正するまでマージを禁止する",
            "静的解析ツールは誤検知が多いので役に立たないと判断し、ツールの使用を中止してすべて人間によるコードレビューに切り替える",
            "警告の件数だけをKPIとして管理し、中身の精査は行わずに、件数が減っている傾向があれば良しとする"
        ],
        "answer": [
            "ツールの検出ルールをチューニングして誤検知パターンを除外設定（Suppress/Ignore）にし、本当に修正すべき重要な警告だけが通知されるように最適化する"
        ],
        "explanation": "【解説】\n静的解析の「オオカミ少年（誤検知過多）」問題に対する正攻法は、ルールのチューニングです。ノイズを減らし、信頼できる警告だけを届けることで、開発者の是正行動を促します。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol138.json)
q2_gen = [
    {
        "id": "Q2-GEN-V138-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】境界値分析の「2点法」と「3点法」。\n入力範囲が「10〜20（整数）」の仕様に対し、テストケースの数を最小限にしつつ、有効値と無効値の境界を効率的に確認したい。\n「2点法」を採用した場合に選択される値のセットとして正しいものはどれか。",
        "options": [
            "有効値の端点である「10」と「20」のみを選択し、無効値のテストは行わない",
            "境界値の「10」と「20」、およびその外側の無効値「9」と「21」の計4点を選択する",
            "境界値「10」とその隣接値「9」「11」、および「20」とその隣接値「19」「21」の計6点を選択する（これは3点法）",
            "範囲内の代表値「15」と、範囲外の代表値「0」「100」を選択する"
        ],
        "answer": [
            "境界値の「10」と「20」、およびその外側の無効値「9」と「21」の計4点を選択する"
        ],
        "explanation": "【解説】\nISTQBにおける「2点法（2-value）」は、境界上の値（ON）と、そのすぐ外側の無効値（OFF）のペアを確認する方法です。したがって、下限で(9, 10)、上限で(20, 21)の4点となります。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol138.json)
q1_aws = [
    {
        "id": "Q1-AWS-V138-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】DynamoDBのキャパシティモード選択。\nアクセス頻度が予測不能で、年に数回だけスパイク的なアクセスが集中するキャンペーンサイト用のデータベースを構築する。\n運用管理の手間を最小限にしつつ、急激な負荷に耐え、かつコストを最適化するためのDynamoDBの設定と検証方法はどれか。",
        "options": [
            "キャパシティモードを「オンデマンド（On-Demand）」に設定し、負荷テストで急激なトラフィック増加に対してもスロットリング（Throttling）が発生せずにオートスケールすることを確認する",
            "「プロビジョニング済み（Provisioned）」モードを選択し、想定される最大アクセス数に合わせて最初から高いWCU/RCUを固定設定しておく",
            "Auto Scaling設定を入れたプロビジョニングモードを選択するが、スケーリングには数分のタイムラグがあることを許容する",
            "DynamoDBは使用せず、RDS for MySQLを選択して、インスタンスサイズをt3.microに固定する"
        ],
        "answer": [
            "キャパシティモードを「オンデマンド（On-Demand）」に設定し、負荷テストで急激なトラフィック増加に対してもスロットリング（Throttling）が発生せずにオートスケールすることを確認する"
        ],
        "explanation": "【解説】\n予測不能なスパイクアクセスには「オンデマンドモード」が最適です。事前の容量設計が不要で、リクエスト数に応じて即座に対応（課金）されます。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol138.json)
q2_fin = [
    {
        "id": "Q2-FIN-V138-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】振込手数料の負担区分（内引き/上乗せ）。\n企業向けインターネットバンキング（FB）で、請求書払いを行う際の振込手数料の計算ロジックをテストしたい。\n「手数料・先方負担（受取人負担）」を選択して10,000円を振り込む場合、システムが生成すべき正しい入出金データはどれか。（手数料は550円とする）",
        "options": [
            "出金口座からは「10,000円」が引き落とされ、受取人には手数料を差し引いた「9,450円」が入金される（内引き）",
            "出金口座からは「10,550円」が引き落とされ、受取人には「10,000円」が入金される（上乗せ）",
            "出金口座からは「10,000円」が引き落とされ、受取人にも「10,000円」が入金され、手数料は銀行が負担する",
            "出金口座からは「9,450円」が引き落とされ、受取人には「10,550円」が入金される"
        ],
        "answer": [
            "出金口座からは「10,000円」が引き落とされ、受取人には手数料を差し引いた「9,450円」が入金される（内引き）"
        ],
        "explanation": "【解説】\n「先方負担（受取人負担）」の場合、振込依頼金額から手数料を差し引いて送金する「内引き」方式が一般的です。逆に「当方負担（振込人負担）」なら、手数料を別途支払う「上乗せ」になります。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol138.json": q3_gen,
    "ch1_general_vol138.json": q1_gen,
    "ch2_general_vol138.json": q2_gen,
    "ch1_aws_vol138.json": q1_aws,
    "ch2_finance_vol138.json": q2_fin
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
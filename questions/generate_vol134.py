import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.134 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol134.json)
q3_gen = [
    {
        "id": "Q3-GEN-V134-01",
        "chapter": "第3章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】信頼度成長曲線（バグ曲線）の解釈。\nシステムテスト終盤において、累積バグ発見数の曲線（ゴンペルツ曲線やロジスティック曲線）が「飽和状態（寝てきた状態）」となり、新規バグがほとんど発見されなくなった。\nこの現象に対するテストマネージャの判断として、最も適切かつ慎重なものはどれか。",
        "options": [
            "バグが出なくなったことは品質が安定した証拠であるため、直ちにテストを終了してリリース判定会議を開催する",
            "テストケースが枯渇して単にバグを見つけられなくなった可能性（テストの弱体化）と、実際にバグが減った可能性の両方を疑い、未実行のパスがないかや探索的テストの追加を検討する",
            "バグが出ないのはテスターのモチベーション低下が原因であると断定し、バグ発見数に応じた報奨金を出して競争させる",
            "統計学的にまだバグが潜んでいるはずであるため、バグが出るまで無意味なランダム入力を繰り返すよう指示する"
        ],
        "answer": [
            "テストケースが枯渇して単にバグを見つけられなくなった可能性（テストの弱体化）と、実際にバグが減った可能性の両方を疑い、未実行のパスがないかや探索的テストの追加を検討する"
        ],
        "explanation": "【解説】\nバグ曲線の飽和は「品質向上」と「テストの限界（マンネリ化）」の二つの意味を持ちます。安易に終了せず、視点を変えたテスト（探索的テストなど）を行って本当にバグがないか確認するのが定石です。",
        "tags": ["第3章", "一般", "シナリオ", "K4"]
    }
]

# 2. 第1章 一般 (ch1_general_vol134.json)
q1_gen = [
    {
        "id": "Q1-GEN-V134-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ペア探索的テスト（Pair Exploratory Testing）。\n複雑な業務ロジックを持つ機能のテストにおいて、ドメイン知識を持つ「業務担当者」と、テスト技術を持つ「テストエンジニア」がペアを組んで探索的テストを行うことになった。\nこのペアテストの効果を最大化するための役割分担はどれか。",
        "options": [
            "二人ともそれぞれ別のPCで黙々とテストを行い、終了後にバグリストを突き合わせて重複を削除する",
            "一人がキーボードを操作する「ドライバー」となり、もう一人が観察・記録・次のテスト提案を行う「ナビゲーター」となって、対話しながらテストを進める",
            "業務担当者がテストを行い、テストエンジニアは後ろで見ているだけで、一切口出しをせずに評価のみを行う",
            "テストエンジニアが操作を行い、業務担当者はマニュアルを読み上げて操作手順を指示するだけに留める"
        ],
        "answer": [
            "一人がキーボードを操作する「ドライバー」となり、もう一人が観察・記録・次のテスト提案を行う「ナビゲーター」となって、対話しながらテストを進める"
        ],
        "explanation": "【解説】\nペアプログラミングと同様、ペアテストも「ドライバー（操作）」と「ナビゲーター（思考・記録）」に分かれて対話することで、一人では気づけない洞察やバグを発見できます。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol134.json)
q2_gen = [
    {
        "id": "Q2-GEN-V134-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】状態遷移テストの「ガード条件（Guard Condition）」。\n「申込」ボタンを押すと「確認」画面に遷移するが、もし「年齢が18歳未満」である場合は遷移せずにエラーメッセージを表示する、という仕様がある。\nこの「年齢が18歳未満」という条件を状態遷移図や遷移表で扱う際の正しい名称とテスト方針はどれか。",
        "options": [
            "これは「ガード条件（Guard Condition）」であり、イベント（ボタン押下）が発生してもガード条件が偽（False）であれば遷移しないことを検証するテストケースが必要である",
            "これは「遷移アクション（Action）」であり、遷移した後に実行される処理として記述し、遷移自体は常に成功するものとしてテストする",
            "これは「不正イベント」であり、状態遷移テストの対象外となるため、単体テストでのみ確認すればよい",
            "これは「N/A（Not Applicable）」であり、物理的に発生しない組み合わせとしてテストケースから除外する"
        ],
        "answer": [
            "これは「ガード条件（Guard Condition）」であり、イベント（ボタン押下）が発生してもガード条件が偽（False）であれば遷移しないことを検証するテストケースが必要である"
        ],
        "explanation": "【解説】\n遷移をブロックする条件を「ガード条件」と呼びます。状態遷移テストでは、同じイベントでもガード条件の真偽によって遷移するか/しないかが分岐するため、両方のケースをテストします。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol134.json)
q1_aws = [
    {
        "id": "Q1-AWS-V134-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】プライベートサブネットからのS3アクセス（コスト最適化）。\nプライベートサブネットにある大量のEC2インスタンスから、S3にあるパッチファイルをダウンロードしたい。\nインターネットゲートウェイ（IGW）は無く、NAT Gatewayのデータ転送コストを回避したい場合、最も適切なネットワーク構成はどれか。",
        "options": [
            "S3用の「VPCエンドポイント（ゲートウェイ型）」を作成し、プライベートサブネットのルートテーブルにS3へのルートを追加する",
            "S3用の「VPCエンドポイント（インターフェース型 / PrivateLink）」を作成し、各AZにENIを配置して時間課金を受け入れる",
            "EC2インスタンスにパブリックIPを付与し、一時的にインターネット経由でS3にアクセスさせる",
            "S3バケットをVPC内部に移動させることで、ローカル通信として処理する"
        ],
        "answer": [
            "S3用の「VPCエンドポイント（ゲートウェイ型）」を作成し、プライベートサブネットのルートテーブルにS3へのルートを追加する"
        ],
        "explanation": "【解説】\nS3とDynamoDBへのアクセスには、無料で使用できる「ゲートウェイ型（Gateway Type）」のVPCエンドポイントが最適です。NAT Gatewayを経由しないため、コスト削減とセキュリティ向上になります。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol134.json)
q2_fin = [
    {
        "id": "Q2-FIN-V134-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】株式売買の「価格優先・時間優先」原則。\n証券取引所の売買システム（マッチングエンジン）のテストにおいて、以下の買い注文が出された場合の約定（やくじょう）順序を検証したい。\n注文A：指値1000円（10:00発注）\n注文B：指値1005円（10:01発注）\n注文C：成行（10:02発注）\n売り注文が出た際、優先的に約定する順序として正しいものはどれか。",
        "options": [
            "注文C（成行） → 注文B（高い指値） → 注文A（安い指値）の順で約定する",
            "注文A（一番早い） → 注文B（次に早い） → 注文C（一番遅い）の順で約定する",
            "注文B（価格が高い） → 注文A（価格が安い） → 注文C（価格指定なし）の順で約定する",
            "すべての注文が同時に約定し、按分比例（プロラタ）で配分される"
        ],
        "answer": [
            "注文C（成行） → 注文B（高い指値） → 注文A（安い指値）の順で約定する"
        ],
        "explanation": "【解説】\n競争売買の原則は「価格優先」＞「時間優先」です。買い注文の場合、「成行（価格指定なし＝最強）」＞「高い指値」＞「安い指値」の順に優先されます。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol134.json": q3_gen,
    "ch1_general_vol134.json": q1_gen,
    "ch2_general_vol134.json": q2_gen,
    "ch1_aws_vol134.json": q1_aws,
    "ch2_finance_vol134.json": q2_fin
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
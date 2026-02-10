import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.139 新規問題データ定義（Final Batch）
# ==========================================

# 1. 第3章 一般 (ch3_general_vol139.json)
q3_gen = [
    {
        "id": "Q3-GEN-V139-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】リリース直前のバグ・トリアージ。\n本番リリース前日の最終テストにおいて、機能動作には影響しないごく軽微な表示崩れ（重要度：低）が見つかった。\nこのバグを修正すると、関連するモジュールの再ビルドが必要となり、リグレッションテストが間に合わないリスクがある。\nテストマネージャとして下すべき判断はどれか。",
        "options": [
            "品質に妥協は許されないため、徹夜してでも修正を行い、テストが間に合わなければリリース日を延期する",
            "修正による二次被害（デグレ）のリスクの方が高いため、今回は修正を見送り、「既知の不具合」としてリリースノートに記載してリリースする",
            "顧客にバレなければ問題ないため、バグ管理システムから当該チケットを削除し、なかったことにしてリリースする",
            "開発者個人の判断に任せ、もし修正パッチが提出されたら、テストなしで本番環境に適用する"
        ],
        "answer": [
            "修正による二次被害（デグレ）のリスクの方が高いため、今回は修正を見送り、「既知の不具合」としてリリースノートに記載してリリースする"
        ],
        "explanation": "【解説】\nリリース直前では「修正することのリスク（回帰テスト不足）」と「バグの影響度」を天秤にかけます。軽微なバグであれば、Defer（先送り）として扱い、リスクを回避するのが定石です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol139.json)
q1_gen = [
    {
        "id": "Q1-GEN-V139-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】探索的テストとアドホックテストの違い。\nテスト計画書において「探索的テスト（Exploratory Testing）」を実施すると定義したが、ステークホルダーから「単なるアドホックテスト（適当なモンキーテスト）と同じではないか」と指摘された。\n探索的テストの専門性を説明する回答として、最も適切なものはどれか。",
        "options": [
            "探索的テストは、テスターがテストの「学習」「設計」「実行」を同時に行い、得られた洞察に基づいて次に実施すべきテストを動的に最適化していく知的プロセスである",
            "探索的テストは、ドキュメントを書くのが苦手なテスターのために考案された手法であり、記録を残さずに自由に操作することに主眼を置いている",
            "アドホックテストは開発者が行うものであり、探索的テストはQAチームが行うものであるという担当者の違いだけである",
            "探索的テストはAIツールが自動的に行うランダムテストのことであり、人間が介入する余地はない"
        ],
        "answer": [
            "探索的テストは、テスターがテストの「学習」「設計」「実行」を同時に行い、得られた洞察に基づいて次に実施すべきテストを動的に最適化していく知的プロセスである"
        ],
        "explanation": "【解説】\n探索的テストは決して「適当」ではありません。テストチャーターやヒューリスティクスに基づき、実行結果からリアルタイムにシステムを学習し、次のテストを設計する高度な技法です。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol139.json)
q2_gen = [
    {
        "id": "Q2-GEN-V139-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】デシジョンカバレッジ（判定条件網羅）。\nプログラム内に `IF (A > 0 OR B > 0)` という条件分岐がある。\nこの分岐に対して「デシジョンカバレッジ（C1）」を100%にするために必要なテストデータの最小セットはどれか。",
        "options": [
            "A=1, B=0 のケース（判定結果：True）のみを実行する",
            "A=1, B=1 のケース（判定結果：True）と、A=0, B=0 のケース（判定結果：False）の2つを実行する",
            "A=1, B=0（True）、A=0, B=1（True）、A=0, B=0（False）の3つのケースを実行して、OR条件の全組み合わせを確認する",
            "ソースコードの全行を実行できればよいため、A=1, B=1 のケースだけで十分である"
        ],
        "answer": [
            "A=1, B=1 のケース（判定結果：True）と、A=0, B=0 のケース（判定結果：False）の2つを実行する"
        ],
        "explanation": "【解説】\nデシジョンカバレッジ（判定条件網羅）の要件は、分岐全体の判定結果が「真（True）」になるケースと「偽（False）」になるケースを少なくとも1回ずつ通すことです。内部条件（AやB単体）の組み合わせまでは問いません。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol139.json)
q1_aws = [
    {
        "id": "Q1-AWS-V139-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】S3のサーバーサイド暗号化と監査。\n機密データをS3に保存する際、暗号化が必須要件となっている。さらに、監査要件として「いつ、誰が、どの鍵を使ってデータを復号したか」をCloudTrailログで追跡できる必要がある。\nこの要件を満たす暗号化方式はどれか。",
        "options": [
            "Amazon S3 マネージドキーによるサーバーサイド暗号化（SSE-S3）",
            "AWS KMS キーによるサーバーサイド暗号化（SSE-KMS）",
            "お客様提供のキーによるサーバーサイド暗号化（SSE-C）",
            "クライアントサイド暗号化（データをアップロードする前にPC上で暗号化する）"
        ],
        "answer": [
            "AWS KMS キーによるサーバーサイド暗号化（SSE-KMS）"
        ],
        "explanation": "【解説】\nSSE-S3はS3がキーを自動管理するため、キーの使用履歴（誰が復号したか）はログに残りません。SSE-KMSを使用することで、KMSへのAPIコールがCloudTrailに記録され、監査が可能になります。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol139.json)
q2_fin = [
    {
        "id": "Q2-FIN-V139-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】株式分割（Stock Split）のポートフォリオ評価。\n保有している銘柄Aについて、「1株を2株に分割する」というコーポレートアクションが実施された。\n権利落ち日以降のポートフォリオ画面において、正しく更新されているべき保有数量と評価額の状態はどれか。",
        "options": [
            "保有数量が2倍になり、株価も2倍になるため、評価額が分割前の4倍に増えていること",
            "保有数量は変わらず、株価が半分になるため、評価額が分割前の半分に減っていること",
            "保有数量が2倍になり、株価が理論上半分になるため、トータルの評価額は分割前と（市場変動を除き）ほぼ変わらないこと",
            "保有数量が半分になり、株価が2倍になる（株式併合と同じ挙動になる）こと"
        ],
        "answer": [
            "保有数量が2倍になり、株価が理論上半分になるため、トータルの評価額は分割前と（市場変動を除き）ほぼ変わらないこと"
        ],
        "explanation": "【解説】\n株式分割（1:2）が行われると、株数は2倍になりますが、1株あたりの価値は半分になります。結果として資産総額（時価総額）は変わりません。システムテストではこの「数量増・単価減・総額維持」を確認します。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol139.json": q3_gen,
    "ch1_general_vol139.json": q1_gen,
    "ch2_general_vol139.json": q2_gen,
    "ch1_aws_vol139.json": q1_aws,
    "ch2_finance_vol139.json": q2_fin
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
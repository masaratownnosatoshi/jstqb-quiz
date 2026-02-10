import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.140 新規問題データ定義（The Final Batch）
# ==========================================

# 1. 第3章 一般 (ch3_general_vol140.json)
q3_gen = [
    {
        "id": "Q3-GEN-V140-01",
        "chapter": "第3章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】TMMi（Test Maturity Model integration）の段階的表現。\n組織のテストプロセス成熟度をTMMiで評価している。現在「レベル2（管理された）」であるが、次の「レベル3（定義された）」へ昇格するために、組織として確立しなければならない体制はどれか。",
        "options": [
            "個々のプロジェクトでテスト計画が策定され、基本的なテスト管理が行われている状態から脱却し、組織標準のテストプロセスが定義され、全組織的に展開・制度化されている",
            "テストツールによる自動化率が80%を超え、すべてのテスト実行が夜間バッチで無人化されている",
            "テストチームが開発チームから完全に独立し、品質保証部門（QA）として経営層直轄の組織になっている",
            "欠陥の予防（Defect Prevention）プロセスが確立され、統計的な手法を用いてプロセスパフォーマンスが予測可能になっている"
        ],
        "answer": [
            "個々のプロジェクトでテスト計画が策定され、基本的なテスト管理が行われている状態から脱却し、組織標準のテストプロセスが定義され、全組織的に展開・制度化されている"
        ],
        "explanation": "【解説】\nTMMiレベル2は「プロジェクトごとの管理」ができている状態です。レベル3（定義された）になるには、「組織標準プロセス」の確立と、その全社的な適用（制度化）が必須要件となります。",
        "tags": ["第3章", "一般", "シナリオ", "K4"]
    }
]

# 2. 第1章 一般 (ch1_general_vol140.json)
q1_gen = [
    {
        "id": "Q1-GEN-V140-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テスト自動化アーキテクチャ（TAA）の階層化。\nテスト自動化スクリプトの保守性を高めるために、TAAを設計している。\nUIの変更（IDやXPathの変更）がテストスクリプト全体に波及するのを防ぐために導入すべき、最も代表的なデザインパターンはどれか。",
        "options": [
            "Page Object Model (POM)：各画面（ページ）をオブジェクトとして定義し、画面要素の操作や取得処理をそのクラス内にカプセル化して、テストシナリオからはメソッドを呼び出すだけに留める",
            "Record & Playback：操作をそのまま記録し、生成されたコードを一切編集せずに再生専用として扱うことで、変更時は再録画で対応する",
            "Keyword Driven Testing：すべての操作を「クリック」「入力」といったキーワードで定義し、Excelシート上でテストケースを管理する",
            "Data Driven Testing：テストデータのみを外部ファイルに分離し、ロジックは画面操作コードの中に直接記述する"
        ],
        "answer": [
            "Page Object Model (POM)：各画面（ページ）をオブジェクトとして定義し、画面要素の操作や取得処理をそのクラス内にカプセル化して、テストシナリオからはメソッドを呼び出すだけに留める"
        ],
        "explanation": "【解説】\nUI変更に強い自動化の定石は「Page Object Model（POM）」です。画面操作の詳細（ロケータなど）をページクラスに隠蔽することで、UI変更時の修正箇所を局所化できます。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol140.json)
q2_gen = [
    {
        "id": "Q2-GEN-V140-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ユーザビリティテストの思考発話法（Think Aloud）。\n初めて自社アプリを使うユーザーにタスクを実行してもらい、ユーザビリティ上の問題点を発見したい。\n被験者の思考プロセスをリアルタイムで把握するために、テスト実施中に依頼すべきことはどれか。",
        "options": [
            "「今、何を見ているか」「何をしようとしているか」「何を感じたか」を、独り言のように常に声に出しながら操作してもらう",
            "操作中は集中してもらうために一切発言させず、終了後にまとめてインタビューを行って、思い出してもらいながら感想を聞く",
            "被験者の隣に開発者が座り、操作に迷っている様子が見られたら、すぐに正しい操作方法を教えてあげる",
            "操作画面の録画だけを行い、視線の動き（アイトラッキング）のデータのみを分析対象として、発言内容は無視する"
        ],
        "answer": [
            "「今、何を見ているか」「何をしようとしているか」「何を感じたか」を、独り言のように常に声に出しながら操作してもらう"
        ],
        "explanation": "【解説】\n思考発話法（Think Aloud Protocol）は、ユーザーの「頭の中」を可視化する手法です。操作後のインタビューでは忘れてしまう微細な違和感や迷いを、リアルタイムに捉えることができます。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol140.json)
q1_aws = [
    {
        "id": "Q1-AWS-V140-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】カオスエンジニアリング（AWS FIS）。\n本番環境におけるシステムの耐障害性を検証するために、意図的に障害（EC2の停止や遅延発生など）を注入する実験を行いたい。\nAWSが提供するフルマネージドのカオスエンジニアリングサービスはどれか。",
        "options": [
            "AWS Fault Injection Service (FIS)",
            "AWS Chaos Monkey Manager",
            "Amazon Inspector Agent",
            "AWS X-Ray"
        ],
        "answer": [
            "AWS Fault Injection Service (FIS)"
        ],
        "explanation": "【解説】\nAWS FISは、AWS上でカオスエンジニアリング（障害注入実験）を安全かつ管理された状態で実施するためのフルマネージドサービスです。本番相当の環境で「壊れても復旧できるか」を検証します。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol140.json)
q2_fin = [
    {
        "id": "Q2-FIN-V140-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】マイナス金利（Negative Interest Rate）のシステム対応。\n中央銀行の政策により市場金利がマイナスになった場合、変動金利型のローンや預金システムにおいて発生しうるリスクと、検証すべき挙動はどれか。",
        "options": [
            "計算結果の利息がマイナス（顧客が利息を支払うのではなく受け取る、またはその逆）になった場合でも、システムがクラッシュせず、仕様通り（例：0%でフロア設定、あるいはマイナス利息として元本減額）に処理されること",
            "マイナス金利はプログラム上エラー（例外）として処理されるべきであるため、計算時にシステムエラー画面が表示され、オペレーターに通知が飛ぶこと",
            "金利入力フィールドにマイナス記号（-）が入力できないように入力制限（バリデーション）をかけ、マイナス金利の存在自体をシステムから排除すること",
            "絶対値関数（ABS）を使用してマイナスを自動的にプラスに変換し、通常の金利として計算を続行すること"
        ],
        "answer": [
            "計算結果の利息がマイナス（顧客が利息を支払うのではなく受け取る、またはその逆）になった場合でも、システムがクラッシュせず、仕様通り（例：0%でフロア設定、あるいはマイナス利息として元本減額）に処理されること"
        ],
        "explanation": "【解説】\nレガシーな金融システムでは「金利＝プラス」が前提となっていることが多く、マイナス金利導入時に計算ロジックが破綻するリスクがあります。0%フロア（下限）が効くか、マイナスを許容するか、仕様に沿った挙動確認が必須です。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol140.json": q3_gen,
    "ch1_general_vol140.json": q1_gen,
    "ch2_general_vol140.json": q2_gen,
    "ch1_aws_vol140.json": q1_aws,
    "ch2_finance_vol140.json": q2_fin
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
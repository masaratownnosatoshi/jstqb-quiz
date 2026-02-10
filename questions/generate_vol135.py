import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.135 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol135.json)
q3_gen = [
    {
        "id": "Q3-GEN-V135-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】インシデント管理と優先度付け。\nリリース直前のテストで複数のバグが見つかったが、修正に使える時間は限られている。\nテストマネージャが開発チームに対して、修正すべきバグの優先順位を指示する際の基準として、最もビジネスリスクを考慮したものはどれか。",
        "options": [
            "修正が簡単で時間がかからない「軽微なバグ」から順に修正させ、修正完了したチケットの枚数を稼ぐことで進捗を良く見せる",
            "「重要度（Severity）」が高く、かつ「発生優先度（Priority）」も高い、ビジネスへの影響が致命的で回避策がないバグを最優先とする",
            "テスト担当者が個人的に気に入らないと感じたバグを優先し、UIのデザイン調整などの見た目の修正に注力させる",
            "発見された順序（古い順）に修正させ、FIFO（先入れ先出し）の原則を厳守する"
        ],
        "answer": [
            "「重要度（Severity）」が高く、かつ「発生優先度（Priority）」も高い、ビジネスへの影響が致命的で回避策がないバグを最優先とする"
        ],
        "explanation": "【解説】\n限られた時間の中では、ビジネスリスク（重要度×優先度）に基づいてトリアージを行うのが鉄則です。修正数や発見順はビジネス価値とは無関係です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol135.json)
q1_gen = [
    {
        "id": "Q1-GEN-V135-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】セキュリティテスト（SQLインジェクション）。\nWebアプリケーションのログイン画面に対して、SQLインジェクション脆弱性がないかを確認したい。\nブラックボックステストのアプローチとして、入力フォームに対して試行すべき具体的なテストデータはどれか。",
        "options": [
            "「admin」や「user」といった一般的なユーザーIDを入力し、ログインが成功することを確認する",
            "「' OR '1'='1」や「\"; DROP TABLE users; --」といったSQLの構文を含む文字列を入力し、認証回避やエラー発生、データの破壊が起きないかを確認する",
            "1万文字以上の非常に長いランダムな文字列を入力し、バッファオーバーフローが発生してサーバーがダウンしないかを確認する",
            "HTMLタグ（<script>alert(1)</script>など）を入力し、ポップアップが表示されるかを確認する"
        ],
        "answer": [
            "「' OR '1'='1」や「\"; DROP TABLE users; --」といったSQLの構文を含む文字列を入力し、認証回避やエラー発生、データの破壊が起きないかを確認する"
        ],
        "explanation": "【解説】\nSQLインジェクションのテストでは、SQL文を不正に成立させるためのメタ文字（シングルクォート等）を含むパターンを入力します。HTMLタグはXSS、長文はBoFのテストです。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol135.json)
q2_gen = [
    {
        "id": "Q2-GEN-V135-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】デシジョンテーブルテストの作成。\n「会員ランク（ゴールド/一般）」と「購入金額（1万円以上/未満）」によって、「送料無料」か「送料有料」かが決まる仕様がある。\nこの仕様の抜け漏れを防ぐためにデシジョンテーブルを作成する場合、最小限網羅すべきルールの数はいくつか（圧縮前）。",
        "options": [
            "2つの条件（ランク、金額）があるため、2つのルール（2通り）を作成すれば十分である",
            "2つの条件がそれぞれ2つの値（True/False）を取り得るため、2の2乗で合計4つのルール（組み合わせ）を作成し、それぞれの期待結果を定義する",
            "境界値分析を行う必要があるため、1万円、9999円、10001円の3つのケースを作成する",
            "正常系（送料無料）と異常系（送料有料）の2パターンを作成する"
        ],
        "answer": [
            "2つの条件がそれぞれ2つの値（True/False）を取り得るため、2の2乗で合計4つのルール（組み合わせ）を作成し、それぞれの期待結果を定義する"
        ],
        "explanation": "【解説】\nデシジョンテーブルの基本は「全条件の組み合わせ網羅」です。2条件×2値＝4ルールを作成することで、論理的な漏れをなくします。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol135.json)
q1_aws = [
    {
        "id": "Q1-AWS-V135-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】S3オブジェクトの一時的な公開。\nS3バケット内のプライベートなファイルを、特定のユーザーに対して10分間だけダウンロード可能にしたい。\nバケットポリシーを変更せずに、安全かつ期限付きでアクセスを許可する方法はどれか。",
        "options": [
            "対象のオブジェクトを一時的に「パブリック公開」設定に変更し、10分後に手動で元に戻す",
            "IAMユーザーを作成してアクセスキーを発行し、そのキーをユーザーに渡して、10分後にユーザーごと削除する",
            "AWS CLIまたはSDKを使用して「署名付きURL（Presigned URL）」を発行し、有効期限を600秒（10分）に設定して、そのURLをユーザーに共有する",
            "S3のウェブサイトホスティング機能を有効にし、HTMLファイルの中にダウンロードリンクを埋め込んで公開する"
        ],
        "answer": [
            "AWS CLIまたはSDKを使用して「署名付きURL（Presigned URL）」を発行し、有効期限を600秒（10分）に設定して、そのURLをユーザーに共有する"
        ],
        "explanation": "【解説】\n期限付きアクセスの標準機能は「署名付きURL（Presigned URL）」です。バケット自体はプライベートのまま、URLを知っている人だけが指定期間アクセス可能になります。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol135.json)
q2_fin = [
    {
        "id": "Q2-FIN-V135-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】外貨両替の適用レート（TTS vs TTB）。\n銀行の窓口システムにおいて、顧客が「日本円の現金」を渡して「米ドルの現金」を受け取る（円→ドル）取引をテストしたい。\nシステムが適用すべき為替レートの種類として、正しいものはどれか。",
        "options": [
            "銀行が顧客からドルを買い取る取引であるため、「TTB（Telegraphic Transfer Buying）」レートが適用されることを確認する",
            "銀行が顧客に対してドルを売る取引であるため、「TTS（Telegraphic Transfer Selling）」レートが適用されることを確認する",
            "現金のやり取りがない仲値取引とみなされるため、「TTM（Telegraphic Transfer Middle）」レートが適用されることを確認する",
            "顧客にとって有利になるように、市場レートよりも低い固定レートが適用されることを確認する"
        ],
        "answer": [
            "銀行が顧客に対してドルを売る取引であるため、「TTS（Telegraphic Transfer Selling）」レートが適用されることを確認する"
        ],
        "explanation": "【解説】\n為替レートは「銀行視点」で決まります。顧客が円→ドルにする場合、銀行はドルを「売る（Sell）」ことになるため、TTSレートが適用されます。（厳密には現金ならCash Sellingですが、選択肢の中ではTTSが正解です）",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol135.json": q3_gen,
    "ch1_general_vol135.json": q1_gen,
    "ch2_general_vol135.json": q2_gen,
    "ch1_aws_vol135.json": q1_aws,
    "ch2_finance_vol135.json": q2_fin
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
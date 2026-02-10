import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.132 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol132.json)
q3_gen = [
    {
        "id": "Q3-GEN-V132-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストポリシーの策定。\n組織全体で統一的なテストの方針（テストポリシー）を策定することになった。\nテストポリシーが形骸化せず、実際のプロジェクトで有効に機能するために、記述すべき内容として最も適切なものはどれか。",
        "options": [
            "テストツールの詳細な操作マニュアルや、バグ管理システムの入力項目の定義といった、日々の作業手順を網羅的に記述する",
            "「テストとは何か」という哲学的な定義から始め、組織のビジネスゴールとテストの目的（品質保証、コスト削減など）をどのように結びつけるかを高レベルで記述する",
            "過去のプロジェクトで発生した全てのバグリストと、その個別の再発防止策を羅列し、同じミスを繰り返さないためのデータベースとして記述する",
            "特定のプロジェクト（例：次期基幹システム）専用のスケジュールと要員計画を記述し、そのプロジェクトが終わったら破棄する前提で作成する"
        ],
        "answer": [
            "「テストとは何か」という哲学的な定義から始め、組織のビジネスゴールとテストの目的（品質保証、コスト削減など）をどのように結びつけるかを高レベルで記述する"
        ],
        "explanation": "【解説】\nテストポリシーは、組織全体の「テストに対する価値観や目的」を定義する最上位文書です。具体的な手順（プロセス）や個別計画（プラン）ではなく、ビジネスゴールとの整合性が重要です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol132.json)
q1_gen = [
    {
        "id": "Q1-GEN-V132-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ウォークスルー（Walkthrough）の実施。\n新人の開発者が作成した詳細設計書について、知識共有と欠陥の早期発見を目的としたレビューを行いたい。\n公式なインスペクションを行うほどのリソースはないため、「ウォークスルー」形式を採用する場合の正しい進め方はどれか。",
        "options": [
            "作成者（Author）自身が進行役となり、参加者に対してドキュメントの内容を読み上げたり説明したりしながら、フィードバックや質問を募る",
            "モデレーター（第三者）が進行を管理し、作成者は一切発言せずに、参加者からの指摘をひたすら記録することに集中する",
            "参加者は事前にドキュメントを読み込んでおく必要はなく、会議の場では作成者の説明を聞くだけで、特に意見を出さずに終了する",
            "管理者が欠陥の数をカウントし、作成者の人事評価（減点）を行うための場として利用する"
        ],
        "answer": [
            "作成者（Author）自身が進行役となり、参加者に対してドキュメントの内容を読み上げたり説明したりしながら、フィードバックや質問を募る"
        ],
        "explanation": "【解説】\nウォークスルーの特徴は「作成者が主導する」点にあります。教育や知識共有、共通理解の形成（Buy-in）が主な目的であり、インスペクションよりもカジュアルな形式です。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol132.json)
q2_gen = [
    {
        "id": "Q2-GEN-V132-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】ドメイン分析テスト（変数間の相互作用）。\n「合計金額が1万円以上なら送料（500円）が無料になる」という仕様を持つECサイトのテスト。\n単一の境界値（9999円と10000円）だけでなく、複数の変数が連動する挙動を確認するためのテストケースとして、最も適切なものはどれか。",
        "options": [
            "商品A（5000円）と商品B（5000円）をカートに入れ、小計が10000円になった時点で送料が0円になり、その後クーポンで100円引き（支払額9900円）になっても送料は0円のままであるかを確認する",
            "商品単価として「-100円」や「文字」を入力し、エラーチェックが正しく機能するかを確認する",
            "送料が無料になるまで商品を1円ずつ追加していき、10000回カート投入操作を行ってシステムの耐久性を確認する",
            "ブラウザの言語設定を英語に変更し、通貨記号が「円」から「ドル」に変わるかどうかだけを確認する"
        ],
        "answer": [
            "商品A（5000円）と商品B（5000円）をカートに入れ、小計が10000円になった時点で送料が0円になり、その後クーポンで100円引き（支払額9900円）になっても送料は0円のままであるかを確認する"
        ],
        "explanation": "【解説】\nドメイン分析では、変数の相互作用（小計、割引、送料判定の順序など）を検証します。「判定基準額」と「最終支払額」が異なるケースなどは、バグの温床となりやすいポイントです。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol132.json)
q1_aws = [
    {
        "id": "Q1-AWS-V132-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ALBのスティッキーセッション（Sticky Sessions）。\nステートフルなWebアプリケーション（セッション情報をサーバーのメモリに保存するタイプ）を、ALB（Application Load Balancer）配下の複数台のEC2で運用することになった。\nユーザーがログイン後に勝手にログアウトされてしまう問題を防ぐ設定と、その検証方法はどれか。",
        "options": [
            "ALBのターゲットグループ設定で「スティッキーセッション（維持設定）」を有効にし、同一クライアントからのリクエストが継続して同じインスタンスにルーティングされることを、Cookieの確認やアクセスログで検証する",
            "各EC2インスタンスにElastic IPを付与し、DNSラウンドロビンで負荷分散を行うことで、ユーザーがIPアドレスを直接指定してアクセスできるようにする",
            "ALBを廃止し、CloudFrontのみでリクエストを処理することで、セッション情報をキャッシュさせる",
            "アプリケーション側でセッションタイムアウト時間を「無制限」に設定し、サーバーが変わってもセッションが切れないようにする"
        ],
        "answer": [
            "ALBのターゲットグループ設定で「スティッキーセッション（維持設定）」を有効にし、同一クライアントからのリクエストが継続して同じインスタンスにルーティングされることを、Cookieの確認やアクセスログで検証する"
        ],
        "explanation": "【解説】\nサーバーローカルにセッションを持つ場合、ALBのスティッキーセッション（Cookieベースの固定化）が必須です。これが機能していないと、リクエストごとに別サーバーに飛び、セッション切れ（ログアウト）が発生します。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol132.json)
q2_fin = [
    {
        "id": "Q2-FIN-V132-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】AML（アンチマネーロンダリング）のネームスクリーニング。\n海外送金システムにおいて、受取人名が「制裁対象者リスト（Sanctions List）」に含まれていないかをチェックする機能をテストしたい。\n単純な完全一致だけでなく、実効性のあるスクリーニング機能を検証するためのテストデータはどれか。",
        "options": [
            "リストに登録されている名前と一字一句違わない完全一致のデータのみを用意し、正しく検知されることを確認する",
            "「Osama Bin Laden」に対して「Usama Bin Ladin」のようなスペル揺れ（Fuzzy Match）や、名前の一部欠落、ミドルネームの有無などを含むデータを用意し、あいまい検索でも検知されることを確認する",
            "制裁リストには存在しない「John Smith」のような一般的な名前を大量に入力し、誤検知（False Positive）が一件も発生しないことを確認する",
            "送金金額が1億円以上の場合のみチェックが行われる仕様であると仮定し、金額条件の境界値テストのみを行う"
        ],
        "answer": [
            "「Osama Bin Laden」に対して「Usama Bin Ladin」のようなスペル揺れ（Fuzzy Match）や、名前の一部欠落、ミドルネームの有無などを含むデータを用意し、あいまい検索でも検知されることを確認する"
        ],
        "explanation": "【解説】\nAMLのネームスクリーニング（フィルタリング）では、意図的なスペル変えやアルファベットの転写揺れを見抜く「あいまい検索（Fuzzy Matching）」の精度検証が最も重要です。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol132.json": q3_gen,
    "ch1_general_vol132.json": q1_gen,
    "ch2_general_vol132.json": q2_gen,
    "ch1_aws_vol132.json": q1_aws,
    "ch2_finance_vol132.json": q2_fin
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
import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.120 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol120.json)
q3_gen = [
    {
        "id": "Q3-GEN-V120-01",
        "chapter": "第3章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】欠陥密度（Defect Density）の解釈。\nあるモジュールのテスト結果において、欠陥密度（KLoCあたりのバグ数）が過去のプロジェクト平均よりも著しく高い値を示した。\nこの数値に対するテストマネージャの解釈として、最も冷静かつ多角的な視点はどれか。",
        "options": [
            "開発者のスキルが低いことが明白であるため、即座に担当者を交代させ、コードを最初から書き直すように指示する（単一の原因に決めつけている）",
            "数値が高いことは「品質が悪い」ことの証明であるため、リリース判定会議で不合格とし、品質が安定するまで無期限でテストを継続する（テストの有効性を無視している）",
            "数値が高いのは「テストが効果的に機能し、多くの潜在バグを除去できた」というポジティブな側面と、「モジュール自体の品質が低い」というネガティブな側面の両方の可能性があるため、バグの内容や複雑度を詳細分析する",
            "欠陥密度が高いと顧客への印象が悪くなるため、軽微なバグは報告書から削除し、平均値に近づくように数値を調整する（データの改ざん）"
        ],
        "answer": [
            "数値が高いのは「テストが効果的に機能し、多くの潜在バグを除去できた」というポジティブな側面と、「モジュール自体の品質が低い」というネガティブな側面の両方の可能性があるため、バグの内容や複雑度を詳細分析する"
        ],
        "explanation": "【解説】\n欠陥密度が高いことは必ずしも悪いことではありません。「バグを出し切った（テストが優秀）」可能性もあります。単純な数値の大小ではなく、中身の分析が必要です。",
        "tags": ["第3章", "一般", "シナリオ", "K4"]
    }
]

# 2. 第1章 一般 (ch1_general_vol120.json)
q1_gen = [
    {
        "id": "Q1-GEN-V120-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テスト自動化のピラミッド（Test Automation Pyramid）。\n開発チームが「E2Eテスト（UIテスト）ですべての回帰テストを自動化したい」と提案してきた。\n自動化アーキテクトとして、ピラミッドの原則に基づいてアドバイスすべき内容はどれか。",
        "options": [
            "UIテストはユーザーの操作を模倣するため最も信頼性が高い。したがって、ピラミッドを逆転させ、UIテストを最大量にする「アイスクリームコーン型」を目指すべきである（アンチパターンへの誘導）",
            "UIテストは実行が遅く壊れやすいため、ピラミッドの頂点（少数）に留め、ビジネスロジックやデータパターンの網羅は、高速で安定した「単体テスト」や「APIテスト（統合テスト）」の層で担保すべきである",
            "ピラミッドの形状は気にせず、手動テストの手順書をそのままRPAツールで録画・再生することが、最も手っ取り早くコスト効果が高い（メンテナンスコストが破綻する）",
            "最近のAI技術を使えばUIテストのメンテナンスフリー化が可能であるため、すべてのテストレベルを廃止し、AIによる自動探索テストのみに一本化する（過度な期待とリスク）"
        ],
        "answer": [
            "UIテストは実行が遅く壊れやすいため、ピラミッドの頂点（少数）に留め、ビジネスロジックやデータパターンの網羅は、高速で安定した「単体テスト」や「APIテスト（統合テスト）」の層で担保すべきである"
        ],
        "explanation": "【解説】\nテスト自動化の鉄則は「ピラミッド型」です。壊れやすいUIテスト（E2E）を最小限にし、堅牢なUnit/APIテストを基盤（大量）にします。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol120.json)
q2_gen = [
    {
        "id": "Q2-GEN-V120-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】非機能テスト（ロングランテスト/ソークテスト）。\nシステム稼働開始直後は問題ないが、3日以上連続稼働させると徐々にレスポンスが悪化し、最終的にOutOfMemoryでクラッシュする現象が報告された。\nこの問題を再現・検証するために実施すべきテストはどれか。",
        "options": [
            "短時間に大量のリクエストを送る「スパイクテスト」を実施し、CPU使用率が100%になった時の挙動を確認する（瞬発的な負荷試験であり、経時劣化は見れない）",
            "定常的な負荷をかけながら長期間（数日〜数週間）連続稼働させる「ソークテスト（耐久テスト）」を実施し、メモリリークやリソースの解放漏れがないかをモニタリングする",
            "システムの電源を頻繁にON/OFFする「リカバリテスト」を実施し、再起動後の復旧時間を計測する（長時間稼働の問題とは関係ない）",
            "データベースのレコード数を1億件にして検索速度を測る「ボリュームテスト」を実施し、インデックスが効いているかを確認する（データ量の問題ではなく、稼働時間の問題である）"
        ],
        "answer": [
            "定常的な負荷をかけながら長期間（数日〜数週間）連続稼働させる「ソークテスト（耐久テスト）」を実施し、メモリリークやリソースの解放漏れがないかをモニタリングする"
        ],
        "explanation": "【解説】\n時間の経過とともに発生する問題（メモリリーク等）を発見するには、長時間の「ソークテスト（Soak Testing）」または「耐久テスト（Endurance Testing）」が必要です。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol120.json)
q1_aws = [
    {
        "id": "Q1-AWS-V120-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】Amazon Cognitoの構成テスト。\nモバイルアプリにおいて、GoogleやFacebookのアカウントでサインイン（認証）し、そのユーザーに対してS3への一時的なアクセス権限（認可）を与えたい。\nCognitoの「ユーザープール」と「IDプール」の役割分担として、正しい構成検証の観点はどれか。",
        "options": [
            "ユーザープールのみを作成し、ユーザープールが直接AWSクレデンシャル（アクセスキー）を発行することを確認する（ユーザープールは認証機能であり、AWS権限発行は行わない）",
            "IDプールのみを作成し、IDプールの中にユーザーのパスワード情報を保存して、認証と認可を一本化する（IDプールはユーザーディレクトリ機能を持たない）",
            "ユーザープールで外部IdP（Google等）との連携と認証（トークン発行）を行い、そのトークンをIDプールに渡してAWSの一時クレデンシャル（IAMロール）を取得する流れを確認する",
            "Cognitoは使用せず、IAMユーザーのアクセスキーをモバイルアプリ内にハードコーディングして配布し、全員が同じ権限でアクセスすることを確認する（セキュリティのアンチパターン）"
        ],
        "answer": [
            "ユーザープールで外部IdP（Google等）との連携と認証（トークン発行）を行い、そのトークンをIDプールに渡してAWSの一時クレデンシャル（IAMロール）を取得する流れを確認する"
        ],
        "explanation": "【解説】\nCognitoの基本構成です。ユーザープールは「認証（Who are you?）」、IDプールは「認可（What can you do? / AWS Credentials）」を担当します。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol120.json)
q2_fin = [
    {
        "id": "Q2-FIN-V120-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】債券利回りの計算基準（Day Count Convention）。\n海外の債券システムにおいて、利息計算の結果が手計算と微妙に合わない。\n原因として「日数の数え方（Day Count Basis）」の違いが疑われる。\n検証すべき設定値の組み合わせとして、金融ドメインで一般的なものはどれか。",
        "options": [
            "サーバーのCPUクロック周波数の違いにより、時間の進み方が異なる可能性を検証する（物理時間のズレは利息計算式に関係ない）",
            "「30/360（1ヶ月を30日、1年を360日とみなす）」方式と、「Actual/365（実日数/365日）」や「Actual/Actual」方式のいずれが適用されているかを確認し、仕様書と一致しているか検証する",
            "うるう年を4年に1回ではなく、100年に1回にする設定が入っているかを確認する（グレゴリオ暦の基本であり、利回り計算方式の主要因ではない）",
            "金利計算は複雑すぎるため、システムが出した答えを正として受け入れ、誤差は「調整額」として雑損処理する運用ルールを策定する（計算ロジックのバグ放置）"
        ],
        "answer": [
            "「30/360（1ヶ月を30日、1年を360日とみなす）」方式と、「Actual/365（実日数/365日）」や「Actual/Actual」方式のいずれが適用されているかを確認し、仕様書と一致しているか検証する"
        ],
        "explanation": "【解説】\n金融計算（特に債券や金利スワップ）では、「日数の数え方（Day Count Convention）」が国や商品によって異なります。30/360やAct/365の取り違えは典型的なバグ原因です。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol120.json": q3_gen,
    "ch1_general_vol120.json": q1_gen,
    "ch2_general_vol120.json": q2_gen,
    "ch1_aws_vol120.json": q1_aws,
    "ch2_finance_vol120.json": q2_fin
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
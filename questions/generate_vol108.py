import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.108 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol108.json)
q3_gen = [
    {
        "id": "Q3-GEN-V108-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストプロセス成熟度モデル（TMMi）。\n組織は現在TMMiレベル2（管理された）の状態にある。\nレベル3（定義された）へとステップアップするために、組織全体として取り組むべき活動はどれか。",
        "options": [
            "すべてのプロジェクトで同じテストツールを強制的に使用し、ツールによる自動化率を100%にすることを目標とする（ツール導入は成熟度の本質ではない）",
            "組織標準のテストプロセス（プロセス資産）を定義・確立し、各プロジェクトがその標準をベースに、特性に合わせて「テーラリング（調整）」して適用できるようにする",
            "CMMIのレベル5を取得している外部ベンダーにテストを丸投げし、自社ではテスト管理を行わないようにする（組織能力の向上にならない）",
            "テスト計画書や設計書の作成を禁止し、すべてのアクティビティを口頭ベースで行うことでアジリティを高める（定義されたプロセスへの逆行）"
        ],
        "answer": [
            "組織標準のテストプロセス（プロセス資産）を定義・確立し、各プロジェクトがその標準をベースに、特性に合わせて「テーラリング（調整）」して適用できるようにする"
        ],
        "explanation": "【解説】\nレベル2（プロジェクトごとの管理）からレベル3（組織的な定義）への壁を超えるには、「組織標準プロセスの確立」と「テーラリングガイドライン」が必須要件です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol108.json)
q1_gen = [
    {
        "id": "Q1-GEN-V108-01",
        "chapter": "第1章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】テスト自動化のROI（投資対効果）試算。\nある回帰テストの手動実行コストは1回あたり10万円である。\n自動化には初期開発に200万円かかり、実行ごとのメンテナンスコストとして1万円かかると想定される。\n自動化への投資が手動コストを下回り、損益分岐点を超えるのは、何回目の実行以降か。",
        "options": [
            "10回目（10回×10万 = 100万 < 200万なので、まだ回収できていない）",
            "20回目（20回×10万 = 200万。自動化コストは200万+20万=220万。まだ赤字）",
            "23回目（手動：230万。自動化：200万 + 23万 = 223万。ここで初めて自動化の方が安くなる）",
            "自動化すれば初回からコスト削減になるため、回数は関係ない（初期投資を無視している）"
        ],
        "answer": [
            "23回目（手動：230万。自動化：200万 + 23万 = 223万。ここで初めて自動化の方が安くなる）"
        ],
        "explanation": "【解説】\n分岐点の計算式：\n(手動単価 × 回数) > (初期費 + 自動化単価 × 回数)\n10x > 200 + 1x\n9x > 200\nx > 22.2...\nしたがって、23回目でペイします。",
        "tags": ["第1章", "一般", "シナリオ", "K4"]
    }
]

# 3. 第2章 一般 (ch2_general_vol108.json)
q2_gen = [
    {
        "id": "Q2-GEN-V108-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】セッションベースドテスト管理（SBTM）。\n探索的テストを管理可能なプロセスにするために、SBTMを導入することにした。\n各セッション（テスト実行単位）の終了時に行われる「デブリーフィング（Debriefing）」の主な目的と内容はどれか。",
        "options": [
            "テスターが発見したバグの数だけを報告し、マネージャがノルマを達成したかどうかを判定して、達成していなければ再テストを命じる（管理主義的すぎる）",
            "テスターが実施した内容（PROOF）、発見したこと、次のセッションへのアイデアをマネージャと対話形式で共有し、チャーターの達成度を確認・学習する",
            "テスト実行中の画面操作をすべて録画し、マネージャが無言でその動画をチェックして、操作ミスがないかを監視する（監視カメラ的な運用は目的が違う）",
            "詳細なテスト手順書を事後的に作成し、誰でも同じテストができるようにドキュメント化を義務付ける（探索的テストのスピード感を殺ぐ）"
        ],
        "answer": [
            "テスターが実施した内容（PROOF）、発見したこと、次のセッションへのアイデアをマネージャと対話形式で共有し、チャーターの達成度を確認・学習する"
        ],
        "explanation": "【解説】\nSBTMの肝はデブリーフィングです。単なる報告ではなく、「対話（Conversation）」を通じてテスト内容を可視化し、次の戦略を練る学習の場です。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol108.json)
q1_aws = [
    {
        "id": "Q1-AWS-V108-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ログ分析のテスト。\nS3バケットに保存された大量のELBアクセスログ（数TB）に対し、特定のエラーコード（5xx）が発生している時間帯やリクエスト元を調査したい。\nサーバーを構築せず、SQLを使って手軽にログを分析・検証するためのAWSサービス構成はどれか。",
        "options": [
            "Amazon EMRでHadoopクラスタを構築し、MapReduceジョブを作成してログファイルを解析する（オーバースペックで準備が大変）",
            "S3上のログデータに対して直接クエリを実行できる「Amazon Athena」を使用し、標準SQLを用いて必要なデータを抽出・分析する",
            "ログファイルをすべてローカルPCにダウンロードし、Excelで開いてフィルタリング機能を使って集計する（データ量が多すぎて開けない）",
            "ログデータをAmazon RDS（リレーショナルデータベース）にインポートし、通常のWebアプリから参照できるように画面を作る（インポートの手間とコストが無駄）"
        ],
        "answer": [
            "S3上のログデータに対して直接クエリを実行できる「Amazon Athena」を使用し、標準SQLを用いて必要なデータを抽出・分析する"
        ],
        "explanation": "【解説】\nS3上のログ分析といえばAthenaです。サーバーレスでSQLが使え、テスト時のログ調査やエビデンス抽出に非常に役立ちます。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol108.json)
q2_fin = [
    {
        "id": "Q2-FIN-V108-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】外国為替（FX）レート変動リスクのテスト。\nリアルタイムの為替レートを取得して日本円換算を行うシステムにおいて、レートの急変や異常値に対する堅牢性を検証したい。\n外部API依存を排除し、再現性のあるテストを行うための手法はどれか。",
        "options": [
            "本番の為替レート配信APIに直接接続し、市場が大きく動くタイミング（雇用統計発表など）を待ってテストを行う（タイミング待ちで計画が立てられない）",
            "為替レート配信サーバーの「モック（Mock）」または「スタブ」を作成し、通常レート、急騰・急落レート、マイナス値や非数値などの異常データを意図的に返却させて挙動を確認する",
            "1ドル=100円の固定レートのみを使用し、変動リスクについては「計算式さえ合っていれば問題ない」とみなしてテストを省略する（リスク検証の放棄）",
            "テスターがストップウォッチを持って画面を監視し、レートが変わった瞬間にボタンを押して、計算が間に合うかを目視確認する（精度の低い人力テスト）"
        ],
        "answer": [
            "為替レート配信サーバーの「モック（Mock）」または「スタブ」を作成し、通常レート、急騰・急落レート、マイナス値や非数値などの異常データを意図的に返却させて挙動を確認する"
        ],
        "explanation": "【解説】\n外部要因（相場）に依存するテストは、モック化して制御下に置くのが鉄則です。異常系や境界値のレートを自由に注入できる環境を作ります。",
        "tags": ["第2章", "金融", "シナリオ", "K3"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol108.json": q3_gen,
    "ch1_general_vol108.json": q1_gen,
    "ch2_general_vol108.json": q2_gen,
    "ch1_aws_vol108.json": q1_aws,
    "ch2_finance_vol108.json": q2_fin
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
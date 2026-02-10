import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.130 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol130.json)
q3_gen = [
    {
        "id": "Q3-GEN-V130-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】IDEALモデルによるプロセス改善。\n組織的なテスト改善活動において、試験的なパイロット運用が終了し、一定の成果が確認された。\nIDEALモデルにおける「学習（Learning）」フェーズとして、次に行うべき活動はどれか。",
        "options": [
            "パイロット運用の結果を分析して教訓（Lessons Learned）をまとめ、プロセスを微調整した上で、改善策を組織全体に展開するための推奨事項を作成する",
            "改善活動は成功したとみなしてプロジェクトを解散し、新しいプロセスに関する文書をイントラネットに格納して終了とする",
            "パイロットプロジェクトで発生した問題を隠蔽し、成功した部分だけを報告することで、全社展開への抵抗感をなくす",
            "直ちに次の新しい改善テーマ（IDEALのIフェーズ）に着手し、今回の改善策の定着化については現場の自主性に任せる"
        ],
        "answer": [
            "パイロット運用の結果を分析して教訓（Lessons Learned）をまとめ、プロセスを微調整した上で、改善策を組織全体に展開するための推奨事項を作成する"
        ],
        "explanation": "【解説】\nIDEALモデルの「学習（Learning）」フェーズは、パイロット運用の評価と分析を行い、次の「展開」に向けた準備を行う段階です。やりっ放しにせず、経験を資産化します。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol130.json)
q1_gen = [
    {
        "id": "Q1-GEN-V130-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ユースケーステストのテストケース作成。\n「ATMでの引き出し」というユースケースには、暗証番号入力成功→金額入力→出金という「基本フロー（Basic Flow）」と、暗証番号間違いや残高不足といった「代替フロー（Alternative Flow）」が存在する。\nカバレッジを高めつつ効率的にテスト設計を行うためのアプローチはどれか。",
        "options": [
            "基本フローを1つのテストケースとし、各代替フローごとに分岐点から終了までを検証する個別のテストケースを作成して、全てのパスを網羅する",
            "基本フローだけがユーザーの主な利用シーンであるため、基本フローのみをテストし、代替フローは探索的テストに委ねて記述しない",
            "全ての代替フローを1つの巨大なテストケースにまとめ、一度の実行で全てのエラーメッセージを確認できるように手順を構成する",
            "ユースケース図に描かれている「アクター」の人数分だけテストケースを作成し、フローの内容自体は考慮しない"
        ],
        "answer": [
            "基本フローを1つのテストケースとし、各代替フローごとに分岐点から終了までを検証する個別のテストケースを作成して、全てのパスを網羅する"
        ],
        "explanation": "【解説】\nユースケーステストでは、Happy Path（基本フロー）だけでなく、そこから派生する例外やエラー処理（代替フロー）を個別のシナリオとして網羅することが重要です。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol130.json)
q2_gen = [
    {
        "id": "Q2-GEN-V130-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】インスペクションにおける役割分担。\n要件定義書のインスペクションを実施するにあたり、モデレーター（進行役）を選出することになった。\nインスペクションを成功させるために、モデレーターとして最も適任な人物はどれか。",
        "options": [
            "対象ドキュメントの作成者（Author）であり、内容を最もよく理解しているため、質問に対して即座に回答できる人物",
            "プロジェクトマネージャであり、欠陥が多く見つかった場合に作成者をその場で叱責し、品質意識を高めることができる人物",
            "作成者とは異なる公平な立場の人物であり、技術的な議論に深入りせず、レビュープロセスが正しく進行するようにファシリテーションできる訓練を受けた人物",
            "新入社員であり、業務知識はないが、会議の進行を経験させることで教育効果が期待できる人物"
        ],
        "answer": [
            "作成者とは異なる公平な立場の人物であり、技術的な議論に深入りせず、レビュープロセスが正しく進行するようにファシリテーションできる訓練を受けた人物"
        ],
        "explanation": "【解説】\nインスペクションのモデレーターは中立である必要があります。作成者（Author）が兼任すると自己防衛に走りやすく、マネージャが兼任すると作成者が萎縮してしまうため不適切です。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol130.json)
q1_aws = [
    {
        "id": "Q1-AWS-V130-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】CloudFrontの地域制限（Geo Restriction）。\n動画配信サービスにおいて、著作権契約の都合上、コンテンツの視聴を「日本国内（JP）」からのアクセスのみに限定したい。\nこの要件を満たしていることを検証するためのテスト方法はどれか。",
        "options": [
            "CloudFrontの「地理的制限（Geo Restriction）」を有効にしてホワイトリストに「JP」を設定し、海外のVPNやプロキシサーバーを経由してアクセスした際に「403 Forbidden」が返されることを確認する",
            "S3バケットポリシーで日本以外のIPアドレスを拒否する設定を行い、CloudFrontの設定は変更せずにテストする",
            "Webサーバーのアプリケーションロジックでブラウザの言語設定（Accept-Language）を確認し、'ja' 以外の場合にエラー画面を表示することを確認する",
            "Route 53のレイテンシーベースルーティングを使用して、日本以外のユーザーを存在しないサーバーに誘導することを確認する"
        ],
        "answer": [
            "CloudFrontの「地理的制限（Geo Restriction）」を有効にしてホワイトリストに「JP」を設定し、海外のVPNやプロキシサーバーを経由してアクセスした際に「403 Forbidden」が返されることを確認する"
        ],
        "explanation": "【解説】\n国単位のアクセス制御にはCloudFrontのGeo Restrictionが最適です。テストでは、対象国からの許可（Allow）と、対象外国からの拒否（Block）の両方を検証します。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol130.json)
q2_fin = [
    {
        "id": "Q2-FIN-V130-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】金融商品の値洗い（Mark-to-Market）。\n保有している有価証券の期末評価において、「時価評価（値洗い）」が正しく行われているかを検証したい。\n取得原価と時価の差額（評価損益）の計算ロジックとして、確認すべきポイントはどれか。",
        "options": [
            "期末日の市場価格（時価）と帳簿価額（取得原価または償却原価）を比較し、その差額が「評価益」または「評価損」として財務諸表に計上される仕訳が生成されていること",
            "有価証券は常に取得原価で評価されるため、市場価格が変動しても帳簿価額は一切変更されず、評価損益も発生しないこと",
            "市場価格が下落した場合のみ評価損を計上し、上昇した場合は利益確定するまで評価益を計上しない「低価法」が、すべての保有区分（売買目的含む）に適用されていること",
            "評価損益は税金計算に関係ないため、システム内部で計算するだけでよく、会計仕訳としては出力されないこと"
        ],
        "answer": [
            "期末日の市場価格（時価）と帳簿価額（取得原価または償却原価）を比較し、その差額が「評価益」または「評価損」として財務諸表に計上される仕訳が生成されていること"
        ],
        "explanation": "【解説】\n売買目的有価証券などは、期末に時価評価（値洗い）を行い、評価差額を損益（PL）に計上する必要があります。この自動仕訳が正しく起きるかがテストの要点です。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol130.json": q3_gen,
    "ch1_general_vol130.json": q1_gen,
    "ch2_general_vol130.json": q2_gen,
    "ch1_aws_vol130.json": q1_aws,
    "ch2_finance_vol130.json": q2_fin
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
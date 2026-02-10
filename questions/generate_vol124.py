import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.124 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol124.json)
q3_gen = [
    {
        "id": "Q3-GEN-V124-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストプロセス改善（TPI Next）の成熟度マトリクス。\n自社のテストプロセスを評価した結果、多くのキーエリア（Key Areas）はレベルAに達しているが、「テストツール」と「テスト環境」のエリアだけが未達であった。\nTPI Nextにおける「成熟度レベル」の判定ルールとして、正しい解釈はどれか。",
        "options": [
            "全てのキーエリアがレベルAの要件を満たしていないため、組織全体の成熟度は「レベルA（制御された）」とは認定されず、それ以下のレベルと判定される",
            "大半のエリアがレベルAに達しているため、平均点を取って「レベルA」と認定し、未達のエリアは次回の改善目標とする",
            "「テストツール」と「テスト環境」は技術的な要素であり、プロセス成熟度の本質ではないため、これらが未達であってもレベルAの認定には影響しない",
            "TPI Nextには全体的な成熟度レベルという概念は存在しないため、各エリアごとのスコアを個別に報告すればよい"
        ],
        "answer": [
            "全てのキーエリアがレベルAの要件を満たしていないため、組織全体の成熟度は「レベルA（制御された）」とは認定されず、それ以下のレベルと判定される"
        ],
        "explanation": "【解説】\nTPI Nextでは、ある成熟度レベルに到達するためには、そのレベルに割り当てられた「すべてのチェックポイント」をクリアする必要があります。一つでも欠けていれば、そのレベルには達していません。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol124.json)
q1_gen = [
    {
        "id": "Q1-GEN-V124-01",
        "chapter": "第1章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】状態遷移テストのNスイッチカバレッジ。\n「待機」→「処理中」→「完了」という単純な遷移だけでなく、「処理中」から一度「一時停止」を経て「処理中」に戻り、そこから「完了」するような、履歴（過去の状態）に依存するバグを検出したい。\nこの場合に採用すべきカバレッジ基準はどれか。",
        "options": [
            "0スイッチカバレッジ（0-switch coverage）を採用し、状態間の直接的な遷移（A→B）をすべて網羅する",
            "1スイッチカバレッジ（1-switch coverage）を採用し、「遷移→遷移」という2段階のシーケンス（A→B→C）を網羅することで、1つ前の状態履歴を考慮したテストを行う",
            "全遷移ペア（All Transition Pairs）を採用し、任意の2つの遷移の組み合わせをランダムに選んでテストする",
            "ステートメントカバレッジ（C0）を採用し、状態遷移を実装しているswitch文のすべてのcase句を一度は実行する"
        ],
        "answer": [
            "1スイッチカバレッジ（1-switch coverage）を採用し、「遷移→遷移」という2段階のシーケンス（A→B→C）を網羅することで、1つ前の状態履歴を考慮したテストを行う"
        ],
        "explanation": "【解説】\n「Nスイッチ」は「N+1回」の遷移連続を指します。過去の履歴（コンテキスト）に依存するバグを見つけるには、単なる遷移（0スイッチ）ではなく、Nスイッチ（この場合は1スイッチ以上）が必要です。",
        "tags": ["第1章", "一般", "シナリオ", "K4"]
    }
]

# 3. 第2章 一般 (ch2_general_vol124.json)
q2_gen = [
    {
        "id": "Q2-GEN-V124-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ビッグバン統合のリスク回避。\n5つのサブシステムからなる大規模システムの統合テストを計画している。全チームの開発終了時期が揃わないため、一斉に結合する「ビッグバン統合」は避けたい。\n最も手戻りリスクを抑え、かつコア機能の動作を早期に確認できる統合戦略はどれか。",
        "options": [
            "すべてのサブシステムが完成するまでテストを待機し、リリース直前の1週間で全員が集まって一気に接続確認を行う",
            "システムの骨格（バックボーン）となるモジュールを最初に統合し、そこに各機能モジュールを順次追加していく「バックボーン統合（スケルトン統合）」を採用する",
            "各サブシステムを個別にリリースしてしまい、本番環境でユーザーに使ってもらいながら、不具合が出たらその都度インターフェースを修正する",
            "ドライバとスタブを大量に作成し、すべてのモジュールを完全に独立させてテストを行い、実際の結合は行わないままリリースする"
        ],
        "answer": [
            "システムの骨格（バックボーン）となるモジュールを最初に統合し、そこに各機能モジュールを順次追加していく「バックボーン統合（スケルトン統合）」を採用する"
        ],
        "explanation": "【解説】\nビッグバンの対極にあるのが「増分統合（Incremental Integration）」です。特に、中核となる骨格を先に通すバックボーン統合は、早期に疎通確認ができるためリスク低減に有効です。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol124.json)
q1_aws = [
    {
        "id": "Q1-AWS-V124-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】AWS Configによるコンプライアンステスト。\n「本番環境のEC2インスタンスには、SSHポート（22）が全開放（0.0.0.0/0）されているセキュリティグループをアタッチしてはならない」というルールを強制したい。\nこのルール違反を自動検知し、継続的に監視するための構成はどれか。",
        "options": [
            "AWS Configルール（restricted-ssh）を有効化し、違反するセキュリティグループが検出された場合に、Configのダッシュボードに「非準拠（Non-compliant）」として表示させる",
            "毎日手動で全てのセキュリティグループの設定を目視確認し、Excelのチェックリストに記録する運用を徹底する",
            "VPCフローログを分析し、22番ポートへのアクセス履歴があるIPアドレスをすべてブロックリストに追加する",
            "Amazon Inspectorエージェントを全インスタンスにインストールし、OS内部のファイアウォール設定（iptablesなど）のみを監視する"
        ],
        "answer": [
            "AWS Configルール（restricted-ssh）を有効化し、違反するセキュリティグループが検出された場合に、Configのダッシュボードに「非準拠（Non-compliant）」として表示させる"
        ],
        "explanation": "【解説】\nAWSリソースの設定状態（Configuration）を監視・評価するのは「AWS Config」の役割です。マネージドルールを使うことで、SSH全開放などの典型的な違反を即座に検知できます。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol124.json)
q2_fin = [
    {
        "id": "Q2-FIN-V124-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】金利指標の移行（LIBOR廃止対応）。\n既存の変動金利ローンシステムにおいて、参照指標を廃止された「LIBOR」から、代替指標である「TORF（東京ターム物リスク・フリー・レート）」等へ移行する改修を行った。\nこの移行に伴うテストにおいて、特に注意して検証すべき「指標間の性質の違い」はどれか。",
        "options": [
            "LIBORもTORFも名前が違うだけで中身は全く同じ金利指標であるため、画面上のラベル表示が変わっていることだけを確認すればよい",
            "LIBORには「銀行の信用リスク」が織り込まれていたが、TORF等のRFR（リスク・フリー・レート）には信用リスクが含まれないため、その差分を埋める「スプレッド調整（Adjustment Spread）」が正しく加算されているかを確認する",
            "新しい指標は常にプラスの金利になるため、マイナス金利のテストケースは全て削除してテストを簡略化する",
            "指標の移行は契約上の問題でありシステム計算には影響しないため、旧システムの計算結果と新システムの計算結果が1円単位まで完全一致することを確認する"
        ],
        "answer": [
            "LIBORには「銀行の信用リスク」が織り込まれていたが、TORF等のRFR（リスク・フリー・レート）には信用リスクが含まれないため、その差分を埋める「スプレッド調整（Adjustment Spread）」が正しく加算されているかを確認する"
        ],
        "explanation": "【解説】\nLIBOR移行の最大の要点は、リスクフリーレートへの変更に伴う「スプレッド調整」です。単純な置き換えでは利率が変わってしまうため、調整値の加算ロジックが必須の検証ポイントになります。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol124.json": q3_gen,
    "ch1_general_vol124.json": q1_gen,
    "ch2_general_vol124.json": q2_gen,
    "ch1_aws_vol124.json": q1_aws,
    "ch2_finance_vol124.json": q2_fin
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
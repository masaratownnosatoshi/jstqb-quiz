import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.127 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol127.json)
q3_gen = [
    {
        "id": "Q3-GEN-V127-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】リスクベースドテスト（RBT）のステークホルダー合意。\nテストマネージャとしてリスクベースドテストの導入を提案したが、ステークホルダーから「リスクが低い機能のテストを省略することで、品質低下に繋がるのではないか」という懸念が出された。\nRBTの本質に基づいた、適切な回答アプローチはどれか。",
        "options": [
            "リスクの低い機能はバグが出ても修正コストが安いため、品質低下を受け入れてでもテストコストを削減すべきであると説得する",
            "テストを省略するのではなく、リスクの高さに応じてテストの厚み（技法や深さ）にメリハリをつけることで、限られたリソースで全体的な残留リスクを最小化するアプローチであると説明する",
            "ステークホルダーの懸念はもっともであるため、RBTの導入は諦め、すべての機能に対して一律に等しい時間をかけてテストを行う従来の方式に戻す",
            "テスト自動化ツールを導入すれば、すべてのテストケースを瞬時に実行できるため、リスク分析自体が不要になると説明する"
        ],
        "answer": [
            "テストを省略するのではなく、リスクの高さに応じてテストの厚み（技法や深さ）にメリハリをつけることで、限られたリソースで全体的な残留リスクを最小化するアプローチであると説明する"
        ],
        "explanation": "【解説】\nRBTの目的は「テストの手抜き」ではなく「リソースの最適配分」です。低リスク機能は簡易的な確認に留め、高リスク機能に手厚く投資することで、致命的な障害リスクを下げます。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol127.json)
q1_gen = [
    {
        "id": "Q1-GEN-V127-01",
        "chapter": "第1章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】欠陥除去率（DRE: Defect Removal Efficiency）の計算。\nあるプロジェクトのシステムテスト工程で80件のバグを発見・修正してリリースした。\nその後、リリースから半年間の運用中に、ユーザーによって新たに20件のバグが発見された。\nこの時点での欠陥除去率（DRE）は何％か。",
        "options": [
            "20%（発見されたバグのうち、市場流出した割合）",
            "25%（市場バグ数 ÷ テストバグ数）",
            "80%（テストバグ数 ÷ (テストバグ数 ＋ 市場バグ数)）",
            "400%（テストバグ数 ÷ 市場バグ数）"
        ],
        "answer": [
            "80%（テストバグ数 ÷ (テストバグ数 ＋ 市場バグ数)）"
        ],
        "explanation": "【解説】\nDREは「開発中に除去できたバグの割合」を示します。\n計算式：テストで除去したバグ数 / (テストで除去したバグ数 + リリース後のバグ数)\n80 / (80 + 20) = 80 / 100 = 80%",
        "tags": ["第1章", "一般", "シナリオ", "K4"]
    }
]

# 3. 第2章 一般 (ch2_general_vol127.json)
q2_gen = [
    {
        "id": "Q2-GEN-V127-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】A/Bテストによる改善検証。\nECサイトの「購入ボタン」の色を、現在の青色から赤色に変更することで、コンバージョン率（CVR）が向上するという仮説を立てた。\nこの仮説を科学的に検証するためのテスト手法として、最も適切なものはどれか。",
        "options": [
            "色彩心理学の専門家を招いてヒューリスティック評価を行い、赤色の方が購買意欲をそそるかどうかを判定してもらう",
            "本番環境のトラフィックをランダムに分割し、一部のユーザーには青いボタン（Aパターン）、残りのユーザーには赤いボタン（Bパターン）を表示して、実際の購入率を比較計測する",
            "開発環境でテスターが両方のボタンを何度もクリックし、赤いボタンの方がクリックしやすいかどうかを主観的に評価する",
            "サイト利用者全員に対してアンケートを実施し、「ボタンが赤色になったらもっと買いますか？」と質問して回答を集計する"
        ],
        "answer": [
            "本番環境のトラフィックをランダムに分割し、一部のユーザーには青いボタン（Aパターン）、残りのユーザーには赤いボタン（Bパターン）を表示して、実際の購入率を比較計測する"
        ],
        "explanation": "【解説】\nUI変更の効果検証には「A/Bテスト（スプリットテスト）」が最適です。実際のユーザー行動（数字）に基づいて判断するため、主観や予測よりも確実なデータが得られます。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol127.json)
q1_aws = [
    {
        "id": "Q1-AWS-V127-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】Lambdaのコールドスタート対策。\nAPI Gateway + Lambdaで構築されたWeb APIにおいて、しばらくアクセスがない状態から久しぶりにリクエストを送ると、最初の1回だけ応答に数秒かかってしまう。\nこの「コールドスタート」による遅延を解消し、常に低レイテンシを維持するための設定はどれか。",
        "options": [
            "Lambda関数のタイムアウト設定を最大値（15分）まで延長し、処理が途中で打ち切られないようにする",
            "Lambda関数のメモリ割り当てを最大（10GB）まで増やすことで、CPUパワーを上げて初期化処理を高速化する",
            "「プロビジョニングされた同時実行（Provisioned Concurrency）」を設定し、あらかじめ指定した数の実行環境を初期化済み（ウォーム状態）に保つ",
            "CloudWatch Eventsを使用して1秒ごとにLambdaを呼び出すスケジュールを設定し、無理やり稼働させ続ける"
        ],
        "answer": [
            "「プロビジョニングされた同時実行（Provisioned Concurrency）」を設定し、あらかじめ指定した数の実行環境を初期化済み（ウォーム状態）に保つ"
        ],
        "explanation": "【解説】\nコールドスタート対策の正攻法は「Provisioned Concurrency」です。環境をあらかじめ暖機運転（初期化）しておくことで、最初のリクエストから即座に応答できます。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol127.json)
q2_fin = [
    {
        "id": "Q2-FIN-V127-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】銀行間取引の照合（Reconciliation）と起算日。\n自社の当座預金元帳と、取引銀行から送られてきた残高証明書（MT940等）を照合したところ、残高が一致しなかった。\n調査の結果、ある入金取引について、自社システムでは「取引日（Entry Date）」で計上していたが、銀行側は「起算日（Value Date）」で計上していることが判明した。\nこの差異に対する金融システムとしての正しい解釈はどれか。",
        "options": [
            "銀行のシステムが間違っているため、銀行に対して取引データの修正を依頼し、Entry Dateに合わせて残高を再計算させる",
            "資金繰りや利息計算の観点では、資金が実際に利用可能になる「起算日（Value Date）」が重要であるため、照合ロジックではValue Date基準での一致を確認すべきである",
            "Entry DateとValue Dateのズレはシステムバグであるため、自社システムのカレンダー設定を修正して、すべての取引が即日決済されるように変更する",
            "少額の金利差であれば無視できるため、日付のズレは許容範囲として「照合OK」とする例外ルールを適用する"
        ],
        "answer": [
            "資金繰りや利息計算の観点では、資金が実際に利用可能になる「起算日（Value Date）」が重要であるため、照合ロジックではValue Date基準での一致を確認すべきである"
        ],
        "explanation": "【解説】\n金融取引において最も重要なのは「Value Date（効力発生日/起算日）」です。利息計算や資金拘束はこの日付に基づくため、照合もValue Dateを基準に行う必要があります。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol127.json": q3_gen,
    "ch1_general_vol127.json": q1_gen,
    "ch2_general_vol127.json": q2_gen,
    "ch1_aws_vol127.json": q1_aws,
    "ch2_finance_vol127.json": q2_fin
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
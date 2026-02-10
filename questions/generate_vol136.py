import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.136 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol136.json)
q3_gen = [
    {
        "id": "Q3-GEN-V136-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テスト自動化のROI（費用対効果）評価。\nテスト自動化プロジェクトを開始して半年が経過し、経営層から「投資に見合う効果が出ているか」を問われた。\n自動化の成果を定量的かつ適切に報告するための指標として、最も説得力のあるものはどれか。",
        "options": [
            "自動テストスクリプトの作成にかかった総行数（LOC）を報告し、これだけの規模のプログラムを作成したという生産性を示す",
            "手動で実施した場合の想定コストと、自動化の開発・保守・実行にかかったコストを比較し、さらに「回帰テストの実行回数」や「リリースサイクルの短縮日数」を提示する",
            "自動テストによって発見されたバグの数だけを報告し、手動テストよりも多くのバグを見つけたと主張する",
            "自動テストツールのライセンス費用がどれだけ高額だったかを報告し、これだけ投資したのだから効果があるはずだと説明する"
        ],
        "answer": [
            "手動で実施した場合の想定コストと、自動化の開発・保守・実行にかかったコストを比較し、さらに「回帰テストの実行回数」や「リリースサイクルの短縮日数」を提示する"
        ],
        "explanation": "【解説】\n自動化のROIは、単なるコスト差分だけでなく、「時間の短縮（Time to Market）」や「繰り返し実行による利益」を含めて評価するのが適切です。バグ発見数は自動化の主目的（回帰テスト）ではないため、主要指標にはなりにくいです。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol136.json)
q1_gen = [
    {
        "id": "Q1-GEN-V136-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】探索的テストの「ツアー（Tours）」メタファ。\nJames Whittakerが提唱した「ツアー（Tours）」メタファを用いて、アプリケーションの特定の側面を探索したい。\n「スーパーモデルツアー（The Supermodel Tour）」を選択した場合、テスターが重点的に確認すべきポイントはどれか。",
        "options": [
            "機能の内部ロジックやデータベースの整合性には目をつぶり、GUIの見た目、デザインの崩れ、描画パフォーマンスといった「表面的な美しさ」や「第一印象」を集中的にチェックする",
            "システムのエラー処理を徹底的に攻撃し、不正な入力を繰り返してアプリケーションをクラッシュさせることに集中する",
            "一般ユーザーが最も頻繁に使用する標準的な操作ルート（メインストリート）を通り、基本的な機能が動作することを確認する",
            "アプリケーションのヘルプファイルやマニュアルに記載されている通りに操作し、ドキュメントの記述と実際の動作が一致しているかを確認する"
        ],
        "answer": [
            "機能の内部ロジックやデータベースの整合性には目をつぶり、GUIの見た目、デザインの崩れ、描画パフォーマンスといった「表面的な美しさ」や「第一印象」を集中的にチェックする"
        ],
        "explanation": "【解説】\n「スーパーモデルツアー」は、中身（ロジック）ではなく、表面（UI/UX）の美しさや見栄えに焦点を当てる探索アプローチです。探索的テストにテーマを持たせるための有効な手法です。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol136.json)
q2_gen = [
    {
        "id": "Q2-GEN-V136-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】状態遷移テストの「無効遷移（Invalid Transition）」。\n「未払い」状態からは「支払い完了」への遷移のみが許可されており、「発送済み」への直接遷移は禁止されている仕様である。\nこの「禁止された遷移」がシステム上で正しくブロックされることを確認するためのテストケースとして、適切な記述はどれか。",
        "options": [
            "「未払い」状態で「発送する」アクションを実行しようとした場合、システムが何も反応せず、エラーも出さずに無視することを確認する",
            "「未払い」状態で「発送する」アクションを実行しようとした場合、システムが遷移を拒否し、適切なエラーメッセージを表示するか、あるいは操作自体がUI上で無効化（グレーアウト）されていることを確認する",
            "「未払い」状態から一旦「支払い完了」に遷移させ、その後に「発送済み」へ遷移させる正常ルートを確認する",
            "「発送済み」状態から「未払い」状態への逆方向の遷移が可能かどうかを確認する"
        ],
        "answer": [
            "「未払い」状態で「発送する」アクションを実行しようとした場合、システムが遷移を拒否し、適切なエラーメッセージを表示するか、あるいは操作自体がUI上で無効化（グレーアウト）されていることを確認する"
        ],
        "explanation": "【解説】\n状態遷移テストでは、許可された遷移（有効遷移）だけでなく、あり得ない遷移（無効遷移）を試みた際の挙動（エラー通知や操作ブロック）も重要な検証対象です。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol136.json)
q1_aws = [
    {
        "id": "Q1-AWS-V136-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】CloudWatch Logsのリアルタイム監視。\nアプリケーションログの中に「ERROR」という文字列が出力されたら、即座にLambda関数を起動してSlackに通知を送りたい。\nこれを実現するための最も低遅延かつ標準的なAWS構成はどれか。",
        "options": [
            "CloudWatch Logsに「サブスクリプションフィルタ」を設定し、ログイベントを直接Lambda関数にストリーミングして、Lambda内でキーワード判定と通知を行う",
            "Lambda関数を5分ごとにスケジュール実行（cron）し、CloudWatch LogsのAPIを呼び出して過去5分間のログを検索（FilterLogEvents）する",
            "S3バケットへのログエクスポートを設定し、S3にファイルが保存されたイベント（PutObject）をトリガーにLambdaを起動してファイルの中身を解析する",
            "EC2インスタンス内に監視エージェントを自作して常駐させ、ログファイルを tail -f で監視して、エラーが出たらメールコマンドを実行する"
        ],
        "answer": [
            "CloudWatch Logsに「サブスクリプションフィルタ」を設定し、ログイベントを直接Lambda関数にストリーミングして、Lambda内でキーワード判定と通知を行う"
        ],
        "explanation": "【解説】\nログのリアルタイム処理には「サブスクリプションフィルタ」を使用します。ログ取り込みとほぼ同時にLambdaへデータをプッシュできるため、ポーリングやバッチ処理よりも即応性が高いです。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol136.json)
q2_fin = [
    {
        "id": "Q2-FIN-V136-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】FX証拠金取引の「スワップポイント」付与。\nFX取引システムのテストにおいて、ポジションを翌日まで持ち越した（ロールオーバーした）際に付与される「スワップポイント（金利差調整額）」の計算を検証したい。\n水曜日から木曜日にかけて持ち越した場合の、一般的な市場慣行（T+2決済）に基づくスワップポイント付与日数は何日分か。",
        "options": [
            "1日分（通常通り1日経過したため）",
            "3日分（土日の2日分が加算されるため）",
            "0日分（水曜日は市場調整日のため付与されない）",
            "7日分（1週間分をまとめて付与するため）"
        ],
        "answer": [
            "3日分（土日の2日分が加算されるため）"
        ],
        "explanation": "【解説】\nFXのスポット取引は通常「T+2」決済です。水曜日の取引の決済日は金曜日、木曜日の取引の決済日は翌週月曜日となります。この間に土日（2日間）が含まれるため、水曜日のロールオーバー時には「3日分」のスワップが付与されるのが慣行です（通称：水曜日の3倍デー）。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol136.json": q3_gen,
    "ch1_general_vol136.json": q1_gen,
    "ch2_general_vol136.json": q2_gen,
    "ch1_aws_vol136.json": q1_aws,
    "ch2_finance_vol136.json": q2_fin
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
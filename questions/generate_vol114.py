import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.114 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol114.json)
q3_gen = [
    {
        "id": "Q3-GEN-V114-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストチームのサイロ化（孤立）解消。\n「開発チーム」と「テストチーム」が完全に分断されており、テストチームは開発が終わってから成果物を投げつけられる（Over the wall）だけの関係になっている。\nこの状況を改善し、品質を作り込むための組織的なアプローチはどれか。",
        "options": [
            "テストチームの権限を強化し、品質基準を満たさない成果物を受け取った場合は、開発チームのマネージャに対して正式な抗議文を送付するプロセスを確立する（対立を深めるだけ）",
            "「シフトレフト」を推進し、要件定義や設計レビューの段階からテスターが参加して、テスト容易性の観点からフィードバックを行う活動を定着させる",
            "テストチームを解散して全員を開発チームに吸収合併し、開発者が自分でテストも行う「フルスタックエンジニア」体制に一気に移行する（専門性の喪失と混乱のリスク）",
            "開発チームとの交流を深めるために、週に一度のランチ会を義務付け、業務以外の話題で盛り上がることで心理的な壁を取り払う（業務プロセスの改善には直結しない）"
        ],
        "answer": [
            "「シフトレフト」を推進し、要件定義や設計レビューの段階からテスターが参加して、テスト容易性の観点からフィードバックを行う活動を定着させる"
        ],
        "explanation": "【解説】\nサイロ化の解消には、工程の上流（左側）への早期参画（シフトレフト）が最も有効です。受け身の姿勢から、能動的な品質作り込みへと役割を変えます。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol114.json)
q1_gen = [
    {
        "id": "Q1-GEN-V114-01",
        "chapter": "第1章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】レガシーシステムのマイグレーションテスト戦略。\n20年稼働したメインフレームシステムをオープン系サーバーに刷新する。\n仕様書は古くて信用できず、ロジックもブラックボックス化している。\nこの移行プロジェクトにおける最も安全で確実なテスト戦略はどれか。",
        "options": [
            "古い仕様書を元に新システムのテストケースをゼロから作成し、仕様書通りに動くことを確認することで、あるべき姿（To-Be）を実現する（現行仕様との乖離リスクが大きい）",
            "「現新比較テスト（Parallel Testing）」を採用し、新旧両方のシステムに同じ入力データを与え、出力結果（帳票やファイル）がビット単位または許容誤差範囲内で一致することを全量検証する",
            "移行ツールを使用するためロジックは自動的に正しく変換されると信じ、テストは最低限の正常系確認のみに留めてコストを削減する（ツールの変換ミスや環境差異を見逃す）",
            "業務部門のユーザーに新システムを使ってもらい、違和感がないかどうかを感覚的に判断してもらう「ユーザー受入テスト」のみに全リソースを集中する（網羅性が低い）"
        ],
        "answer": [
            "「現新比較テスト（Parallel Testing）」を採用し、新旧両方のシステムに同じ入力データを与え、出力結果（帳票やファイル）がビット単位または許容誤差範囲内で一致することを全量検証する"
        ],
        "explanation": "【解説】\n仕様が不明なレガシー移行では、「現行システム＝正解（仕様）」とみなす現新比較（パラレルテスト）が唯一の現実解です。",
        "tags": ["第1章", "一般", "シナリオ", "K4"]
    }
]

# 3. 第2章 一般 (ch2_general_vol114.json)
q2_gen = [
    {
        "id": "Q2-GEN-V114-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】境界値分析（2点法 vs 3点法）。\n「18歳以上60歳未満」が入会可能なシステムで、年齢入力欄の境界値テストを行いたい。\n最も効率的かつリスクの低い「2点法（2-value boundary value analysis）」で選択すべきテストデータの組み合わせはどれか。",
        "options": [
            "境界値そのものとその内側を確認するため、「18, 19」と「59, 60」を選択する（境界の外側（無効値）のテストが含まれていない）",
            "有効クラスと無効クラスの境界を確認するため、「17（無効）, 18（有効）」および「59（有効）, 60（無効）」を選択する",
            "3点法を採用し、「17, 18, 19」および「59, 60, 61」を選択して、境界値を挟んだ前後すべての値を手厚くテストする（2点法という条件に反する）",
            "代表値として「30」を選び、さらに境界値として「18」と「60」を選ぶことで、全体的な動作確認を行う（境界値分析としての網羅性が中途半端）"
        ],
        "answer": [
            "有効クラスと無効クラスの境界を確認するため、「17（無効）, 18（有効）」および「59（有効）, 60（無効）」を選択する"
        ],
        "explanation": "【解説】\n2点法は「境界値（ON）」と「その隣の無効値（OFF）」をテストします。18以上なら18(Valid)と17(Invalid)、60未満（59以下）なら59(Valid)と60(Invalid)が境界です。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol114.json)
q1_aws = [
    {
        "id": "Q1-AWS-V114-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】AWSの合成モニタリング（Synthetic Monitoring）。\nWebサイトの「ログイン→商品検索→カート追加」という重要導線が、24時間365日正常に動作しているかを監視したい。\nサーバー内部のログ監視だけでなく、ユーザー視点での死活監視を実現するAWSサービスはどれか。",
        "options": [
            "Amazon CloudWatch Syntheticsの「Canary」を使用し、SeleniumまたはPuppeteerベースのスクリプトを定期実行して、ユーザー操作をシミュレーション監視する",
            "AWS Lambdaを1分ごとに実行してトップページにHTTPリクエストを送り、ステータスコードが200であることを確認する（画面遷移やDOMの描画確認ができない）",
            "Amazon GuardDutyを有効化し、Webサイトに対する不審なアクセスパターンを検知してアラートを出す（セキュリティ監視であり、動作監視ではない）",
            "開発チームが交代制で1時間ごとに手動でサイトにアクセスし、正常に動いているかを目視確認する（運用負荷が高すぎて持続不可能）"
        ],
        "answer": [
            "Amazon CloudWatch Syntheticsの「Canary」を使用し、SeleniumまたはPuppeteerベースのスクリプトを定期実行して、ユーザー操作をシミュレーション監視する"
        ],
        "explanation": "【解説】\nSynthetics Canaryを使えば、ユーザーの一連の操作（シナリオ）を定期的に自動実行し、UIレベルでの死活監視が可能になります。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol114.json)
q2_fin = [
    {
        "id": "Q2-FIN-V114-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ATMの現金処理テスト。\nATMの実機テストにおいて、「出金口に紙幣が詰まる（ジャム）」という物理障害が発生した際の、トランザクション整合性を検証したい。\n実施すべきテストシナリオとその期待結果はどれか。",
        "options": [
            "出金処理中に電源ケーブルを抜き、再起動後に取引が「成立」となっており、口座残高が減算されていることを確認する（現金を受け取っていないのに減算されるのはバグ）",
            "出金処理中に紙幣搬送部で紙幣を故意に詰まらせ、センサーが異常を検知した時点で取引が「取消（Reversal）」され、口座残高が減算されない（または即時返金される）ことを確認する",
            "紙幣詰まりはハードウェアの問題であり、ソフトウェア側では関知しないため、エラー画面が表示されることだけを確認し、残高については検証しない（金融事故の原因になる）",
            "詰まった紙幣を無理やり引っ張り出し、ATMが正常に動作を再開できるか耐久性をテストする（ハードウェアの破壊試験であり、論理テストではない）"
        ],
        "answer": [
            "出金処理中に紙幣搬送部で紙幣を故意に詰まらせ、センサーが異常を検知した時点で取引が「取消（Reversal）」され、口座残高が減算されない（または即時返金される）ことを確認する"
        ],
        "explanation": "【解説】\n金融端末のテストでは、物理障害（紙幣詰まり、カード詰まり）発生時に、顧客の資産（残高）が守られること（原子性）の検証が最重要です。",
        "tags": ["第2章", "金融", "シナリオ", "K3"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol114.json": q3_gen,
    "ch1_general_vol114.json": q1_gen,
    "ch2_general_vol114.json": q2_gen,
    "ch1_aws_vol114.json": q1_aws,
    "ch2_finance_vol114.json": q2_fin
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
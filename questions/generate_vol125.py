import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.125 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol125.json)
q3_gen = [
    {
        "id": "Q3-GEN-V125-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストの独立性（Independence of Testing）。\n開発チームとは別に、社外の第三者検証専門会社にシステムテストを委託することになった。\n独立性を高めることによるメリットは明確であるが、一方で懸念されるリスクとその対策として適切なものはどれか。",
        "options": [
            "開発チームとテストチームの対立やコミュニケーション不足により、仕様の誤解やフィードバックの遅延が発生するリスクがあるため、定期的なミーティングやチャットツールでの密な連携フローを確立する",
            "外部のテストチームは開発の内部事情を知らないため、テストの品質が必ず低下するというリスクがあり、開発者が作成したテストケースのみを実行させるように制限する",
            "独立性が高すぎると開発チームが品質保証の責任を放棄してしまうため、バグが発見された場合の修正責任もテストチームに負わせる契約にする",
            "外部委託はセキュリティリスクが高いため、本番環境と全く同じデータをテスト環境で使用させ、データ漏洩が起きないかどうかを監視対象にする"
        ],
        "answer": [
            "開発チームとテストチームの対立やコミュニケーション不足により、仕様の誤解やフィードバックの遅延が発生するリスクがあるため、定期的なミーティングやチャットツールでの密な連携フローを確立する"
        ],
        "explanation": "【解説】\nテストの独立性が高い（開発者と別組織である）場合、客観性は増しますが、開発コンテキストの共有不足や対立構造（Us vs Them）が生じやすくなります。意図的なコミュニケーション設計が必要です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol125.json)
q1_gen = [
    {
        "id": "Q1-GEN-V125-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】探索的テストのタイムボックス管理。\n60分間のセッションで探索的テストを実施していたが、終了間際に重大なバグの兆候を見つけた。\nしかし、原因を特定するにはさらに30分以上かかりそうである。\nセッションベースドテスト管理（SBTM）の原則に基づく、最も適切な行動はどれか。",
        "options": [
            "バグの兆候を見つけた以上、時間を気にせず解決するまで調査を続け、セッション時間を事後報告で90分に修正する",
            "タイムボックス（60分）は厳守すべきであるため、現在のセッションはいったん終了して記録を残し、調査の続きを行うための新しいセッションを別途スケジュールする",
            "時間切れでバグを見逃すのは避けるべきだが、記録をつけるのは手間なので、正式なセッションとは別枠の休憩時間を使って個人的に調査を続ける",
            "タイムボックス内に完了しなかったタスクは失敗とみなされるため、バグの兆候は見なかったことにして、時間内に完了した部分だけを報告する"
        ],
        "answer": [
            "タイムボックス（60分）は厳守すべきであるため、現在のセッションはいったん終了して記録を残し、調査の続きを行うための新しいセッションを別途スケジュールする"
        ],
        "explanation": "【解説】\nタイムボックスの延長は、計画や集中力管理を崩すため原則禁止です。新しいチャーター（Opportunity）として切り出し、別のセッション枠で実施するのがSBTMのルールです。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol125.json)
q2_gen = [
    {
        "id": "Q2-GEN-V125-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】境界値分析（3点法）。\n入力フィールドの仕様が「10以上、50以下（整数）」と定義されている。\n「3点法（3-value boundary value analysis）」を用いて、下限の境界付近をテストする場合のテストデータの組み合わせとして正しいものはどれか。",
        "options": [
            "境界値である「10」と、その隣の無効値である「9」の2つを選択する",
            "境界値「10」、その1つ下の無効値「9」、および1つ上の有効値「11」の3つを選択する",
            "代表値「30」、下限「10」、上限「50」の3つを選択する",
            "有効値「10」、無効値「-10」、無効値「0」の3つを選択する"
        ],
        "answer": [
            "境界値「10」、その1つ下の無効値「9」、および1つ上の有効値「11」の3つを選択する"
        ],
        "explanation": "【解説】\n3点法では、境界値そのもの（ON）、境界の一つ外側（OFF）、境界の一つ内側（IN/Interior）の3点をテストします。10以上の場合、9(無効), 10(有効), 11(有効)となります。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol125.json)
q1_aws = [
    {
        "id": "Q1-AWS-V125-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】CloudFrontによる有料コンテンツ配信テスト。\n動画配信サイトにおいて、有料会員にのみ動画へのアクセスを許可するため、CloudFrontの「署名付きURL（Signed URL）」または「署名付きCookie」を使用している。\nこのアクセス制御が正しく機能していることを検証するためのテストケースはどれか。",
        "options": [
            "署名付きURLを発行し、有効期限内であれば動画が再生できること、および有効期限が切れた後や署名の一部を改ざんしたURLでは「403 Forbidden」となることを確認する",
            "S3バケットをパブリック公開設定にし、CloudFrontを経由せずに直接S3のURLにアクセスしても動画が見られることを確認する",
            "有料会員のアカウントでログインし、ブラウザのCookieを全て削除しても動画が再生され続けることを確認する",
            "署名付きURLの発行ロジックは複雑なためテストを省略し、Basic認証をかけたテスト環境で代用確認を行う"
        ],
        "answer": [
            "署名付きURLを発行し、有効期限内であれば動画が再生できること、および有効期限が切れた後や署名の一部を改ざんしたURLでは「403 Forbidden」となることを確認する"
        ],
        "explanation": "【解説】\n署名付きURL/Cookieのテストでは、正当な署名でのアクセス成功（ポジティブテスト）だけでなく、期限切れや改ざん署名でのアクセス拒否（ネガティブテスト）の確認が必須です。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol125.json)
q2_fin = [
    {
        "id": "Q2-FIN-V125-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】債券の償還（Redemption）処理。\n社債管理システムにおいて、満期日（Maturity Date）を迎えた債券の償還処理をテストしたい。\n元本返済と利払いの整合性を検証するために確認すべき事項はどれか。",
        "options": [
            "満期日において、額面金額（元本）が全額返済されるとともに、最終回の利息支払いが正しく計算され、両方が合算されて投資家の口座に入金されること",
            "満期日になると債券データが物理的に削除され、システム上から完全に消滅すること",
            "元本の返済は行われるが、最終回の利息は次回の利払日に後回しにされること",
            "償還処理は銀行側のシステムで行われるため、社債管理システム側ではステータスを「償還済」に変更するだけで、金額の計算は行わないこと"
        ],
        "answer": [
            "満期日において、額面金額（元本）が全額返済されるとともに、最終回の利息支払いが正しく計算され、両方が合算されて投資家の口座に入金されること"
        ],
        "explanation": "【解説】\n満期償還（Redemption at Maturity）では、元本の返還と「最後の利払い（Last Coupon）」が同時に行われます。元本だけ、あるいは利息抜けがないかを確認する必要があります。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol125.json": q3_gen,
    "ch1_general_vol125.json": q1_gen,
    "ch2_general_vol125.json": q2_gen,
    "ch1_aws_vol125.json": q1_aws,
    "ch2_finance_vol125.json": q2_fin
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
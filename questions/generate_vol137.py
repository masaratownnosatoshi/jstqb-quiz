import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.137 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol137.json)
q3_gen = [
    {
        "id": "Q3-GEN-V137-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テスト進捗管理と「Sカーブ」。\nテスト実行フェーズにおいて、消化予定線（計画）に対して実績線が下回る乖離が発生し始めた。\nこのまま放置すると納期遅延になることが予測される場合、テストマネージャが最初に取るべきコントロールアクションはどれか。",
        "options": [
            "直ちにテスターを増員し、休日出勤を命令して遅れを一気に取り戻す計画に変更する",
            "遅延の原因（バグ多発によるブロック、環境トラブル、要員スキル不足など）を調査・分析し、原因に応じた対策を立案してステークホルダーと調整する",
            "テスト消化数を稼ぐために、実行が簡単で時間がかからないテストケースを優先的に実施するよう指示を出し、見かけ上の進捗率を上げる",
            "進捗報告書の数値を書き換え、計画通りに進んでいるように見せかけて、開発チームがバグ修正を終えるまでの時間を稼ぐ"
        ],
        "answer": [
            "遅延の原因（バグ多発によるブロック、環境トラブル、要員スキル不足など）を調査・分析し、原因に応じた対策を立案してステークホルダーと調整する"
        ],
        "explanation": "【解説】\n進捗遅れへの対策は「原因分析」から始まります。原因がバグによるブロックなら開発側の対応が必要であり、単なる増員では解決しない場合も多いため、まずは分析が最優先です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol137.json)
q1_gen = [
    {
        "id": "Q1-GEN-V137-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】受け入れテスト駆動開発（ATDD）。\nアジャイルチームにおいて、開発着手前に「受け入れテスト（Acceptance Test）」を定義することで、要件の曖昧さを排除しようとしている。\nATDDのプロセスにおいて、受け入れ基準を作成する際の適切なコラボレーション方法はどれか。",
        "options": [
            "プロダクトオーナー、開発者、テスターの「3者（Three Amigos）」が集まり、具体的な事例やシナリオについて議論しながら共同でテストケースを作成する",
            "テスターが一人で仕様書を読み込み、開発者がコードを書き始める前に全てのテストケースを完成させて、開発者にドキュメントとして手渡す",
            "プロダクトオーナーが要件定義書を書き、開発者はそれを読むだけで質問はせず、テスターはリリース直前まで関与しない",
            "開発者が実装を行い、その動作に合わせて後から受け入れ基準を書き起こすことで、常にテストが合格する状態を保つ"
        ],
        "answer": [
            "プロダクトオーナー、開発者、テスターの「3者（Three Amigos）」が集まり、具体的な事例やシナリオについて議論しながら共同でテストケースを作成する"
        ],
        "explanation": "【解説】\nATDDの核心は「Three Amigos（3人のアミーゴ）」による協調作業です。ビジネス（PO）、開発、テストの3つの視点を統合し、実装前に共通理解を形成します。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol137.json)
q2_gen = [
    {
        "id": "Q2-GEN-V137-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】直交表（Orthogonal Array）の選定。\n4つのパラメータがあり、それぞれが3つの値（水準）を持つ設定画面の組み合わせテストを行いたい。\n2因子間の網羅率100%を目指すために「L9直交表（3の4乗）」を使用する場合、この直交表が保証する数学的な特性はどれか。",
        "options": [
            "任意の2つの列を取り出したとき、すべての値の組み合わせ（3×3＝9通り）が、同じ回数（この場合は1回）ずつ現れること",
            "すべてのパラメータのすべての値が少なくとも1回は登場し、かつランダムに組み合わされていること",
            "3つの因子を同時に変化させたときの組み合わせ（3の3乗＝27通り）が全て網羅されていること",
            "バグが出る可能性が高い組み合わせをAIが予測し、優先的に上位に配置されていること"
        ],
        "answer": [
            "任意の2つの列を取り出したとき、すべての値の組み合わせ（3×3＝9通り）が、同じ回数（この場合は1回）ずつ現れること"
        ],
        "explanation": "【解説】\n直交表の定義は「任意の2列において、すべてのペアが同数回出現する」ことです。これにより、最小のケース数で2因子間網羅（Pairwise）をバランス良く実現できます。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol137.json)
q1_aws = [
    {
        "id": "Q1-AWS-V137-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】WAFによるSQLインジェクション対策のテスト。\nCloudFrontにAWS WAFを適用し、SQLインジェクション攻撃をブロックするルール（AWSManagedRulesSQLiRuleSet）を設定した。\nこの設定が正しく機能していることを確認するための検証方法はどれか。",
        "options": [
            "通常の正常なリクエストだけを送信し、Webサイトが正常に表示されることだけを確認する",
            "curlコマンドやBurp Suiteなどのツールを使用し、URLパラメータやヘッダーにSQL攻撃パターン（例：' OR 1=1 --）を含んだリクエストを送信して、403 Forbiddenが返ることを確認する",
            "データベースのログを確認し、不正なSQLクエリが実行されていないかを目視でチェックする",
            "WAFの設定画面で「ブロックモード」がオンになっていることを確認するだけで、実際のリクエスト送信テストは省略する"
        ],
        "answer": [
            "curlコマンドやBurp Suiteなどのツールを使用し、URLパラメータやヘッダーにSQL攻撃パターン（例：' OR 1=1 --）を含んだリクエストを送信して、403 Forbiddenが返ることを確認する"
        ],
        "explanation": "【解説】\nWAFのテストでは、実際に攻撃パターンを含むリクエストを投げて「遮断されること（Positive Block）」を確認する必要があります。単なる設定確認では不十分です。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol137.json)
q2_fin = [
    {
        "id": "Q2-FIN-V137-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】債券の経過利子（Accrued Interest）。\n利払日の途中で債券を売買する場合、買い手は売り手に対して、前回利払日から受渡日までの期間に応じた「経過利子」を支払う必要がある。\nこの経過利子の計算において、一般的に使用される日数の数え方と、検証時の注意点はどれか。",
        "options": [
            "経過利子はサービスとして免除されるのが一般的であるため、常に0円になることを確認する",
            "実際の日数（Actual）ではなく、1ヶ月を常に30日として計算する方式が多いため、31日の月であっても30日分の利息として計算されているかを確認する（ただし商品による）",
            "受渡日が属する月の「前月の末日」までの利息を計算し、当月分の日数は切り捨てて計算されていることを確認する",
            "経過利子は税金の計算対象外であるため、源泉徴収税額が引かれずに全額が支払われることを確認する"
        ],
        "answer": [
            "実際の日数（Actual）ではなく、1ヶ月を常に30日として計算する方式が多いため、31日の月であっても30日分の利息として計算されているかを確認する（ただし商品による）"
        ],
        "explanation": "【解説】\n債券の経過利子計算では、しばしば「30/360」などの日数計算慣行（Day Count Convention）が適用されます。実日数（Act）なのか30日ベースなのか、仕様と一致しているかの検証が重要です。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol137.json": q3_gen,
    "ch1_general_vol137.json": q1_gen,
    "ch2_general_vol137.json": q2_gen,
    "ch1_aws_vol137.json": q1_aws,
    "ch2_finance_vol137.json": q2_fin
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
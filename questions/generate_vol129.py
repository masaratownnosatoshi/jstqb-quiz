import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.129 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol129.json)
q3_gen = [
    {
        "id": "Q3-GEN-V129-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テスト終了報告書（Test Summary Report）の目的。\nプロジェクト終了時に作成するテスト終了報告書において、ステークホルダー（経営層や顧客）が最も関心を持ち、かつ記載すべき主要な内容はどれか。",
        "options": [
            "発見されたすべてのバグのID、タイトル、再現手順、ログを全件リストアップした詳細な一覧表",
            "テスト活動を通じて得られた、個々の開発者のコーディング能力や性格に関する個人的な評価とランク付け",
            "計画に対する実施状況の要約、残存リスク、およびリリース可否判断（Go/No-Go）を行うための品質評価と推奨事項",
            "次期プロジェクトのための詳細なテストケース再利用計画書と、テストツールのライセンス更新費用見積もり"
        ],
        "answer": [
            "計画に対する実施状況の要約、残存リスク、およびリリース可否判断（Go/No-Go）を行うための品質評価と推奨事項"
        ],
        "explanation": "【解説】\nテスト終了報告書の主目的は、ステークホルダーが「リリースして良いか」を判断するための情報提供です。詳細なバグ一覧ではなく、品質の要約とリスク評価が求められます。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol129.json)
q1_gen = [
    {
        "id": "Q1-GEN-V129-01",
        "chapter": "第1章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】探索的テスト（Exploratory Testing）の適用局面。\nあるプロジェクトにおいて、仕様書が不完全で頻繁に変更される状況下で、短期間でのテストが求められている。\nこの状況で、事前に手順書を作成するスクリプトテストよりも探索的テストを選択すべき理由はどれか。",
        "options": [
            "テスト実行と並行してテスト設計（学習）を行うため、ドキュメント作成のオーバーヘッドを最小化しつつ、変化する仕様に柔軟に対応できるから",
            "探索的テストは未経験者でも実施可能であり、テスト担当者のスキルレベルに関わらず一定の成果が出せる手法だから",
            "テストの再現性を完全に保証できるため、将来的な回帰テストの自動化に向けた準備として最適だから",
            "テストの進捗管理（消化件数）を定量的に行うことが容易であり、管理者が進捗を正確に把握しやすいから"
        ],
        "answer": [
            "テスト実行と並行してテスト設計（学習）を行うため、ドキュメント作成のオーバーヘッドを最小化しつつ、変化する仕様に柔軟に対応できるから"
        ],
        "explanation": "【解説】\n探索的テストの強みは「学習・設計・実行の同時進行」です。仕様が曖昧または流動的な状況で、ドキュメント保守コストを省きつつバグを見つけるのに適しています。",
        "tags": ["第1章", "一般", "シナリオ", "K4"]
    }
]

# 3. 第2章 一般 (ch2_general_vol129.json)
q2_gen = [
    {
        "id": "Q2-GEN-V129-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ユーザーストーリーの受け入れテスト。\nアジャイル開発において「Given/When/Then（前提/もし/ならば）」の形式で記述された受け入れ基準（Acceptance Criteria）を検証したい。\nこの形式に基づいたテストアプローチとして正しいものはどれか。",
        "options": [
            "Given（前提）条件を無視し、When（操作）とThen（結果）の組み合わせだけをランダムに実行して、予期せぬ挙動を探す",
            "システム内部のデータベース構造やAPIのレスポンスタイムが、Givenで定義された非機能要件を満たしているかを計測する",
            "記述されたシナリオ通りにシステムを操作し、特定の前提条件下でアクションを実行した際に、期待される振る舞いや結果が得られるかを確認する",
            "ユーザーストーリーの文章量や誤字脱字をチェックし、ドキュメントとしての品質を静的に検証する"
        ],
        "answer": [
            "記述されたシナリオ通りにシステムを操作し、特定の前提条件下でアクションを実行した際に、期待される振る舞いや結果が得られるかを確認する"
        ],
        "explanation": "【解説】\nGherkin記法（Given/When/Then）は、振る舞い駆動開発（BDD）におけるテストシナリオの標準形式です。この記述通りに振る舞うかを検証するのが受け入れテストの基本です。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol129.json)
q1_aws = [
    {
        "id": "Q1-AWS-V129-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】CloudFormationのドリフト検出。\nIaC（CloudFormation）で管理されているセキュリティグループの設定が、誰かの手動操作によって変更された疑いがある。\nテンプレートと実際のリソース設定との差異（構成の乖離）を確認するための正しい方法はどれか。",
        "options": [
            "CloudFormationコンソールまたはCLIから「ドリフトの検出（Detect Drift）」を実行し、リソースの現在のプロパティ値とテンプレートの定義値を比較する",
            "スタックを一度削除してから再作成し、変更された部分が元に戻るかどうかを確認する",
            "AWS CloudTrailのログを過去1年分すべてダウンロードし、セキュリティグループに対するAPIコールを目視で検索する",
            "AWS Configの管理画面を開き、すべてのリソースについて「再評価」ボタンを手動でクリックする"
        ],
        "answer": [
            "CloudFormationコンソールまたはCLIから「ドリフトの検出（Detect Drift）」を実行し、リソースの現在のプロパティ値とテンプレートの定義値を比較する"
        ],
        "explanation": "【解説】\nCloudFormationには、スタック外で行われた変更を検知する「ドリフト検出機能」があります。これにより、テンプレートと実環境の差分を具体的に特定できます。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol129.json)
q2_fin = [
    {
        "id": "Q2-FIN-V129-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】定期預金の利息計算（単利 vs 複利）。\n定期預金システムのテストにおいて、「期間3年、年利1%」の商品について、単利（Simple Interest）と複利（Compound Interest）の計算結果の違いを検証したい。\n2年目の利息計算ロジックとして、正しい検証ポイントはどれか。",
        "options": [
            "単利の場合も複利の場合も、2年目の利息は「当初の元本 × 1%」で計算され、結果は同額になることを確認する",
            "単利の場合は「当初の元本 × 1%」で計算されるが、複利の場合は「（当初元本＋1年目の税引後利息）× 1%」で計算され、複利の方が受取額が多くなることを確認する",
            "複利計算は複雑であるため、システム上は単利と同じロジックで実装し、満期時に差額を「調整金」として一括付与することを確認する",
            "単利の場合は毎年利息が支払われるが、複利の場合は満期まで利息が計算されず、元本が変わらないことを確認する"
        ],
        "answer": [
            "単利の場合は「当初の元本 × 1%」で計算されるが、複利の場合は「（当初元本＋1年目の税引後利息）× 1%」で計算され、複利の方が受取額が多くなることを確認する"
        ],
        "explanation": "【解説】\n複利（Compound Interest）の特徴は「利息が利息を生む」ことです。2年目以降、元本に前年の利息（税引後）が組み入れられる（元加される）かどうかが、単利との決定的な違いであり、テストの要点です。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol129.json": q3_gen,
    "ch1_general_vol129.json": q1_gen,
    "ch2_general_vol129.json": q2_gen,
    "ch1_aws_vol129.json": q1_aws,
    "ch2_finance_vol129.json": q2_fin
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
import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.128 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol128.json)
q3_gen = [
    {
        "id": "Q3-GEN-V128-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テスト終了基準と残存リスク。\nリリース予定日が迫っているが、優先度「低」のバグが数件修正されずに残っている。\nテスト終了基準（Exit Criteria）としては「重大なバグがないこと」と定義されている。\nテストマネージャが取るべき行動として、最も適切なものはどれか。",
        "options": [
            "残っているバグがシステムの重要機能に影響しないことを確認し、ステークホルダーと合意した上で、残存リスクとして記録してテストを終了する",
            "すべてのバグを修正しない限りリリースは認められないため、独断でリリース延期を決定し、開発チームに徹夜での修正を命じる",
            "優先度「低」のバグであれば顧客に気づかれることはないため、バグ管理システムから削除して「バグゼロ」の状態にしてからリリースする",
            "テスト終了基準を満たしていないが、リリース日は絶対であるため、バグの存在を報告書には記載せず、口頭だけで開発リーダーに伝えてリリースする"
        ],
        "answer": [
            "残っているバグがシステムの重要機能に影響しないことを確認し、ステークホルダーと合意した上で、残存リスクとして記録してテストを終了する"
        ],
        "explanation": "【解説】\nテスト終了は「バグゼロ」を意味しません。終了基準（重大なバグがない）を満たし、残存リスク（既知の軽微なバグ）についてステークホルダーの合意（受容）が得られれば、リリース可能です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol128.json)
q1_gen = [
    {
        "id": "Q1-GEN-V128-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】デシジョンテーブル（決定表）の圧縮。\n会員ランク（ゴールド、シルバー、一般）による割引判定ロジックにおいて、「ゴールド会員」であれば、購入金額に関わらず常に「20%割引」が適用される仕様である。\nこのロジックをデシジョンテーブルで表現する際、表を簡潔にするための適切な記述方法はどれか。",
        "options": [
            "条件「会員ランク＝ゴールド」の列において、条件「購入金額」のセルに「N/A（不問）」または「－（ハイフン）」を記述し、購入金額ごとの列を統合する",
            "購入金額の条件（例：1万円以上、1万円未満など）ごとに列をすべて分割し、ゴールド会員の列を複数作成して網羅性をアピールする",
            "ゴールド会員は割引率が固定であり条件分岐がないため、デシジョンテーブルには記述せず、備考欄にテキストで補足するだけに留める",
            "条件「購入金額」のセルに「全額」と記述し、すべての金額パターンをテストケースとして生成するようにツールを設定する"
        ],
        "answer": [
            "条件「会員ランク＝ゴールド」の列において、条件「購入金額」のセルに「N/A（不問）」または「－（ハイフン）」を記述し、購入金額ごとの列を統合する"
        ],
        "explanation": "【解説】\n結果に影響を与えない条件は「不問（Don't Care）」として扱い、列を統合（Collapse）するのがデシジョンテーブルの定石です。これにより表のサイズを削減し、可読性を高めます。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol128.json)
q2_gen = [
    {
        "id": "Q2-GEN-V128-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】ペアワイズ法（オールペア法）の限界。\nOS、ブラウザ、Javaバージョンの組み合わせテストをペアワイズ法で設計・実施したが、リリース後に「特定の3つの組み合わせ（Win + Chrome + Java8）」でのみ発生するバグが見つかった。\nこの事象に対するテスト技法の観点からの分析として、正しい記述はどれか。",
        "options": [
            "ペアワイズ法は「2因子間の相互作用」を網羅する技法であり、3因子以上の特定の組み合わせで発生するバグ（高次相互作用）については保証範囲外であるため、技法の特性上起こり得る事象である",
            "ペアワイズ法を使用すれば全てのバグを検出できるはずであるため、これはテストケース生成ツールのアルゴリズムにバグがあったか、パラメータ設定に誤りがあったと考えられる",
            "3因子の組み合わせバグが出たということは、直交表（Orthogonal Array）を使っていれば防げたはずであり、ペアワイズ法を選定したこと自体が間違いであった",
            "このバグは単一の因子（Java8）に起因するものであり、組み合わせテストの問題ではなく、境界値分析の漏れである"
        ],
        "answer": [
            "ペアワイズ法は「2因子間の相互作用」を網羅する技法であり、3因子以上の特定の組み合わせで発生するバグ（高次相互作用）については保証範囲外であるため、技法の特性上起こり得る事象である"
        ],
        "explanation": "【解説】\nペアワイズ法（2-wise）は、任意の「2つの因子」の組み合わせを網羅します。3つ以上の特定条件が重なった時にのみ起きるバグは検出できないリスクがあり、これは技法の仕様（限界）です。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol128.json)
q1_aws = [
    {
        "id": "Q1-AWS-V128-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】CloudTrailログの完全性検証。\n監査部門から「AWSの操作ログ（CloudTrail）が管理者によって改ざんや削除されていないことを証明してほしい」という要求があった。\nこの要件を満たすために有効化すべきCloudTrailの機能はどれか。",
        "options": [
            "ログファイルの検証（Log File Validation）機能を有効化し、ダイジェストファイルを用いてログのハッシュチェーンを検証できるようにする",
            "S3バケットのバージョニング機能を有効化し、ログファイルが上書きされた場合に古いバージョンを復元できるようにする",
            "AWS KMSによるログファイルの暗号化（SSE-KMS）を有効化し、鍵を持っていないユーザーがログを読めないようにする",
            "Amazon GuardDutyを有効化し、ログに対する不審なアクセスパターンを検知してアラートを発砲する"
        ],
        "answer": [
            "ログファイルの検証（Log File Validation）機能を有効化し、ダイジェストファイルを用いてログのハッシュチェーンを検証できるようにする"
        ],
        "explanation": "【解説】\n「改ざんされていないことの証明（完全性）」には、CloudTrailの「Log File Validation」を使用します。ダイジェストファイル（ハッシュ値）により、ログの削除や変更を数学的に検知できます。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol128.json)
q2_fin = [
    {
        "id": "Q2-FIN-V128-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】株式の配当落ち（Ex-Dividend）処理。\n証券システムにおいて、株式の配当権利落ち日（Ex-Date）における処理をテストしたい。\n権利付き最終日（Cum-Date）の翌営業日である権利落ち日に、システム上で確認すべき株価と権利の挙動はどれか。",
        "options": [
            "基準値段（前日終値）から予想配当金分が差し引かれて（下落して）取引が開始されること、および前日までに保有していた株主に対して配当受領権が確定していること",
            "配当金の支払いは数ヶ月後であるため、株価には何の影響もなく、前日終値と同じ価格から取引が開始されること",
            "権利落ち日になった瞬間に、投資家の証券口座残高に配当金相当額が現金として即時入金されていること",
            "配当落ちに伴い保有株数が自動的に増加し、株式分割と同じ処理が行われていること"
        ],
        "answer": [
            "基準値段（前日終値）から予想配当金分が差し引かれて（下落して）取引が開始されること、および前日までに保有していた株主に対して配当受領権が確定していること"
        ],
        "explanation": "【解説】\n権利落ち日には、理論上「配当金の分だけ株価が下がる（配当落ち）」という現象が発生します。システム的には、基準値の調整と、権利確定（株主名簿の固定）が正しく行われるかを確認します。",
        "tags": ["第2章", "金融", "シナリオ", "K3"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol128.json": q3_gen,
    "ch1_general_vol128.json": q1_gen,
    "ch2_general_vol128.json": q2_gen,
    "ch1_aws_vol128.json": q1_aws,
    "ch2_finance_vol128.json": q2_fin
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
import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.126 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol126.json)
q3_gen = [
    {
        "id": "Q3-GEN-V126-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】インシデント管理と回帰テスト。\n重大なバグが報告され、開発チームが修正パッチを作成した。テストチームがこの修正を確認する際、実施すべき一連のアクションとして、プロセス上最も適切なものはどれか。",
        "options": [
            "修正された箇所が正しく動作することを確認する「確認テスト（Re-testing）」を行い、その後に周辺機能への悪影響がないかを確認する「回帰テスト（Regression Testing）」を実施する",
            "回帰テストは工数がかかるため省略し、修正された箇所の確認テストのみを行って、バグチケットをクローズする",
            "修正によって別のバグが発生している可能性が高いため、確認テストは行わずに、システム全体の全量テスト（フルリグレッション）のみを実施する",
            "開発者が「修正完了」と言っている以上、テストチームは何もせずにチケットをクローズし、信頼関係を重視する"
        ],
        "answer": [
            "修正された箇所が正しく動作することを確認する「確認テスト（Re-testing）」を行い、その後に周辺機能への悪影響がないかを確認する「回帰テスト（Regression Testing）」を実施する"
        ],
        "explanation": "【解説】\nバグ修正後は、まず「直ったことの確認（Re-testing）」を行い、次に「壊していないことの確認（Regression Testing）」を行うのが標準的なプロセスです。片方だけでは不十分です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol126.json)
q1_gen = [
    {
        "id": "Q1-GEN-V126-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ユーザビリティテストの評価指標。\nECサイトの購入フロー改善プロジェクトにおいて、ユーザーが商品をカートに入れてから購入完了するまでの「効率性」を測定したい。\nこの目的に最も適した定量的な指標はどれか。",
        "options": [
            "タスク完了にかかった時間（Task Time）や、クリック数・画面遷移数などの操作ステップ数を計測する",
            "ユーザーに対して「このサイトは使いやすかったですか？」というアンケートを行い、5段階評価の平均点を算出する",
            "サイトのデザインが美しいかどうかを色彩心理学の専門家に評価してもらい、美的スコアを算出する",
            "サーバーのCPU使用率やメモリ消費量を計測し、システムリソースの観点から効率性を評価する"
        ],
        "answer": [
            "タスク完了にかかった時間（Task Time）や、クリック数・画面遷移数などの操作ステップ数を計測する"
        ],
        "explanation": "【解説】\n「効率性（Efficiency）」は、ユーザーがゴールに到達するまでのリソース（時間や労力）で測ります。アンケートは「満足度」、サーバー負荷は「性能」の指標です。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol126.json)
q2_gen = [
    {
        "id": "Q2-GEN-V126-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】同値分割法（Equivalence Partitioning）の無効同値クラス。\n年齢入力欄（1〜100歳の整数）のテストケースを作成する際、仕様には明記されていないが、システムの実装上リスクとなり得る「無効同値クラス」のデータとして、考慮すべきものはどれか。",
        "options": [
            "文字データ（例：「あいうえお」）や記号、空文字（NULL）、および浮動小数点数（例：10.5）といった、整数以外のデータ型",
            "1〜100の範囲内にある「50」や「80」といった、正常な整数データ",
            "境界値である「1」と「100」、およびその隣の「0」と「101」",
            "開発者がテスト済みであると主張する「20」や「30」といった代表的な値"
        ],
        "answer": [
            "文字データ（例：「あいうえお」）や記号、空文字（NULL）、および浮動小数点数（例：10.5）といった、整数以外のデータ型"
        ],
        "explanation": "【解説】\n同値分割では、範囲外の数値（0や101）だけでなく、そもそも「型が違う（文字、小数など）」入力も無効同値クラスとして扱います。これらはバリデーション漏れによるクラッシュの原因となりやすいです。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol126.json)
q1_aws = [
    {
        "id": "Q1-AWS-V126-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】IAMポリシーの評価論理（Deny優先）。\nあるIAMユーザーに対し、「S3のフルアクセス許可（Allow）」ポリシーと、「特定のバケット（Bucket-A）へのアクセス拒否（Deny）」ポリシーの両方がアタッチされている。\nこのユーザーがBucket-Aにアクセスしようとした場合の結果として、正しいものはどれか。",
        "options": [
            "明示的な拒否（Explicit Deny）が優先されるため、アクセスは拒否される",
            "許可（Allow）の権限の方が強いため、アクセスは許可される",
            "ポリシーのアタッチ順序に依存し、後にアタッチされた方のポリシーが適用される",
            "競合するポリシーがある場合、AWSアカウントのルートユーザーの承認が必要となる"
        ],
        "answer": [
            "明示的な拒否（Explicit Deny）が優先されるため、アクセスは拒否される"
        ],
        "explanation": "【解説】\nIAMポリシーの評価ロジックでは、「明示的な拒否（Explicit Deny）」が常に最優先されます。どんなに強力な許可があっても、一つでもDenyがあれば拒否となります。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol126.json)
q2_fin = [
    {
        "id": "Q2-FIN-V126-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】外貨預金の利息計算と為替レート適用。\n外貨普通預金の利息計算において、利息入金日（Interest Payment Date）の為替レートを用いて円換算額を算出する仕様となっている。\nテストデータの準備において、特に注意して検証すべき「レート適用タイミング」のケースはどれか。",
        "options": [
            "利息計算期間中の平均レートを算出し、それを用いて計算されていることを確認する",
            "利息入金日が休日であった場合、直前の営業日のレート（仲値：TTM）が適用されるか、あるいは翌営業日のレートが適用されるか、銀行規定に基づいた正しい日付のレートが使われているかを確認する",
            "常に「1ドル＝100円」の固定レートが適用されていることを確認し、市場変動の影響を受けないようにする",
            "利息計算はリアルタイムに行われるため、入金処理が実行された瞬間の秒単位のレートが適用されていることを確認する"
        ],
        "answer": [
            "利息入金日が休日であった場合、直前の営業日のレート（仲値：TTM）が適用されるか、あるいは翌営業日のレートが適用されるか、銀行規定に基づいた正しい日付のレートが使われているかを確認する"
        ],
        "explanation": "【解説】\n為替レートは営業日ごとに1回（公表仲値など）決まるのが一般的です。入金日が休日の場合、「いつのレートを使うか（前営業日or翌営業日）」は仕様バグの多発ポイントです。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol126.json": q3_gen,
    "ch1_general_vol126.json": q1_gen,
    "ch2_general_vol126.json": q2_gen,
    "ch1_aws_vol126.json": q1_aws,
    "ch2_finance_vol126.json": q2_fin
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
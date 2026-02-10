import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.107 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol107.json)
q3_gen = [
    {
        "id": "Q3-GEN-V107-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストプロセス改善（TPI Next）の優先順位付け。\n現在のテストプロセスは「場当たり的」で、ドキュメントも標準化されていない。\n限られたリソースで改善を始めるにあたり、最初に手を付けるべきキーエリアとして最も推奨されるものはどれか。",
        "options": [
            "テスト自動化ツールを導入し、手動テストを全て廃止して効率化を図る（プロセスが未成熟な状態での自動化は失敗する）",
            "テスト戦略（Strategy）とテスト方法論（Methodology）を定義し、プロジェクト全体で「どのようにテストするか」の共通認識と標準を作る",
            "詳細なテストケース管理ツールを購入し、すべてのテストケースを細かく記録することを義務付ける（管理負荷が増えすぎて破綻する）",
            "テスト担当者のスキル評価を行い、スキルの低いメンバーをプロジェクトから外す（リソース不足が悪化する）"
        ],
        "answer": [
            "テスト戦略（Strategy）とテスト方法論（Methodology）を定義し、プロジェクト全体で「どのようにテストするか」の共通認識と標準を作る"
        ],
        "explanation": "【解説】\n改善の初期段階（制御されていない状態）では、まず「標準（どうやるか）」を確立することが最優先です。ツール導入や詳細管理は、プロセスが安定してから行うべきです。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol107.json)
q1_gen = [
    {
        "id": "Q1-GEN-V107-01",
        "chapter": "第1章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】テスト工数の見積もり（三点見積もり）。\nある機能のテスト実行工数について、楽観値（O）=10人日、最頻値（M）=16人日、悲観値（P）=28人日と見積もられた。\nPERT（プログラム評価レビュー手法）の加重平均式を用いて算出した見積もり工数はいくつか。",
        "options": [
            "17人日（計算式：(10 + 4×16 + 28) ÷ 6 = 102 ÷ 6 = 17）",
            "18人日（単純平均：(10 + 16 + 28) ÷ 3 = 18）",
            "16人日（最頻値をそのまま採用）",
            "20人日（安全を見て悲観値に近い値を採用）"
        ],
        "answer": [
            "17人日（計算式：(10 + 4×16 + 28) ÷ 6 = 102 ÷ 6 = 17）"
        ],
        "explanation": "【解説】\nPERTの式は「(O + 4M + P) / 6」です。\n(10 + 64 + 28) / 6 = 102 / 6 = 17人日となります。最頻値に重みを置くことで、より確度の高い見積もりが可能です。",
        "tags": ["第1章", "一般", "シナリオ", "K4"]
    }
]

# 3. 第2章 一般 (ch2_general_vol107.json)
q2_gen = [
    {
        "id": "Q2-GEN-V107-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】状態遷移テストの設計。\n「注文ステータス」の遷移をテストしたい。ステータスは「注文済」「入金済」「発送済」「キャンセル」「完了」がある。\n無効な遷移（例：「注文済」からいきなり「完了」になる等）がシステム的にブロックされることを確認するためのテスト設計アプローチはどれか。",
        "options": [
            "全ての有効な遷移（Happy Path）だけを網羅したテストケースを作成し、正常に遷移することを確認する（不正遷移のガードを確認できない）",
            "状態遷移図または状態遷移表（N/A含む）を作成し、許可されていない遷移ルート（N/Aセル）に対してイベントを発行し、エラーになるか遷移しないことを確認する（ネガティブテスト）",
            "ランダムにボタンを連打して、ステータスがおかしくならないかを目視で確認する（網羅性がなく再現性も低い）",
            "データベースの値を直接書き換えて、無効なステータスに変更できるか試す（アプリケーションロジックのテストになっていない）"
        ],
        "answer": [
            "状態遷移図または状態遷移表（N/A含む）を作成し、許可されていない遷移ルート（N/Aセル）に対してイベントを発行し、エラーになるか遷移しないことを確認する（ネガティブテスト）"
        ],
        "explanation": "【解説】\n状態遷移テストでは、有効な遷移（0-switch coverage）だけでなく、無効な遷移（Negative test）がブロックされることを確認することが重要です。状態遷移表の「N/A（斜線）」部分がテスト対象になります。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol107.json)
q1_aws = [
    {
        "id": "Q1-AWS-V107-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】CloudFrontのキャッシュ動作テスト。\nWebサイトの更新を行ったが、ユーザーから「古い画像が表示され続けている」という報告があった。\nCloudFrontのキャッシュ設定（TTL）や無効化（Invalidation）の動作を検証し、解決するための正しい手順はどれか。",
        "options": [
            "CloudFrontのディストリビューションを一度削除し、再作成することでキャッシュをクリアする（ダウンタイムが発生し、設定も消えるため不適切）",
            "ブラウザのキャッシュをクリアするよう全ユーザーに通知し、サーバー側の設定は変更しない（根本解決になっていない）",
            "特定のファイルのURLに対して「Invalidation（無効化リクエスト）」を作成・実行し、その後すぐにアクセスして新しいファイルが取得できることを確認する",
            "TTL設定を「0」に変更して、今後一切キャッシュしないように設定変更する（パフォーマンスが低下し、CDNのメリットがなくなる）"
        ],
        "answer": [
            "特定のファイルのURLに対して「Invalidation（無効化リクエスト）」を作成・実行し、その後すぐにアクセスして新しいファイルが取得できることを確認する"
        ],
        "explanation": "【解説】\n古いキャッシュが残っている場合の正しい対処は「Invalidation（無効化）」です。テストでは、更新→Invalidation→確認のフローが正しく機能するかを検証します。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol107.json)
q2_fin = [
    {
        "id": "Q2-FIN-V107-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】帳票の数値整合性テスト。\n「月次損益計算書」のシステムテストにおいて、画面上の表示金額と、PDF帳票の金額、およびCSVダウンロードデータの金額がすべて一致していることを保証したい。\n効率的かつ漏れのない検証方法はどれか。",
        "options": [
            "画面、PDF、CSVを目視で見比べ、主要な項目（合計金額など）が合っていれば良しとする（目視では細かい数字の見落としが発生する）",
            "画面、PDF、CSVのデータをそれぞれテキストまたは構造化データとして抽出し、比較ツールを用いて全項目の値を機械的に突合（Diff）するテストスクリプトを作成・実行する",
            "CSVデータだけを確認し、CSVが合っていればPDFも合っているはずだと仮定してテストを省略する（帳票生成ロジックのバグを見逃す）",
            "経理担当者に実際に使ってもらい、間違いがあれば報告してもらう運用にする（テスト工程での品質保証責任の放棄）"
        ],
        "answer": [
            "画面、PDF、CSVのデータをそれぞれテキストまたは構造化データとして抽出し、比較ツールを用いて全項目の値を機械的に突合（Diff）するテストスクリプトを作成・実行する"
        ],
        "explanation": "【解説】\n金融帳票の整合性チェックは「機械的な全件比較」が鉄則です。PDFからのテキスト抽出ライブラリなどを活用し、自動化することで精度と効率を両立させます。",
        "tags": ["第2章", "金融", "シナリオ", "K3"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol107.json": q3_gen,
    "ch1_general_vol107.json": q1_gen,
    "ch2_general_vol107.json": q2_gen,
    "ch1_aws_vol107.json": q1_aws,
    "ch2_finance_vol107.json": q2_fin
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
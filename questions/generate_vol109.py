import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.109 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol109.json)
q3_gen = [
    {
        "id": "Q3-GEN-V109-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストプロセス成熟度診断（アセスメント）。\n組織の現状（As-Is）を把握するために、TMMiまたはTPI Nextに基づいたアセスメントを実施したい。\n現状を正確に評価するためのアプローチとして、最も信頼性が高いものはどれか。",
        "options": [
            "全テスト担当者にWebアンケートを一斉配信し、自己評価スコア（1〜5点）の平均値を算出して、それを組織の成熟度レベルと認定する（主観的すぎて信頼性が低い）",
            "アセッサー（評価者）が主要なステークホルダーにインタビューを行い、実際の成果物（テスト計画書や報告書）を査読して、モデルの基準と照らし合わせて証拠ベースで判定する",
            "過去のプロジェクトのバグ摘出数とテスト工数のデータだけを統計分析し、数値が良いプロジェクトを「成熟度が高い」と機械的に判定する（プロセスの質を見ていない）",
            "外部の有名コンサルタントを呼び、現場を見ずにマネージャの話だけを聞いて、業界平均と比較したレポートを作成してもらう（現場の実態と乖離する）"
        ],
        "answer": [
            "アセッサー（評価者）が主要なステークホルダーにインタビューを行い、実際の成果物（テスト計画書や報告書）を査読して、モデルの基準と照らし合わせて証拠ベースで判定する"
        ],
        "explanation": "【解説】\n成熟度診断は「客観的な証拠（Evidence）」が必要です。自己申告のアンケートではなく、インタビューとドキュメントレビューによる事実確認が必須です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol109.json)
q1_gen = [
    {
        "id": "Q1-GEN-V109-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】アジャイル見積もり（プランニングポーカー）。\nあるストーリーの規模見積もりで、チームメンバーの出したポイントが「3, 5, 5, 20」と大きく割れた。\nスクラムマスターまたはテスト担当者が促すべき次のアクションはどれか。",
        "options": [
            "議論をしていると時間がもったいないので、全員の出した数字の平均値（8.25なので8）を採用し、次のストーリーに進む（認識のズレを放置するリスク）",
            "最も大きな数字（20）を出したメンバーと、最も小さな数字（3）を出したメンバーにそれぞれの根拠や懸念点を説明してもらい、認識を合わせてから再投票を行う",
            "多数決の原理に従い、最も票が多かった「5」を採用して、少数派の意見は切り捨てる（重要なリスクが見落とされる可能性がある）",
            "見積もりが割れるのは仕様が不明確な証拠であるため、このストーリーは今回のスプリント対象から無条件で除外する（安易な先送り）"
        ],
        "answer": [
            "最も大きな数字（20）を出したメンバーと、最も小さな数字（3）を出したメンバーにそれぞれの根拠や懸念点を説明してもらい、認識を合わせてから再投票を行う"
        ],
        "explanation": "【解説】\nプランニングポーカーの目的は「数字を当てること」ではなく「認識のズレ（リスク）を解消すること」です。乖離がある場合は対話が必要です。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol109.json)
q2_gen = [
    {
        "id": "Q2-GEN-V109-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】状態遷移テストの網羅性。\nECサイトの注文処理（注文→入金→発送→完了）において、ステータス管理の不具合が頻発している。\n「本来ありえない遷移（例：未入金なのに発送される）」を防ぐためのテスト設計として、最も効果的なアプローチはどれか。",
        "options": [
            "全ての「正しい遷移（Valid Transitions）」を網羅するテストケース（0-switch coverage）を作成し、正常に業務が流れることだけを確認する（不正遷移のガードを確認できない）",
            "状態遷移表（State Transition Table）を作成し、無効なイベントと状態の組み合わせ（N/Aセル）に対してテストを実行し、システムが遷移を拒否（エラーまたは無視）することを確認する",
            "ランダムに画面操作を行う探索的テストを実施し、たまたま不正な遷移が発生しないかを運任せで確認する（網羅性が保証されない）",
            "可能なすべての遷移パスを無限に繰り返す「n-switch coverage」を目指し、数千パターンのシナリオを作成して全量テストする（現実的な時間で終わらない）"
        ],
        "answer": [
            "状態遷移表（State Transition Table）を作成し、無効なイベントと状態の組み合わせ（N/Aセル）に対してテストを実行し、システムが遷移を拒否（エラーまたは無視）することを確認する"
        ],
        "explanation": "【解説】\nステータス管理のバグ（不正遷移）を見つけるには、Happy Path（正常遷移）だけでなく、禁止された遷移（Negative Testing）を網羅的に確認する必要があります。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol109.json)
q1_aws = [
    {
        "id": "Q1-AWS-V109-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】CloudFrontとS3によるセキュアな配信。\nS3バケット内の静的コンテンツをCloudFront経由でのみアクセス可能にし、S3への直接アクセスは禁止したい。\nこの要件を満たしているか確認するためのテスト方法はどれか。",
        "options": [
            "S3バケットを「パブリックアクセス許可」に設定した上で、ファイル名を推測困難なランダムな文字列（GUID等）にして、誰も直接アクセスできないようにする（セキュリティ・バイ・オブスキュリティ）",
            "OAC (Origin Access Control) または OAI を設定し、S3バケットポリシーで「CloudFrontからのアクセスのみ許可（Principal判定）」する設定を行った上で、S3のURLに直接アクセスして「403 Forbidden」になることを確認する",
            "CloudFrontのURLにアクセスして画像が表示されることだけを確認し、S3側の設定確認は省略する（直接アクセスの穴が空いている可能性がある）",
            "S3のバケットポリシーですべてのアクセスを拒否（Deny All）し、CloudFrontからもアクセスできない状態にして、安全性を最大限に高める（サービスが機能しない）"
        ],
        "answer": [
            "OAC (Origin Access Control) または OAI を設定し、S3バケットポリシーで「CloudFrontからのアクセスのみ許可（Principal判定）」する設定を行った上で、S3のURLに直接アクセスして「403 Forbidden」になることを確認する"
        ],
        "explanation": "【解説】\nCloudFront経由のみに制限するには、OAC/OAIとバケットポリシーの組み合わせが必須です。テストでは「S3直接アクセスが拒否されること」を確認します。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol109.json)
q2_fin = [
    {
        "id": "Q2-FIN-V109-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】金利計算の精度テスト。\n年利計算において、小数点以下の端数処理（切り捨て・四捨五入）で1円の誤差も許されない。\nプログラミング言語の浮動小数点数型（float/double）に起因する誤差（丸め誤差）を検出するためのテスト方針はどれか。",
        "options": [
            "計算結果に1円程度の誤差が出るのはコンピュータの仕様上仕方がないため、許容範囲（±1円）を設けてテストを合格とする（金融システムでは許されない）",
            "テストデータの期待値を計算する際、Excelや電卓ではなく、高精度な「Decimal型（固定小数点）」を使用したスクリプトで厳密に計算し、システムの実装もDecimal型が使われているかコードレビューとセットで検証する",
            "ランダムな金額で大量に計算させ、結果が「なんとなく正しそう」であればOKとする（稀に発生する境界値の丸め誤差を見逃す）",
            "金額をすべて整数（Integer）に変換してから計算し、最後に割り算を行うロジックに変更するよう開発者に指示するが、割り算のタイミングでの誤差は考慮しない（計算順序による誤差リスク）"
        ],
        "answer": [
            "テストデータの期待値を計算する際、Excelや電卓ではなく、高精度な「Decimal型（固定小数点）」を使用したスクリプトで厳密に計算し、システムの実装もDecimal型が使われているかコードレビューとセットで検証する"
        ],
        "explanation": "【解説】\n金融計算でFloat/Doubleは厳禁です。テスト期待値もDecimalで計算し、1円単位（あるいは銭単位）まで完全に一致することを確認する必要があります。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol109.json": q3_gen,
    "ch1_general_vol109.json": q1_gen,
    "ch2_general_vol109.json": q2_gen,
    "ch1_aws_vol109.json": q1_aws,
    "ch2_finance_vol109.json": q2_fin
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
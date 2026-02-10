import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.122 新規問題データ定義（括弧なし・フラット文体）
# ==========================================

# 1. 第3章 一般 (ch3_general_vol122.json)
q3_gen = [
    {
        "id": "Q3-GEN-V122-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】アジャイル開発における「準備完了の定義（Definition of Ready: DoR）」の活用。\nスプリント計画会議において、ユーザーストーリーの要件が曖昧なまま開発に着手してしまい、スプリント後半になって仕様確認のための手戻りが頻発している。\nこのプロセス課題を解決するための施策として、最も適切なものはどれか。",
        "options": [
            "スプリント期間を2週間から4週間に延長し、開発チームが仕様を確認するためのバッファ時間を十分に確保する",
            "「完了の定義（DoD）」の基準を緩和し、仕様が一部未確定であってもリリースできるようにすることで、スプリント内の完了率を上げる",
            "「準備完了の定義（DoR）」を導入し、受け入れ基準や入力データが明確になっていないストーリーは、スプリントバックログへの投入を拒否するルールにする",
            "プロダクトオーナー（PO）の権限を縮小し、開発チームが独自に仕様を決定できるようにすることで、確認待ちの時間を削減する"
        ],
        "answer": [
            "「準備完了の定義（DoR）」を導入し、受け入れ基準や入力データが明確になっていないストーリーは、スプリントバックログへの投入を拒否するルールにする"
        ],
        "explanation": "【解説】\n開発着手後の手戻りを防ぐには「入り口」の品質管理が重要です。DoR（Definition of Ready）を設け、着手条件（要件の明確化など）を満たしたものだけをスプリントに入れるようにします。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol122.json)
q1_gen = [
    {
        "id": "Q1-GEN-V122-01",
        "chapter": "第1章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】テストベースの品質と欠陥の検出。\n要件定義書のレビューにおいて、「システムは高負荷時でも十分なレスポンス性能を維持すること」という記述が見つかった。\nテストアナリストとして、この記述に対して指摘すべき問題点はどれか。",
        "options": [
            "「高負荷」や「十分な」という表現が定性的で曖昧であるため、具体的な同時アクセス数や目標応答時間（秒数）を数値で定義する必要がある",
            "非機能要件はテストの対象外であるため、要件定義書から削除し、運用保守フェーズで検討するように記載を変更する必要がある",
            "性能要件はハードウェアのスペックに依存するため、ソフトウェアの要件定義書に記述するのではなく、インフラ設計書にのみ記述すべきである",
            "レスポンス性能よりも機能の正しさが優先されるべきであるため、この要件の優先順位を「低」に設定し直す必要がある"
        ],
        "answer": [
            "「高負荷」や「十分な」という表現が定性的で曖昧であるため、具体的な同時アクセス数や目標応答時間（秒数）を数値で定義する必要がある"
        ],
        "explanation": "【解説】\n「テスト不能（Untestable）」な要件の典型例です。テストを行うためには、合格基準が客観的に判定できる「定量的な数値」で定義されている必要があります。",
        "tags": ["第1章", "一般", "シナリオ", "K4"]
    }
]

# 3. 第2章 一般 (ch2_general_vol122.json)
q2_gen = [
    {
        "id": "Q2-GEN-V122-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】デシジョンテーブルテストの圧縮（Collapse）。\nある条件分岐のロジックにおいて、条件Aが「真（True）」であれば、条件Bや条件Cの値に関わらず、必ずアクションXが実行される仕様になっている。\nこの部分のデシジョンテーブルを簡略化（圧縮）する際の正しい記述方法はどれか。",
        "options": [
            "条件Aが真となる列における条件Bと条件Cのセルを「N/A（不問）」または「－（ハイフン）」とし、複数の列を1つの列に統合して表現する",
            "条件Aが真となるケースはテストの必要がないため、デシジョンテーブルから該当する列を完全に削除する",
            "条件Bと条件Cが存在しないものとして扱い、条件Aだけの新しいデシジョンテーブルを別途作成して管理する",
            "すべての組み合わせを網羅するために、条件Bと条件Cの真偽の組み合わせ（True/False）を全て展開し、省略せずに記述する"
        ],
        "answer": [
            "条件Aが真となる列における条件Bと条件Cのセルを「N/A（不問）」または「－（ハイフン）」とし、複数の列を1つの列に統合して表現する"
        ],
        "explanation": "【解説】\n結果に影響を与えない条件の組み合わせは「不問（Don't Care）」として扱い、列を統合（圧縮）することでテーブルを見やすく整理できます。これを怠るとテーブルが巨大化しすぎます。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol122.json)
q1_aws = [
    {
        "id": "Q1-AWS-V122-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】RDSの可用性テスト（Multi-AZ）。\nRDS for MySQLをマルチAZ構成で運用している。\nプライマリインスタンスに障害が発生した場合の自動フェイルオーバーが、アプリケーション側で正しくハンドリングされるか（DNS切り替えの追従など）を検証したい。\n最も推奨されるテスト方法はどれか。",
        "options": [
            "RDSコンソールの「再起動（Reboot）」アクションを選択し、「フェイルオーバーして再起動しますか？」のオプションを有効にして実行する",
            "プライマリインスタンスのセキュリティグループ設定を変更し、意図的に全ての通信を遮断することでタイムアウトを発生させる",
            "アプリケーションサーバー側のデータベース接続設定を書き換え、存在しないIPアドレスに向けて接続リクエストを送信する",
            "AWSサポートに連絡し、指定した日時に物理ホストの電源を落としてもらうように依頼する"
        ],
        "answer": [
            "RDSコンソールの「再起動（Reboot）」アクションを選択し、「フェイルオーバーして再起動しますか？」のオプションを有効にして実行する"
        ],
        "explanation": "【解説】\nRDSのマルチAZフェイルオーバーをテストする公式機能として「フェイルオーバー付き再起動」が用意されています。これにより、DNSの切り替えやアプリの再接続ロジックを安全に検証できます。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol122.json)
q2_fin = [
    {
        "id": "Q2-FIN-V122-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】クレジットカード決済のオーソリ（信用照会）と売上確定。\nECサイトの決済テストにおいて、商品は発送されていないが、クレジットカードの利用枠だけが確保されている状態（仮売上）を確認したい。\n決済代行会社（PSP）の管理画面やAPIレスポンスにおいて、確認すべきステータスや挙動はどれか。",
        "options": [
            "トランザクションのステータスが「Auth（オーソリ成功）」または「仮売上」となっており、まだ「Capture（実売上/売上確定）」処理が行われていないことを確認する",
            "トランザクションのステータスが「Sales（売上）」になっており、顧客のカード明細に請求確定データとして即時に反映されていることを確認する",
            "オーソリ処理はカードの有効性確認のみであるため、利用枠の減算（確保）は行われておらず、利用可能額が変わっていないことを確認する",
            "ステータスが「Void（取消）」になっており、決済処理自体が無効化されていることを確認する"
        ],
        "answer": [
            "トランザクションのステータスが「Auth（オーソリ成功）」または「仮売上」となっており、まだ「Capture（実売上/売上確定）」処理が行われていないことを確認する"
        ],
        "explanation": "【解説】\nクレジットカード決済には「オーソリ（枠確保）」と「売上確定（実請求）」の2段階があります。商品発送前はオーソリ（仮売上）状態であるのが正常なフローです。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol122.json": q3_gen,
    "ch1_general_vol122.json": q1_gen,
    "ch2_general_vol122.json": q2_gen,
    "ch1_aws_vol122.json": q1_aws,
    "ch2_finance_vol122.json": q2_fin
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
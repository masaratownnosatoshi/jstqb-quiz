import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.110 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol110.json)
q3_gen = [
    {
        "id": "Q3-GEN-V110-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストプロセス改善における「IDEALモデル」。\n組織のテストプロセス改善を開始するにあたり、「診断（Diagnosing）」フェーズが完了した。\nIDEALモデルに従う場合、次に行うべき「確立（Establishing）」フェーズのアクションとして最も適切なものはどれか。",
        "options": [
            "診断結果に基づき、具体的な改善計画を作成し、パイロットプロジェクトの選定や改善チームの結成を行って、実行の準備を整える",
            "直ちに新しいプロセスを全社一斉に展開し、すべてのプロジェクトに対して新しいルールの遵守を強制する（準備不足での展開は混乱を招く）",
            "診断結果が悪かったプロジェクトの責任者を処分し、新しいマネージャを外部から登用して体制を刷新する（改善ではなく処罰になってしまっている）",
            "プロセスの改善は現場の自主性に任せることとし、マネジメント層は一切関与せず、報告だけを待つことにする（リーダーシップの放棄）"
        ],
        "answer": [
            "診断結果に基づき、具体的な改善計画を作成し、パイロットプロジェクトの選定や改善チームの結成を行って、実行の準備を整える"
        ],
        "explanation": "【解説】\nIDEALモデルの順序は、開始(I)→診断(D)→確立(E)→行動(A)→学習(L)です。「確立」では、いきなり展開するのではなく、計画策定やパイロット準備を行います。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol110.json)
q1_gen = [
    {
        "id": "Q1-GEN-V110-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】アジャイル開発における「完了の定義（Definition of Done: DoD）」。\nスプリントレビューにおいて、ステークホルダーから「機能は動いているが、ヘルプ画面の記述が古い」という指摘を受けた。\nこのような事態を防ぐためのDoDの活用方法として正しいものはどれか。",
        "options": [
            "ヘルプ画面の更新は開発者の仕事ではないため、テクニカルライターが完了するまでDoDには含めず、機能実装だけで完了とする（完了基準の甘さ）",
            "「ユーザー向けドキュメントが更新され、レビュー済みであること」をDoDに明記し、これを満たさない限りストーリーを完了（Done）とみなさない運用を徹底する",
            "DoDはあくまで努力目標であるため、スプリント終了時に間に合わなければ、次回のスプリントで対応することにして完了扱いにしてもよい（プロセスの形骸化）",
            "ヘルプ画面の更新は重要度が低いため、リリース直前の「ハードニングスプリント」でまとめて対応することにし、通常スプリントでは無視する（技術的負債の蓄積）"
        ],
        "answer": [
            "「ユーザー向けドキュメントが更新され、レビュー済みであること」をDoDに明記し、これを満たさない限りストーリーを完了（Done）とみなさない運用を徹底する"
        ],
        "explanation": "【解説】\nDoDは品質のゲートキーパーです。必要な作業（ドキュメント更新など）が漏れているなら、それをDoDに追加し、厳格に運用するのがアジャイルの鉄則です。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol110.json)
q2_gen = [
    {
        "id": "Q2-GEN-V110-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】根本原因分析（RCA）。\n「本番環境でのみ発生するパフォーマンス低下」という問題に対し、フィッシュボーンダイアグラム（特性要因図）を用いて分析を行った。\n「環境要因」の枝において深掘りすべき項目として、最も可能性が高く検証価値のある仮説はどれか。",
        "options": [
            "テスト環境と本番環境で、データベースのインデックス設定や統計情報、データ量（カーディナリティ）に差異があり、実行計画が変わっているのではないか",
            "本番環境のサーバーの色が気に入らないため、サーバーが機嫌を損ねて処理速度を落としているのではないか（非科学的）",
            "開発担当者が本番環境のコードを勝手に書き換えて、意図的にウェイト処理を入れたのではないか（性悪説すぎる仮説）",
            "宇宙線の影響によりメモリのビット反転（ソフトエラー）が発生し、偶然パフォーマンスが低下したのではないか（再現性が低く、最初に疑うべきではない）"
        ],
        "answer": [
            "テスト環境と本番環境で、データベースのインデックス設定や統計情報、データ量（カーディナリティ）に差異があり、実行計画が変わっているのではないか"
        ],
        "explanation": "【解説】\n環境差異による性能問題の筆頭は「DB統計情報」や「インデックス」の違いです。RCAでは、オカルトや極端なレアケースではなく、論理的にあり得る構成差異から疑います。",
        "tags": ["第2章", "一般", "シナリオ", "K4"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol110.json)
q1_aws = [
    {
        "id": "Q1-AWS-V101-01", # ID重複防止のため連番注意（vol110として作成）
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】Auto Scalingの動作検証。\nEC2インスタンスのCPU使用率が70%を超えたらスケールアウト（台数増加）する設定を行いたい。\nこのスケーリングポリシーが正しく機能することを、短時間かつ低コストで検証するための方法はどれか。",
        "options": [
            "実際に数千人のユーザーを集めて一斉にアクセスさせ、CPU負荷を自然に上昇させてスケーリングを待つ（コストと手間がかかりすぎる）",
            "stressコマンド等の負荷ツールをインスタンス内で実行してCPU使用率を人為的に引き上げ、CloudWatchアラームの発火とAuto Scalingの起動を確認する",
            "Auto Scalingの設定画面を目視で確認し、設定値が正しいのであれば必ず動くと信じて、実機でのテストは省略する（設定ミスを見抜けない）",
            "本番稼働中のサーバーを1台手動で停止させ、減った分が自動的に補充されること（Auto Healing）を確認する（スケーリングポリシーの検証になっていない）"
        ],
        "answer": [
            "stressコマンド等の負荷ツールをインスタンス内で実行してCPU使用率を人為的に引き上げ、CloudWatchアラームの発火とAuto Scalingの起動を確認する"
        ],
        "explanation": "【解説】\nスケーリングのトリガー（CPU負荷）を検証するには、`stress` などのツールで擬似的に負荷をかけるのが定石です。人を集めるのは非現実的です。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol110.json)
q2_fin = [
    {
        "id": "Q2-FIN-V110-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】API連携におけるセキュリティテスト（OAuth 2.0）。\nFinTechアプリが銀行の口座情報を参照するために、OAuth 2.0を用いたAPI連携を行っている。\n認可コード（Authorization Code）の横取り攻撃を防ぐために実装されている「PKCE（Proof Key for Code Exchange）」が正しく機能しているか検証したい。\n適切なテスト方法はどれか。",
        "options": [
            "認可リクエストから `code_challenge` パラメータを削除して送信し、認可サーバーがエラー（invalid_request）を返却することを確認する（必須チェックの検証）",
            "認可リクエストを送信する際に、HTTPSではなくHTTPで送信し、通信が暗号化されていないことを確認する（PKCEの検証ではない）",
            "アクセストークンの有効期限が切れた後にAPIを呼び出し、リフレッシュトークンによる更新ができるかを確認する（トークンライフサイクルの検証であり、PKCEではない）",
            "正しい `code_verifier` を持たない攻撃者が、横取りした認可コードを使ってトークン交換を試みても、成功してしまうことを確認する（これは脆弱性の確認であり、防げていることの確認ではない）"
        ],
        "answer": [
            "認可リクエストから `code_challenge` パラメータを削除して送信し、認可サーバーがエラー（invalid_request）を返却することを確認する（必須チェックの検証）"
        ],
        "explanation": "【解説】\nPKCEのテストでは、「PKCEパラメータがない場合に拒否されるか」や「不正なverifierで拒否されるか」といったネガティブテストが重要です。",
        "tags": ["第2章", "金融", "シナリオ", "K3"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol110.json": q3_gen,
    "ch1_general_vol110.json": q1_gen,
    "ch2_general_vol110.json": q2_gen,
    "ch1_aws_vol110.json": q1_aws,
    "ch2_finance_vol110.json": q2_fin
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
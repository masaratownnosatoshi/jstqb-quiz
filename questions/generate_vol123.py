import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# ==========================================
# Vol.123 新規問題データ定義
# ==========================================

# 1. 第3章 一般 (ch3_general_vol123.json)
q3_gen = [
    {
        "id": "Q3-GEN-V123-01",
        "chapter": "第3章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】テストツールの導入とPoC（概念実証）。\n組織全体に新しいテスト自動化ツールを導入しようと計画している。カタログスペック上は要件を満たしているが、実際の開発プロセスに適合するかは不明である。\n本格導入前のリスク軽減策として、最も適切なアプローチはどれか。",
        "options": [
            "ツールのライセンスを全プロジェクト分一括購入し、トップダウンで「来月から全員このツールを使うこと」という業務命令を出して強制的に定着させる",
            "特定のパイロットプロジェクトを選定してPoC（概念実証）を実施し、実際の環境で期待通りの効果が出るか、既存プロセスと競合しないかを小規模に検証する",
            "ツールのベンダー営業担当者の説明を全面的に信頼し、自社での検証は行わずに、ベンダーが提示した成功事例の数値をそのまま経営層への報告に使う",
            "無料のオープンソースツールであれば導入コストはゼロであるため、検証なしに全社員のPCにインストールさせ、使いながら問題点を見つけてもらう"
        ],
        "answer": [
            "特定のパイロットプロジェクトを選定してPoC（概念実証）を実施し、実際の環境で期待通りの効果が出るか、既存プロセスと競合しないかを小規模に検証する"
        ],
        "explanation": "【解説】\nツール導入の失敗を防ぐにはPoC（Proof of Concept）が不可欠です。スモールスタートで実効性を確認してから、段階的に展開するのが定石です。",
        "tags": ["第3章", "一般", "シナリオ", "K3"]
    }
]

# 2. 第1章 一般 (ch1_general_vol123.json)
q1_gen = [
    {
        "id": "Q1-GEN-V123-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】アクセシビリティテスト（WCAG/JIS X 8341-3）。\n公共性の高いWebサイトの構築において、視覚障害者や高齢者を含む全てのユーザーが利用できることを保証したい。\nアクセシビリティ対応の検証として実施すべき具体的なテスト内容はどれか。",
        "options": [
            "高解像度の最新モニターを使用し、デザインや配色が美しく見えるか、アニメーションが滑らかに動作するかを重点的に確認する",
            "マウス操作だけで全ての機能にアクセスできるかを確認し、キーボード操作については使用頻度が低いためテスト対象外とする",
            "スクリーンリーダー（音声読み上げソフト）を使用し、画像に代替テキスト（alt属性）が設定されているか、見出しレベル（h1-h6）が論理的な順序で構成されているかを確認する",
            "健常者のテスターだけを集め、彼らが「使いやすい」と感じるかどうかをアンケート調査し、その平均点をアクセシビリティの指標とする"
        ],
        "answer": [
            "スクリーンリーダー（音声読み上げソフト）を使用し、画像に代替テキスト（alt属性）が設定されているか、見出しレベル（h1-h6）が論理的な順序で構成されているかを確認する"
        ],
        "explanation": "【解説】\nアクセシビリティテストでは、スクリーンリーダーでの読み上げ確認や、キーボードのみでの操作性（フォーカス移動）の検証が必須となります。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

# 3. 第2章 一般 (ch2_general_vol123.json)
q2_gen = [
    {
        "id": "Q2-GEN-V123-01",
        "chapter": "第2章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】ペアワイズ法（All-pairs）の適用範囲。\nOS（Windows, Mac, Linux）、ブラウザ（Chrome, Firefox, Safari）、Javaバージョン（8, 11, 17）の組み合わせテストを行いたい。\nペアワイズ法を適用してテストケースを削減することが適している状況と、そのリスクに関する正しい記述はどれか。",
        "options": [
            "特定の3つの条件が重なった時にのみ発生する不具合（3因子間相互作用）のリスクは低いと仮定し、2つの因子の組み合わせさえ網羅できれば十分な品質を確保できると判断する場合",
            "銀行の勘定系システムのようなミッションクリティカルな領域であり、発生確率は低くても組み合わせ起因のバグを一切見逃すことが許されない場合",
            "各因子が互いに独立しておらず、強い依存関係（例：SafariはMacでしか動かない等）が多数存在し、無効な組み合わせが大半を占める場合",
            "テスト自動化環境が整っており、すべての組み合わせ（全網羅）を実行しても数分で完了するため、テストケース削減の必要性がない場合"
        ],
        "answer": [
            "特定の3つの条件が重なった時にのみ発生する不具合（3因子間相互作用）のリスクは低いと仮定し、2つの因子の組み合わせさえ網羅できれば十分な品質を確保できると判断する場合"
        ],
        "explanation": "【解説】\nペアワイズ法は「2因子間の相互作用」を効率的に網羅する手法です。3因子以上のバグを見逃すリスク（残存リスク）を受容できる場合に適しています。",
        "tags": ["第2章", "一般", "シナリオ", "K3"]
    }
]

# 4. 第1章 AWS (ch1_aws_vol123.json)
q1_aws = [
    {
        "id": "Q1-AWS-V123-01",
        "chapter": "第1章",
        "level": "K3",
        "category": "AWS",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】CloudWatch Alarmの通知テスト。\nCPU使用率が80%を超えたらメール通知を行うCloudWatch Alarmを設定した。\n実際にCPU負荷を上げることなく、アラーム設定と通知アクション（SNS）が正しく連携されているかをテストするための最も効率的な方法はどれか。",
        "options": [
            "EC2インスタンスにログインし、無限ループのプログラムを実行してCPU使用率を100%にし、実際にアラーム状態になるまで待機する",
            "AWS CLIの `set-alarm-state` コマンドを使用し、アラームの状態を強制的に「ALARM」に変更して、通知がトリガーされることを確認する",
            "CloudWatchのコンソール画面を開き、アラームの設定値が「80%」になっていることを目視で確認するだけで完了とする",
            "Amazon SNSのトピックから自分宛てにテストメールを送信し、メールが届くことだけを確認する（CloudWatchとの連携確認は行わない）"
        ],
        "answer": [
            "AWS CLIの `set-alarm-state` コマンドを使用し、アラームの状態を強制的に「ALARM」に変更して、通知がトリガーされることを確認する"
        ],
        "explanation": "【解説】\n実際に負荷をかけなくても、`set-alarm-state` コマンドを使えばアラーム状態をシミュレートでき、アクション（通知やAuto Scaling）のテストが可能です。",
        "tags": ["第1章", "AWS", "シナリオ", "K3"]
    }
]

# 5. 第2章 金融 (ch2_finance_vol123.json)
q2_fin = [
    {
        "id": "Q2-FIN-V123-01",
        "chapter": "第2章",
        "level": "K4",
        "category": "金融",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【分析】株式取引の約定日と受渡日（T+2）。\n証券取引システムにおいて、顧客が株式を購入した際の「受渡日（Settlement Date）」が正しく計算されるかを検証したい。\n市場の決済サイクルが「T+2（取引日の2営業日後）」である場合、考慮すべき日付計算のロジックはどれか。",
        "options": [
            "取引日（Trade Date）に2日を加算する際、土日祝日（市場休業日）をスキップせず、単純にカレンダー上の2日後を受渡日として設定する",
            "取引日（Trade Date）から起算して、営業日ベースで2日目を算出し、間に土日祝日が含まれる場合はその分だけ受渡日を後ろにずらす",
            "受渡日は常に取引日の翌日（T+1）とし、市場の決済サイクルに関わらずシステム側で一律に固定する",
            "顧客が注文画面で受渡日を自由に指定できるようにし、システム側では日付の妥当性チェックを行わない"
        ],
        "answer": [
            "取引日（Trade Date）から起算して、営業日ベースで2日目を算出し、間に土日祝日が含まれる場合はその分だけ受渡日を後ろにずらす"
        ],
        "explanation": "【解説】\n金融取引の「T+N」は営業日ベースでの計算（Business Days）です。金曜日に取引（T）した場合、土日を飛ばして火曜日が受渡日（T+2）になるロジックなどを検証します。",
        "tags": ["第2章", "金融", "シナリオ", "K4"]
    }
]

# ==========================================
# ファイル生成 & Index更新処理
# ==========================================
files_content = {
    "ch3_general_vol123.json": q3_gen,
    "ch1_general_vol123.json": q1_gen,
    "ch2_general_vol123.json": q2_gen,
    "ch1_aws_vol123.json": q1_aws,
    "ch2_finance_vol123.json": q2_fin
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
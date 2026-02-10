import json
import os

# 修正設定（ファイル名 -> 問題ID -> 新しい選択肢テキスト）
FIX_MAP = {
    "ch1_aws.json": {
        "Q1-AWS-05": "ユーザーデータをランダムに削除してバックアップの復元力をテストする（※本番データ消失のリスクがあるため不適切）",
        "Q1-AWS-06": "ベンダーロックインの最大化"
    },
    "ch1_aws_vol11.json": {
        "Q1-AWS-V11-01": "クラウド特有の制限事項（スケーリング等）を無視して、オンプレミスと同じ設定を強制適用する"
    },
    "ch1_aws_vol2.json": {
        "Q1-AWS-V2-02": "運用手順をドキュメント化せず、個人の記憶と職人芸に依存する"
    },
    "ch1_finance_vol11.json": {
        "Q1-FIN-V11-01": "非機能要件の未達を隠蔽し、ステークホルダーに報告せずにリリースする"
    },
    "ch1_finance_vol12.json": {
        "Q1-FIN-V12-01": "顧客影響を考慮せず、最も混雑する平日の昼間にATMを全停止して更新作業を行う"
    }
}

OUTPUT_DIR = "."

def fix_phase2_a():
    print("--- Phase 2-A: AWS・金融系ファイルのゴミデータ修正を開始 ---")
    
    fixed_count = 0
    
    for filename, id_map in FIX_MAP.items():
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(file_path):
            print(f"スキップ（ファイルなし）: {filename}")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_modified = False
            
            if isinstance(data, list):
                for q in data:
                    q_id = q.get("id")
                    
                    # ターゲットのIDかチェック
                    if q_id in id_map:
                        target_text = "統計的なばらつき"
                        new_text = id_map[q_id]
                        
                        # 選択肢リストの中身を走査して置換
                        if "options" in q:
                            new_options = []
                            replaced = False
                            for opt in q["options"]:
                                if target_text in opt:
                                    new_options.append(new_text)
                                    replaced = True
                                else:
                                    new_options.append(opt)
                            
                            if replaced:
                                q["options"] = new_options
                                file_modified = True
                                print(f"修正: {filename} (ID: {q_id})")
                                print(f"  -> 「{target_text}」を文脈に沿った選択肢に変更しました。")
            
            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                fixed_count += 1
            else:
                print(f"変更なし: {filename} (対象のゴミデータが見つかりませんでした)")

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"Phase 2-A 完了: {fixed_count} ファイルを修正しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_phase2_a()
    input()
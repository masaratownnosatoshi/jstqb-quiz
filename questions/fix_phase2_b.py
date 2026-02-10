import json
import os

# 修正設定（ファイル名 -> 問題ID -> 新しい選択肢テキスト）
FIX_MAP = {
    "ch1_general_vol10.json": {
        "Q1-GEN-V10-01": "残存バグを「仕様」として再分類し、見かけ上の合格率を100%にする（隠蔽）"
    },
    "ch1_general_vol17.json": {
        "Q1-GEN-V17-01": "開発者の手元にある最新機種（1台）のみで動作確認を行い、市場の断片化（Fragmentation）は無視する"
    },
    "ch1_general_vol26.json": {
        "Q1-GEN-V26-02": "「運用でカバーする」として、顧客への周知なしにリリースを強行する"
    },
    "ch1_general_vol3.json": {
        "Q1-GEN-V3-01": "テスト担当者のスキル不足と決めつけ、原因調査をせずに全員を交代させる"
    },
    "ch1_general_vol50.json": {
        "Q1-GEN-V50-01": "全てのリスクを「受容」し、テストを行わない",
        "Q1-GEN-V50-02": "すべてのサブシステムに同じ工数をかけ、リスクの大小に関わらず画一的なテストを行う"
    },
    "ch1_general_vol67.json": {
        "Q1-GEN-V67-02": "ドキュメントのみをレビューし、ユーザーへのヒアリングは一切行わない"
    }
}

OUTPUT_DIR = "."

def fix_phase2_b():
    print("--- Phase 2-B: 一般カテゴリ前半のゴミデータ修正を開始 ---")
    
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
                        new_text = id_map[q_id]
                        
                        # 置換対象のゴミデータパターン
                        garbage_patterns = ["統計的なばらつき", "報告せずにこっそりと修正し"]
                        
                        if "options" in q:
                            new_options = []
                            replaced = False
                            for opt in q["options"]:
                                # ゴミデータが含まれていれば置換
                                if any(g in opt for g in garbage_patterns):
                                    new_options.append(new_text)
                                    replaced = True
                                else:
                                    new_options.append(opt)
                            
                            if replaced:
                                q["options"] = new_options
                                file_modified = True
                                print(f"修正: {filename} (ID: {q_id})")
                                print(f"  -> 不適切な選択肢を文脈に沿ったものに変更しました。")
            
            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                fixed_count += 1
            else:
                print(f"変更なし: {filename} (対象のゴミデータが見つかりませんでした)")

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"Phase 2-B 完了: {fixed_count} ファイルを修正しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_phase2_b()
    input()
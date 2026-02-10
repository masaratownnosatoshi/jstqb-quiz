import json
import os

# 修正設定（ファイル名 -> 問題ID -> 新しい選択肢テキスト）
FIX_MAP = {
    "ch2_general_vol76.json": {
        "Q2-GEN-V76-03": "静的解析ツールを導入したため、人間の目によるコードレビューは不要と判断して廃止する"
    },
    "ch2_general_vol79.json": {
        "Q2-GEN-V79-01": "他のシステムと同じソースコードをコピー＆ペーストして使い回すことで、テスト自体を省略する"
    },
    "ch3_finance.json": {
        "Q3-FIN-03": "トラブル発生時、上司や顧客に報告すると怒られるため、現場判断で勝手に修正し、事なきを得る（隠蔽・独断）"
    },
    "ch3_finance_vol3.json": {
        "Q3-FIN-V3-01": "運用担当者の睡眠時間を確保するため、夜間はシステムのアラート通知を切り、翌朝まとめて対応する"
    },
    "ch3_general_vol15.json": {
        "Q3-GEN-V15-02": "単一ベンダーの製品群（スイート）ですべて統一し、外部ツールとの連携やデータ交換を一切遮断する（ベンダーロックイン）"
    },
    # スキル不足系3兄弟
    "ch3_general_vol76.json": {
        "Q3-GEN-V76-01": "学習コストがかかるため自動化ツールの導入を諦め、外部ベンダーに丸投げするか、人海戦術で乗り切る"
    },
    "ch3_general_vol77.json": {
        "Q3-GEN-V77-01": "学習コストがかかるため自動化ツールの導入を諦め、外部ベンダーに丸投げするか、人海戦術で乗り切る"
    },
    "ch3_general_vol79.json": {
        "Q3-GEN-V79-02": "学習コストがかかるため自動化ツールの導入を諦め、外部ベンダーに丸投げするか、人海戦術で乗り切る"
    }
}

OUTPUT_DIR = "."

def fix_phase2_d():
    print("--- Phase 2-D: 最後のゴミデータ修正を開始 ---")
    
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
                    
                    if q_id in id_map:
                        new_text = id_map[q_id]
                        # 修正対象パターン（複数のゴミデータに対応）
                        garbage_patterns = [
                            "統計的なばらつき",
                            "報告せずにこっそりと修正し",
                            "リスクを受容したことにして、対策を先送りする"
                        ]
                        
                        if "options" in q:
                            new_options = []
                            replaced = False
                            for opt in q["options"]:
                                if any(g in opt for g in garbage_patterns):
                                    new_options.append(new_text)
                                    replaced = True
                                else:
                                    new_options.append(opt)
                            
                            if replaced:
                                q["options"] = new_options
                                file_modified = True
                                print(f"修正: {filename} (ID: {q_id})")
                                print(f"  -> 不適切な選択肢を修正しました。")
            
            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                fixed_count += 1
            else:
                print(f"変更なし: {filename} (対象のゴミデータが見つかりませんでした)")

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"Phase 2-D 完了: {fixed_count} ファイルを修正しました。")
    print("これでフェーズ2（ゴミデータ一掃）はすべて完了です！")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_phase2_d()
    input()
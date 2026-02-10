import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."
SEARCH_KEYWORD = "欠陥の偏在"

def check_clustering_status():
    print(f"--- キーワード「{SEARCH_KEYWORD}」の調査開始 ---")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    found_count = 0

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for i, q in enumerate(data):
                    q_text = q.get("question", "")
                    
                    if SEARCH_KEYWORD in q_text:
                        found_count += 1
                        q_id = q.get("id", "不明")
                        options = q.get("options", [])
                        
                        print(f"\n[発見 {found_count}]")
                        print(f"  ファイル名: {filename}")
                        print(f"  配列Index : {i} 番目")
                        print(f"  ID        : {q_id}")
                        
                        # 選択肢に（）が含まれているかチェック
                        has_parens = False
                        for opt in options:
                            if "（" in opt or "(" in opt:
                                # ただし、正解の「リファクタリング（設計見直し...）」は除外して判定したいが
                                # ここでは単純に検出状況を見たいのでそのまま表示
                                has_parens = True
                        
                        print(f"  状態      : {'★（）あり' if has_parens else '◎（）なし (クリーン)'}")
                        print("  選択肢プレビュー:")
                        for opt in options:
                            print(f"    - {opt[:40]}...")

        except Exception as e:
            print(f"エラー読み込み不可: {filename}")

    print("\n" + "-" * 30)
    if found_count == 0:
        print("「欠陥の偏在」を含む問題は見つかりませんでした。")
    else:
        print(f"合計 {found_count} 件見つかりました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    check_clustering_status()
    input()
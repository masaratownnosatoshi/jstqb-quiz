import json
import os
import glob

# 探したい問題文の一部（ユーザー様が提示された文章）
SEARCH_TEXT = "【背景】静的解析ツール導入後、警告（Warning）が数千件発生し、開発者が無視し始めた。"

def search_specific_problem():
    print(f"--- キーワード「{SEARCH_TEXT}」を含むファイルを検索中 ---")
    
    json_files = glob.glob(os.path.join(".", "*.json"))
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
                    
                    if SEARCH_TEXT in q_text:
                        found_count += 1
                        print(f"\n【発見 {found_count}】")
                        print(f"  ファイル名: {filename}")
                        print(f"  ID        : {q.get('id')}")
                        print(f"  問題文冒頭: {q_text[:40]}...")
                        print(f"  選択肢:")
                        for opt in q.get("options", []):
                            print(f"    - {opt}")
                        print(f"  設定された正解: {q.get('answer')}")
                        print("-" * 20)

        except Exception as e:
            print(f"読み込みエラー: {filename} ({e})")

    if found_count == 0:
        print("\n該当する問題は見つかりませんでした。")
    else:
        print(f"\n合計 {found_count} 件見つかりました。")
    
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    search_specific_problem()
    input()
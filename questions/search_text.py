import json
import os
import glob

# 検索したいキーワード
SEARCH_KEYWORD = "統計的なばらつき"
# 検索対象のディレクトリ（必要に応じて変更してください）
SEARCH_DIR = "."  # カレントディレクトリ以下を検索
# または "questions" などを指定

def search_text_in_files():
    print(f"--- キーワード「{SEARCH_KEYWORD}」の検索を開始 ---")
    
    # サブディレクトリも含めて再帰的に検索
    json_files = glob.glob(os.path.join(SEARCH_DIR, "**/*.json"), recursive=True)
    
    found_count = 0

    for file_path in json_files:
        # index.json や設定ファイルは除外
        if "index.json" in file_path or "package.json" in file_path:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    # 問題文、選択肢、解説などを文字列化して検索
                    q_str = json.dumps(q, ensure_ascii=False)
                    
                    if SEARCH_KEYWORD in q_str:
                        print(f"\n🔥 発見しました！")
                        print(f"  ファイル名: {os.path.basename(file_path)}")
                        print(f"  問題ID: {q.get('id', '不明')}")
                        print(f"  問題文冒頭: {q.get('question', '')[:30]}...")
                        found_count += 1

        except Exception as e:
            # 読み込みエラーは無視
            continue

    print("-" * 30)
    if found_count == 0:
        print("✅ 「統計的なばらつき」が含まれる問題は見つかりませんでした。")
    else:
        print(f"⚠️ 合計 {found_count} 件 見つかりました。")

if __name__ == "__main__":
    search_text_in_files()
    input("\nエンターキーを押して終了...")
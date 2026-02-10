import json
import os
import glob

# 検索対象のディレクトリ
SEARCH_DIR = "."

# 複数回答を示唆するキーワード
MULTI_KEYWORDS = [
    "2つ選べ", "3つ選べ", "4つ選べ", 
    "２つ選べ", "３つ選べ", "４つ選べ", 
    "すべて選べ", "複数選べ"
]

def check_multi_answers():
    print("--- 複数選択なのに回答が1つしかない問題の検索を開始 ---")
    
    # 再帰的にJSONファイルを検索
    json_files = glob.glob(os.path.join(SEARCH_DIR, "**/*.json"), recursive=True)
    found_count = 0
    
    for file_path in json_files:
        filename = os.path.basename(file_path)
        
        # 設定ファイルなどは除外
        if filename in ["index.json", "package.json", "manifest.json", "tsconfig.json", "vercel.json"]:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    q_text = q.get("question", "")
                    answers = q.get("answer", [])
                    
                    # 問題文に「○つ選べ」が含まれているか確認
                    keyword_found = None
                    for k in MULTI_KEYWORDS:
                        if k in q_text:
                            keyword_found = k
                            break
                    
                    # 「○つ選べ」があるのに、正解リストの長さが1以下の場合
                    if keyword_found and len(answers) <= 1:
                        print(f"\n🔥 発見しました！")
                        print(f"  ファイル: {filename}")
                        print(f"  ID: {q.get('id', '不明')}")
                        print(f"  キーワード: 「{keyword_found}」")
                        print(f"  現在の回答数: {len(answers)}個 {answers}")
                        print(f"  問題文冒頭: {q_text[:50]}...")
                        found_count += 1

        except Exception as e:
            # 読み込みエラーは無視
            continue
            
    print("-" * 30)
    if found_count == 0:
        print("✅ 該当する問題は見つかりませんでした。すべて正常です。")
    else:
        print(f"⚠️ 合計 {found_count} 件 の不整合が見つかりました。")

if __name__ == "__main__":
    check_multi_answers()
    input("\nエンターキーを押して終了...")
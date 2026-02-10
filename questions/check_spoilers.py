import json
import os
import glob
import re

# 検索対象ディレクトリ
SEARCH_DIR = "."

# 検出条件（正規表現）
# 文末または文中に「（...）」があり、中に「ない」「する」「困難」「失敗」「不可」などの言葉が含まれるものを怪しいとみなす
SPOILER_PATTERN = re.compile(r'[（\(].*?(ない|する|できる|困難|失敗|不可|高い|低い|防ぐ|反する|招く|落ちる|増える|減る).*?[）\)]')

def check_spoilers():
    print("--- 選択肢に残った「カッコ書きのネタバレ」を検索します ---")
    
    json_files = glob.glob(os.path.join(SEARCH_DIR, "**/*.json"), recursive=True)
    found_count = 0
    
    for file_path in json_files:
        filename = os.path.basename(file_path)
        
        # 設定ファイル系は除外
        if filename in ["index.json", "package.json", "manifest.json", "tsconfig.json", "vercel.json"]:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    options = q.get("options", [])
                    suspicious_options = []
                    
                    for opt in options:
                        # パターンに一致するかチェック
                        if SPOILER_PATTERN.search(opt):
                            suspicious_options.append(opt)
                    
                    if suspicious_options:
                        print(f"\n🔥 発見しました！")
                        print(f"  ファイル: {filename}")
                        print(f"  ID: {q.get('id', '不明')}")
                        print(f"  問題文冒頭: {q.get('question', '')[:30]}...")
                        print("  ⚠️ 怪しい選択肢:")
                        for s_opt in suspicious_options:
                            print(f"    - {s_opt}")
                        found_count += 1

        except Exception as e:
            continue

    print("-" * 30)
    if found_count == 0:
        print("✅ ネタバレのような記述は見つかりませんでした。")
    else:
        print(f"⚠️ 合計 {found_count} 件 の候補が見つかりました。")

if __name__ == "__main__":
    check_spoilers()
    input("\nエンターキーを押して終了...")
import json
import os
import glob

# 設定
OUTPUT_DIR = "."
INDEX_FILE = "index.json"
PATH_PREFIX = "questions/"

def update_index_correctly():
    print("--- index.json を正しい形式（chunks）で更新します ---")
    
    chunks = []
    # フォルダ内の全JSONを取得
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
    json_files.sort()

    for file_path in json_files:
        filename = os.path.basename(file_path)
        
        # index.json 自身や設定ファイルは除外
        if filename in [INDEX_FILE, "package.json", "manifest.json", "tsconfig.json", "vercel.json"]:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # データがリスト（問題集）であることを確認
            if isinstance(data, list) and len(data) > 0:
                first_q = data[0]
                chapter = first_q.get("chapter", "不明")
                category = first_q.get("category", "その他")
                klevel = first_q.get("level", "K3") 

                chunk_info = {
                    "path": PATH_PREFIX + filename,
                    "chapter": chapter,
                    "category": category,
                    "klevel": klevel,
                    "qCount": len(data)
                }
                chunks.append(chunk_info)

        except Exception as e:
            print(f"  ⚠️ 読込エラー（スキップ）: {filename} ({e})")

    # 最終的な構造を作成
    output_data = {
        "chunks": chunks
    }

    try:
        with open(os.path.join(OUTPUT_DIR, INDEX_FILE), 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print("-" * 30)
        print(f"✅ 更新完了！")
        print(f"■ 登録ファイル数: {len(chunks)}")
        
        # 新規ファイルの確認
        if any("ch3_ai_extra_high_3.json" in c["path"] for c in chunks):
            print("✨ 新規ファイル (ch3_ai_extra_high_3.json) も正常に追加されました！")

    except Exception as e:
        print(f"❌ 書き込みエラー: {e}")

if __name__ == "__main__":
    update_index_correctly()
    input("エンターキーを押して終了...")
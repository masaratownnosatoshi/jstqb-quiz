import json
import os
import glob

# 設定
OUTPUT_DIR = "."
INDEX_FILE = "index.json"

# 削除対象のファイル名パターン
DELETE_PATTERNS = [
    "ch3_ai_extra_high.json",
    "ch3_ai_extra_high_2.json",
    "ch3_ai_extra_high_3.json",
    "ch3_ai_extra_high_4.json",
    "ch3_ai_extra_high_5.json"
]

def remove_ai_questions():
    print("--- 範囲外のAI問題ファイルの削除とIndex更新を開始します ---")
    
    # 1. ファイルの削除
    deleted_count = 0
    for pattern in DELETE_PATTERNS:
        file_path = os.path.join(OUTPUT_DIR, pattern)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ 削除しました: {pattern}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ 削除エラー: {pattern} ({e})")
        else:
            print(f"⚠️ 見つかりません（すでに削除済み?）: {pattern}")

    print(f"-> 合計 {deleted_count} つのファイルを削除しました。\n")

    # 2. index.json の更新（削除したファイルのエントリを除去）
    try:
        index_path = os.path.join(OUTPUT_DIR, INDEX_FILE)
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # chunksの中から、削除対象のファイルを含むものを除外
            if "chunks" in data:
                original_count = len(data["chunks"])
                new_chunks = [
                    chunk for chunk in data["chunks"] 
                    if os.path.basename(chunk["path"]) not in DELETE_PATTERNS
                ]
                
                # 変更があれば保存
                if len(new_chunks) < original_count:
                    data["chunks"] = new_chunks
                    with open(index_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    print(f"✅ index.json を更新しました（{original_count} -> {len(new_chunks)} エントリ）")
                else:
                    print("ℹ️ index.json に削除対象は含まれていませんでした。")
            else:
                print("⚠️ index.json の形式が想定と異なります（chunksが見つかりません）。")
        else:
            print("❌ index.json が見つかりません。")

    except Exception as e:
        print(f"❌ index.json 更新エラー: {e}")

    print("-" * 30)
    print("完了しました。")

if __name__ == "__main__":
    remove_ai_questions()
    input("エンターキーを押して終了...")
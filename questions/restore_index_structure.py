import json
import os
import glob

# 設定
OUTPUT_DIR = "."
INDEX_FILE = "index.json"
# パスのプレフィックス（2/6のファイルに合わせて "questions/" をつける）
PATH_PREFIX = "questions/"

def restore_index_structure():
    print("--- 以前の形式（chunks形式）で index.json を復元します ---")
    
    chunks = []
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
    
    # ファイル名でソート（順番を安定させるため）
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
                # 1問目からメタデータを取得（章、カテゴリ、レベル）
                first_q = data[0]
                chapter = first_q.get("chapter", "不明")
                category = first_q.get("category", "その他")
                level = first_q.get("level", "K?").replace("K", "") # "K3" -> "3" の可能性もあるが、元データに合わせて調整
                
                # 元データの "klevel" は "K3" のような形式なのでそのまま取得
                klevel = first_q.get("level", "K3") 

                # チャンク情報を作成
                chunk_info = {
                    "path": PATH_PREFIX + filename, # 例: questions/ch1_aws.json
                    "chapter": chapter,
                    "category": category,
                    "klevel": klevel,
                    "qCount": len(data)
                }
                
                chunks.append(chunk_info)
                # print(f"  登録: {filename} ({len(data)}問)")

        except Exception as e:
            print(f"  ⚠️ 読込エラー: {filename} ({e})")

    # 最終的な構造を作成
    output_data = {
        "chunks": chunks
    }

    # index.json を保存
    try:
        with open(os.path.join(OUTPUT_DIR, INDEX_FILE), 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print("-" * 30)
        print(f"✅ 復元完了！")
        print(f"■ 登録ファイル数: {len(chunks)}")
        print(f"■ 保存先: {INDEX_FILE}")
        print("-" * 30)
        
        # 新規ファイルが含まれているか確認
        new_files = ["ch_calculation_extra.json", "ch_calculation_evm.json", "ch_calculation_metrics.json"]
        found_count = 0
        for chunk in chunks:
            for new_file in new_files:
                if new_file in chunk["path"]:
                    found_count += 1
        
        if found_count >= 3:
            print("✨ 新規追加した計算問題ファイルも正しくリストに含まれています！")

    except Exception as e:
        print(f"❌ 書き込みエラー: {e}")

if __name__ == "__main__":
    restore_index_structure()
    input("エンターキーを押して終了...")
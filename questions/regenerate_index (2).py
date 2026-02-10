import json
import os
import glob

OUTPUT_DIR = "."
INDEX_FILE = "index.json"

def regenerate_index():
    print("--- index.json の再生成（更新）を開始 ---")
    
    all_questions = []
    # フォルダ内の全jsonファイルを取得
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
    
    file_count = 0

    for file_path in json_files:
        filename = os.path.basename(file_path)
        
        # 自分自身や設定ファイルは除外
        if filename in [INDEX_FILE, "package.json", "manifest.json", "tsconfig.json"]:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                all_questions.extend(data)
                file_count += 1
                # print(f"  読み込み: {filename} ({len(data)}問)")

        except Exception as e:
            print(f"  ⚠️ スキップ: {filename} ({e})")

    # index.json を書き出し
    try:
        with open(os.path.join(OUTPUT_DIR, INDEX_FILE), 'w', encoding='utf-8') as f:
            json.dump(all_questions, f, ensure_ascii=False, indent=2)
            
        print("-" * 30)
        print(f"✅ 更新完了！")
        print(f"■ 読み込んだファイル数: {file_count}")
        print(f"■ 合計問題数: {len(all_questions)} 問")
        print(f"■ 出力先: {INDEX_FILE}")
        print("-" * 30)
        
        # 新規追加ファイルの確認
        new_files = ["ch_calculation_extra.json", "ch_calculation_evm.json", "ch_calculation_metrics.json"]
        found_new = [f for f in new_files if os.path.exists(f)]
        if found_new:
            print(f"✨ 以下の新規ファイルも正しく取り込まれました:\n   {', '.join(found_new)}")
        else:
            print("※ 新規ファイルが見当たりません。作成スクリプトを実行しましたか？")

    except Exception as e:
        print(f"❌ 書き込みエラー: {e}")

if __name__ == "__main__":
    regenerate_index()
    input("エンターキーを押して終了...")
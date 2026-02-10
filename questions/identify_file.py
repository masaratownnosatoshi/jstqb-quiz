import json
import os
import glob

def identify_file():
    print("--- 問題ファイルの特定を開始 ---")
    
    # 検索するキーワード（問題文に含まれる特徴的なフレーズ）
    target_keyword = "放射線治療機器"
    
    # カレントディレクトリの全JSONファイルを走査
    json_files = glob.glob(os.path.join(".", "*.json"))
    found = False

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    q_text = str(q.get("question", ""))
                    
                    # キーワードが見つかったら報告
                    if target_keyword in q_text:
                        filename = os.path.basename(file_path)
                        q_id = q.get("id")
                        options = q.get("options")
                        answer = q.get("answer")
                        
                        print(f"\n★ 発見しました！")
                        print(f"■ ファイル名: {filename}")
                        print(f"■ 問題ID: {q_id}")
                        print(f"■ 現在の選択肢: {options}")
                        print(f"■ 現在の正解: {answer}")
                        
                        if not options or options == [""]:
                             print("  -> ⚠️ 選択肢が空です！修正が必要です。")
                        else:
                             print("  -> 選択肢は入っています。キャッシュの問題の可能性があります。")
                        
                        found = True
                        return # 1つ見つかれば終了

        except Exception as e:
            continue

    if not found:
        print("\n❌ 該当する問題を含むファイルが見つかりませんでした。")
        print("フォルダ内にJSONファイルが存在するか、キーワードが正しいか確認してください。")

    print("\nエンターキーを押して終了してください...")

if __name__ == "__main__":
    identify_file()
    input()
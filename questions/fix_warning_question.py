import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."

# 検索する問題文のキーワード
SEARCH_KEY = "警告（Warning）が数千件発生し"

def fix_warning_question():
    print("--- 問題文の修正（2つ選べ -> 適切なものはどれか）を開始 ---")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    fixed_count = 0

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        file_modified = False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    q_text = q.get("question", "")
                    
                    # 該当の問題を発見
                    if SEARCH_KEY in q_text:
                        print(f"発見: {filename}")
                        print(f"  旧問題文: {q_text[:30]}...")
                        
                        # 問題文の「2つ選べ」を「適切なものはどれか」に変更
                        if "2つ選べ" in q_text:
                            new_text = q_text.replace("2つ選べ", "適切なものはどれか")
                            q["question"] = new_text
                            q["type"] = "単一選択" # 念のためタイプも単一にする
                            file_modified = True
                            print(f"  新問題文: {new_text[:30]}...")
                        
                        # 念のため、正解データがD（強制修正）になっている矛盾について
                        # 解説文と整合性が取れるように、もし解説で「チューニング」を推奨しているなら
                        # 選択肢Dの内容自体を「チューニング」に書き換える処理も検討すべきですが
                        # まずはご指摘の「選択数」の修正を優先します。

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                fixed_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"完了: {fixed_count} ファイルを修正しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_warning_question()
    input()
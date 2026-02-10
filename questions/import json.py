import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."

# 検索キー（問題文の一部）
SEARCH_KEY = "目標の80%のアクセスでサーバがダウンした"

# 新しい選択肢B（適切な対応策）
NEW_OPTION_B = "流量制御（スロットリング）などの緩和策を検討し、システムダウンだけは回避する運用案を策定する"

def fix_ec_loadtest_question():
    print("--- ECサイト負荷テスト問題の修正を開始 ---")
    
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
                        print(f"  ID: {q.get('id')}")
                        
                        # 選択肢B（インデックス1）を修正
                        if len(q["options"]) >= 2:
                            old_opt = q["options"][1]
                            if old_opt == "統計的なばらつき":
                                q["options"][1] = NEW_OPTION_B
                                file_modified = True
                                print(f"  修正前: {old_opt}")
                                print(f"  修正後: {NEW_OPTION_B}")
                            else:
                                # 念のため、すでに修正済みでないか確認
                                print(f"  (選択肢Bは既に対処済みの可能性があります: {old_opt[:10]}...)")
                        
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
    fix_ec_loadtest_question()
    input()
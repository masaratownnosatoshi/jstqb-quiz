import json
import os
import glob

OUTPUT_DIR = "."

# 検索条件（一字一句完全一致ではなく、部分一致で広く探します）
SEARCH_TEXT_1 = "大規模セール前のECサイト"
SEARCH_TEXT_2 = "目標の80%"

# 書き換える内容
# Bにある「統計的なばらつき」を、まともな選択肢（適切な対応）に変更します
NEW_OPTION_TEXT = "流量制御（スロットリング）などの緩和策を検討し、システムダウンだけは回避する運用案を策定する"

def force_fix_ec_site():
    print("--- ECサイト負荷テスト問題の再修正を開始 ---")
    
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
    found = False

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_modified = False
            
            if isinstance(data, list):
                for q in data:
                    q_text = q.get("question", "")
                    
                    # 問題文の特徴が一致するか
                    if SEARCH_TEXT_1 in q_text and SEARCH_TEXT_2 in q_text:
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # 選択肢の修正
                        if "options" in q:
                            new_options = []
                            replaced = False
                            for opt in q["options"]:
                                if "統計的なばらつき" in opt:
                                    new_options.append(NEW_OPTION_TEXT)
                                    replaced = True
                                    print("  => ゴミデータ「統計的なばらつき」を適切な選択肢に置換しました。")
                                else:
                                    new_options.append(opt)
                            
                            if replaced:
                                q["options"] = new_options
                                file_modified = True
                                found = True
            
            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                break # 見つかったら終了

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    if not found:
        print("警告: 対象の問題が見つかりませんでした。")
    
    print("-" * 30)
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    force_fix_ec_site()
    input()
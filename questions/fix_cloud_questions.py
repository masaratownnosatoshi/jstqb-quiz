import json
import os
import glob

OUTPUT_DIR = "."

def fix_cloud_questions():
    print("--- クラウド/AWS関連問題の修正を開始 ---")
    
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
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
                    
                    # 1. 時差の問題 (ch3_cloud.json 想定)
                    if "時差あり" in q_text and "対策2つ" in q_text:
                        print(f"発見(時差): {filename}")
                        # 問題文の修正
                        q["question"] = q_text.replace("対策2つ", "最も適切な対策はどれか")
                        
                        # 選択肢C(ゴミ)の修正
                        options = q.get("options", [])
                        for i, opt in enumerate(options):
                            if "統計的なばらつき" in opt:
                                options[i] = "重要な意思決定はすべて同期会議（リアルタイム）で行い、参加できないメンバーには後で決定事項のみを通達する"
                                print("  => 選択肢Cを修正しました")
                        
                        file_modified = True

                    # 2. AWS知識不足の問題
                    if "AWS知識不足" in q_text and "施策2つ" in q_text:
                        print(f"発見(AWS育成): {filename}")
                        # 問題文の修正
                        q["question"] = q_text.replace("育成施策2つ", "最も適切な育成施策はどれか")
                        file_modified = True
                        print("  => 問題文を単一選択形式に修正しました")

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
    fix_cloud_questions()
    input()
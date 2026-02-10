import json
import os
import glob

OUTPUT_DIR = "."

# 修正対象
SEARCH_TEXT = "テスト自動化エンジニアのキャリアパス設計"

# 修正後のきれいな選択肢
NEW_OPTIONS = [
    "プログラミング言語の教本を渡し、独学で文法をマスターするまで業務には参加させない",
    "自動化ツールをゼロから選定させ、比較検討レポートを作成させることで、ツールの特性を深く理解させる",
    "既存の「キーワード駆動フレームワーク」を使用したテストケースのデータ入力や、簡単なスクリプトのメンテナンスから始めさせ、徐々にコードに触れる機会を増やす",
    "高度なCI/CDパイプラインの構築を任せ、DevOpsの全体像を理解させることで、自動化の意義を学ばせる"
]

# 正しい正解（C）
NEW_ANSWER = [
    "既存の「キーワード駆動フレームワーク」を使用したテストケースのデータ入力や、簡単なスクリプトのメンテナンスから始めさせ、徐々にコードに触れる機会を増やす"
]

def fix_automation_career_question():
    print(f"--- 問題「{SEARCH_TEXT}」の修正を開始 ---")
    
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "**/*.json"), recursive=True)
    found = False

    for file_path in json_files:
        if "index.json" in file_path or "package.json" in file_path:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_modified = False
            
            if isinstance(data, list):
                for q in data:
                    q_text = q.get("question", "")
                    
                    if SEARCH_TEXT in q_text:
                        print(f"発見: {os.path.basename(file_path)} (ID: {q.get('id')})")
                        
                        # 選択肢と正解を更新
                        q["options"] = NEW_OPTIONS
                        q["answer"] = NEW_ANSWER
                        
                        file_modified = True
                        found = True
                        print("  => 選択肢のヒント（カッコ書き）を削除しました。")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {os.path.basename(file_path)}")
                break

        except Exception as e:
            continue

    if not found:
        print("⚠️ 警告: 該当する問題が見つかりませんでした。")

    print("-" * 30)
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_automation_career_question()
    input()
import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード
SEARCH_TEXT = "欠陥のライフサイクル管理"
SEARCH_SUBTEXT = "修正完了（Fixed）"

# 修正後のきれいな選択肢
NEW_OPTIONS = [
    "開発者の修正が不完全であったため、ステータスを「Reopened（差し戻し）」にし、新たなバグについては別の新規レポート（New）を起票して関連付ける",
    "修正完了ステータスのままにしておき、備考欄に「まだ直っていません」と追記して、開発者が気づくのを待つ",
    "ステータスを「Closed」にしてレポートを閉じ、直っていない現象については全く新しい別のバグとして新規起票する",
    "開発者を呼び出してその場で修正させ、直ったことを確認してからステータスを「Closed（完了）」に変更することで、これ以上の手戻りを防ぐ"
]

# 正解の選択肢（A）
NEW_ANSWER = [
    "開発者の修正が不完全であったため、ステータスを「Reopened（差し戻し）」にし、新たなバグについては別の新規レポート（New）を起票して関連付ける"
]

def fix_defect_lifecycle():
    print("--- 欠陥ライフサイクル管理問題の修正を開始 ---")
    
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
                    
                    # 問題文の一致確認
                    if SEARCH_TEXT in q_text and SEARCH_SUBTEXT in q_text:
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # 選択肢と正解を更新
                        q["options"] = NEW_OPTIONS
                        q["answer"] = NEW_ANSWER
                        
                        file_modified = True
                        found = True
                        print("  => 選択肢のカッコ書き（注釈）を削除しました。")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                break # 見つかったら終了

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    if not found:
        print("警告: 該当する問題が見つかりませんでした。")

    print("-" * 30)
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_defect_lifecycle()
    input()
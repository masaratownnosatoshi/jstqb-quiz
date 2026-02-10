import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード
SEARCH_TEXT = "テストプロセス改善計画の策定"
SEARCH_SUBTEXT = "回帰テストの実行に時間がかかりすぎる"

# 修正後のきれいな選択肢
NEW_OPTIONS = [
    "回帰テストの実施頻度を減らし、リリース直前の1回のみ実行することで、全体のテスト時間を短縮する",
    "テストケースの内容を簡略化し、詳細な手順を省略することで、テスト実行にかかる時間を短縮する",
    "リスクベースでテストケースの優先順位付けを行い、高リスクなテストケースを自動化することで、効率的な回帰テストを実現する",
    "テスト担当者を倍増させ、手動テストを並列で実行することで時間短縮を図る"
]

# 正解の選択肢（C）
NEW_ANSWER = [
    "リスクベースでテストケースの優先順位付けを行い、高リスクなテストケースを自動化することで、効率的な回帰テストを実現する"
]

def fix_test_process_improvement():
    print("--- テストプロセス改善問題の修正を開始 ---")
    
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
    fix_test_process_improvement()
    input()
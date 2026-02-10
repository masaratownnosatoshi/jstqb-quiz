import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード
SEARCH_TEXT = "自動化チームと手動テストチームが分断"

# 新しい選択肢（Bを修正）
NEW_OPTIONS = [
    "両チームを統合し、自動化エンジニアを手動テスターの中に配置して、自動化可能なケースを一緒に選定する",
    "自動化エンジニアを物理的に隔離し、技術的な実装作業のみに集中させて効率化を図る", # 修正：分断を助長する誤答
    "自動化チームを解散し、開発者にテストコード作成をすべて委託する",
    "「自動化」をサービスとして手動チームに提供する形にし、定期的な同期ミーティングを設ける"
]

# 新しい正解（AとD）
NEW_ANSWER = [
    "両チームを統合し、自動化エンジニアを手動テスターの中に配置して、自動化可能なケースを一緒に選定する",
    "「自動化」をサービスとして手動チームに提供する形にし、定期的な同期ミーティングを設ける"
]

def fix_automation_team_conflict():
    print("--- 自動化チーム連携問題の修正を開始 ---")
    
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
                    if SEARCH_TEXT in q_text:
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # 選択肢、正解、解説を更新
                        q["options"] = NEW_OPTIONS
                        q["answer"] = NEW_ANSWER
                        q["explanation"] = "【解説】\nサイロ化（分断）を防ぐには、以下の2つのアプローチが有効です。\n1. **チーム統合 (A)**: 自動化エンジニアをテストチーム内に配置し、密に協働する。\n2. **サービス化と同期 (D)**: 別チームであっても、自動化をサービスとして提供し、定例会議で連携を密にする（Test Automation CoEモデル）。\n\n※物理的な隔離(B)は分断を悪化させ、丸投げ(C)は品質責任の放棄につながります。"
                        
                        file_modified = True
                        found = True
                        print("  => 選択肢Bを修正し、正解をAとDの2つに設定しました。")

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
    fix_automation_team_conflict()
    input()
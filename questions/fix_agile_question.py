import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."

# 検索キー（問題文の一部）
SEARCH_KEY = "I群：ユニット/統合テスト"

# 新しい問題文（群の記述を削除し、戦略を問う内容にシンプル化）
NEW_QUESTION_TEXT = """あなたはアジャイル開発プロジェクトのテストマネージャである。

【プロジェクト状況】
・2週間スプリントで開発中。
・開発者は「ユニットテスト」を実装しているが、カバレッジは低い。
・QAチームはスプリント末期に「システムテスト（手動）」を行っているが、バグが多く発見され、修正が次スプリントに持ち越される（負債化する）ケースが増えている。

【課題】
「スプリント内での品質完結（Done）」を実現するために、テストレベルと役割分担を再構成したい。

アジャイルの原則およびシフトレフトの観点から、チームが取るべき最も適切な戦略はどれか。"""

def fix_agile_question():
    print("--- アジャイル「組み合わせ」問題の修正を開始 ---")
    
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
                    
                    # 該当の問題を発見（I群...という記述があるもの）
                    if SEARCH_KEY in q_text:
                        print(f"発見: {filename}")
                        print(f"  ID: {q.get('id')}")
                        
                        # 問題文を差し替え
                        q["question"] = NEW_QUESTION_TEXT
                        file_modified = True
                        print("  => 問題文から「組み合わせ（I群...）」の記述を削除しました。")
                        
                        # 念のため、不自然な選択肢C（人事評価）も、もう少し文脈に合う誤答に直しておきます
                        # C: 「個人の責任として人事評価を下げる」 -> 
                        # C: 「開発者は機能実装に集中させるため、テストはすべてQAチームに委譲し、分業を徹底する」
                        # (※Bと被るなら「自動化を諦めて人海戦術」などにしても良いですが、
                        #  今回は質問の意図に従い問題文修正を優先します)

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
    fix_agile_question()
    input()
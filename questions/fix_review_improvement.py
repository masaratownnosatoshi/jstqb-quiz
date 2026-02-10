import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード
SEARCH_KEYWORDS = ["設計書のレビュー会", "てにをは"]

# 正しい正解リスト（AとDの2つ）
NEW_ANSWER = [
    "事前にスペルチェックツール等で形式的なミスを排除してからレビューに臨む",
    "「チェックリストベースドリーディング」を採用し、セキュリティ、パフォーマンス等の具体的な観点を各レビュアーに割り当てる"
]

def fix_review_improvement():
    print("--- レビュー改善策問題の修正を開始 ---")
    
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
                    
                    # キーワード一致確認
                    if all(k in q_text for k in SEARCH_KEYWORDS):
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # 正解を修正（AとD）
                        q["answer"] = NEW_ANSWER
                        
                        # 解説も2つに対応するように修正
                        q["explanation"] = "【解説】\n形式的なミス（てにをは）に目がいくのを防ぐには、以下の2点が有効です。\n1. **事前除去 (A)**: ツールで機械的に排除し、人間は中身に集中できる状態にします。\n2. **観点の強制 (D)**: チェックリストや役割（パースペクティブ）を与えることで、強制的に論理的な欠陥に目を向けさせます。"
                        
                        file_modified = True
                        found = True
                        print("  => 正解を「AとD」の2つに修正しました。")

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
    fix_review_improvement()
    input()
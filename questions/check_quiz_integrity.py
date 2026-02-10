import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."

# 検知したいゴミデータのキーワード
GARBAGE_PATTERNS = [
    "統計的なばらつき",
    "報告せずにこっそりと修正し",
    "リスクを受容したことにして、対策を先送りする",
    "2つ選べ"  # 正解が1つなのに2つ選べと言っている系
]

def check_quiz_integrity():
    print("=== クイズデータ健全性チェックを開始します ===")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    error_count = 0
    warning_count = 0

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    q_id = q.get("id", "不明")
                    options = q.get("options", [])
                    answer = q.get("answer", [])
                    question = q.get("question", "")
                    
                    issues = []

                    # 1. 選択肢が空っぽチェック
                    if any(not opt.strip() for opt in options):
                        issues.append("★【致命的】空の選択肢が含まれています")

                    # 2. 選択肢の重複チェック
                    if len(options) != len(set(options)):
                        issues.append("★【致命的】選択肢の内容が重複しています")

                    # 3. 正解リンク切れチェック
                    if answer and answer[0] not in options:
                        issues.append("★【致命的】正解データが選択肢の中にありません")

                    # 4. 選択肢の数チェック（通常は4択のはず）
                    if len(options) < 2:
                        issues.append("★【致命的】選択肢が少なすぎます（2個未満）")

                    # 5. ゴミデータ・不整合チェック
                    for pattern in GARBAGE_PATTERNS:
                        if any(pattern in opt for opt in options):
                            issues.append(f"△【警告】ゴミデータ疑い: 「{pattern}」")
                    
                    if "2つ選べ" in question and len(answer) == 1:
                        issues.append("△【警告】問題文は「2つ選べ」ですが、正解が1つしかありません")

                    # エラーがあれば表示
                    if issues:
                        print(f"\n■ ファイル: {filename} (ID: {q_id})")
                        print(f"  問題文: {question[:30]}...")
                        for issue in issues:
                            print(f"  - {issue}")
                        
                        # 重複や空がある場合は詳細を表示
                        if any("致命的" in i for i in issues):
                            print("  [現在の選択肢]:")
                            for i, opt in enumerate(options):
                                print(f"    {i+1}: '{opt}'")
                            error_count += 1
                        else:
                            warning_count += 1

        except Exception as e:
            print(f"エラー: {filename} を読み込めませんでした ({e})")

    print("\n" + "=" * 40)
    print(f"診断終了: 致命的なエラー {error_count} 件, 警告 {warning_count} 件")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    check_quiz_integrity()
    input()
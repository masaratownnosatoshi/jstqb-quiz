import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."

# 新しい選択肢D（アンチパターン：リトライ運用）
NEW_OPTION_D = "CIパイプライン上で「失敗したら自動リトライ（再実行）」する設定を追加し、偶然成功すれば問題なしとして運用を続ける"

def force_fix_flaky():
    print("--- Flaky問題の捜索と修正を開始 ---")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    fixed_count = 0
    found_any = False

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
                    
                    # 条件を緩くして検索 ("Flaky" という単語さえあれば対象とみなす)
                    if "Flaky" in q_text:
                        found_any = True
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        options = q.get("options", [])
                        is_target_option = False
                        
                        # 選択肢の中に「統計的」なものがあるか探す
                        for i, opt in enumerate(options):
                            if "統計的" in opt:
                                print(f"  ゴミデータ検出: {opt}")
                                options[i] = NEW_OPTION_D
                                file_modified = True
                                is_target_option = True
                                print(f"  => 修正しました: {NEW_OPTION_D[:20]}...")
                        
                        if not is_target_option:
                            print("  (この問題には「統計的」な選択肢はありませんでした)")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                fixed_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    if not found_any:
        print("警告: 「Flaky」という文字を含む問題自体が見つかりませんでした。")
    else:
        print(f"完了: {fixed_count} ファイルを修正しました。")
    
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    force_fix_flaky()
    input()
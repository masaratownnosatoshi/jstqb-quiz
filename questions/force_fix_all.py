import json
import os
import re
import glob

# カレントディレクトリの全jsonファイルを対象
TARGET_DIR = "."

# 削除パターンの強化
# 1. 全角カッコ（内容）
# 2. その後ろに空白があっても許容 (\s*)
# 3. 行末 ($)
REMOVE_PATTERN = re.compile(r'（[^）]+）\s*$')

def force_fix_all():
    print("--- 全ファイル一括修正開始 ---")
    
    # ディレクトリ内の全JSONファイルを取得
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    
    fixed_count = 0
    total_files = 0

    for file_path in json_files:
        # index.json は除外
        if "index.json" in file_path:
            continue
            
        total_files += 1
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            
            if isinstance(data, list):
                for q in data:
                    if "options" in q:
                        new_options = []
                        for opt in q["options"]:
                            # 正規表現で削除 & 右側の空白削除
                            new_opt = REMOVE_PATTERN.sub('', opt).rstrip()
                            
                            if new_opt != opt:
                                modified = True
                                # デバッグ用：何が消えたか表示
                                print(f"修正: {opt} -> {new_opt}")
                            new_options.append(new_opt)
                        q["options"] = new_options
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                fixed_count += 1
        
        except Exception as e:
            print(f"エラー読み込み不可: {filename} ({e})")

    print("-" * 30)
    print(f"処理終了: 対象{total_files}ファイル中、{fixed_count}ファイルを修正しました。")

if __name__ == "__main__":
    force_fix_all()
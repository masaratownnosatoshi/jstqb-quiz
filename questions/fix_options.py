import json
import os
import re
import glob

# 対象とするディレクトリ（カレントディレクトリ）
TARGET_DIR = "."

# 修正対象のボリューム範囲 (Vol.96 〜 Vol.120)
TARGET_VOL_START = 96
TARGET_VOL_END = 120

# 削除対象のパターン（選択肢の末尾にある全角カッコとその中身）
# 例: "〜である（コスト増のリスク）" -> "〜である"
REMOVE_PATTERN = re.compile(r'（[^）]+）$')

def fix_files():
    print(f"--- 修正開始: Vol.{TARGET_VOL_START} 〜 Vol.{TARGET_VOL_END} ---")
    
    # ファイル名パターンに一致するものを取得 (例: ch1_general_vol96.json)
    # 念のため全jsonを取得してから、vol番号でフィルタリングします
    all_json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    
    processed_count = 0

    for file_path in all_json_files:
        filename = os.path.basename(file_path)
        
        # ファイル名からボリューム番号を抽出 (vol96, vol100等)
        match = re.search(r'vol(\d+)', filename)
        if not match:
            continue
            
        vol_num = int(match.group(1))
        
        # 指定範囲外ならスキップ
        if not (TARGET_VOL_START <= vol_num <= TARGET_VOL_END):
            continue

        try:
            # 1. ファイル読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            
            # 2. データ修正
            if isinstance(data, list):
                for q in data:
                    if "options" in q:
                        new_options = []
                        for opt in q["options"]:
                            # 正規表現で末尾の（）を削除し、右側の空白も削除
                            new_opt = REMOVE_PATTERN.sub('', opt).rstrip()
                            
                            if new_opt != opt:
                                modified = True
                            new_options.append(new_opt)
                        q["options"] = new_options
            
            # 3. 保存（変更があった場合のみ）
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"修正完了: {filename}")
                processed_count += 1
            else:
                print(f"変更なし: {filename}")

        except Exception as e:
            print(f"エラー ({filename}): {e}")

    print("-" * 30)
    print(f"完了: 合計 {processed_count} ファイルを修正しました。")

if __name__ == "__main__":
    fix_files()
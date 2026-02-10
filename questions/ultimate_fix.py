import json
import os
import glob
import re
import difflib

TARGET_DIR = "."

# 正規表現: 末尾の ( ) や （ ） を、改行やスペースごと削除
# 貪欲マッチにして、一番後ろの閉じ括弧から遡る
CLEAN_REGEX = re.compile(r'\s*[（\(].*?[）\)]\s*$', re.DOTALL)

def clean_text(text):
    """テキストから末尾の括弧説明を削除する"""
    if not isinstance(text, str):
        return text
    # 正規表現で置換
    cleaned = CLEAN_REGEX.sub('', text)
    return cleaned.strip()

def get_best_match(target, options):
    """正解テキストに最も近い選択肢を探す（類似度判定）"""
    if not options:
        return None
    # 1. 完全一致
    if target in options:
        return target
    # 2. 類似度（0.5以上で最も似ているものを採用）
    matches = difflib.get_close_matches(target, options, n=1, cutoff=0.5)
    if matches:
        return matches[0]
    return None

def ultimate_fix():
    print("=== 最終完全修復処理 (Ultimate Fix) を開始 ===")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    total_fixed = 0
    
    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        file_changed = False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    q_id = q.get('id', 'unknown')
                    
                    # --- 1. 選択肢のクリーニング ---
                    if "options" in q:
                        new_opts = []
                        for opt in q["options"]:
                            cleaned = clean_text(opt)
                            if cleaned != opt:
                                file_changed = True
                            new_opts.append(cleaned)
                        q["options"] = new_opts
                    
                    # --- 2. 正解データのクリーニングと強制同期 ---
                    if "answer" in q and len(q["answer"]) > 0:
                        original_ans = q["answer"][0]
                        cleaned_ans = clean_text(original_ans)
                        
                        # 選択肢の中からベストマッチを探す（強制同期）
                        best_match = get_best_match(cleaned_ans, q["options"])
                        
                        if best_match:
                            # 正解データが選択肢と異なる場合（ゴミ削除含む）、選択肢の文言で上書きする
                            if original_ans != best_match:
                                print(f"  [修正] {filename} ({q_id})")
                                print(f"    正解(旧): {original_ans[:30]}...")
                                print(f"    正解(新): {best_match[:30]}...")
                                q["answer"] = [best_match]
                                file_changed = True
                        else:
                            # 万が一マッチしなくても、クリーニング結果は反映する
                            if original_ans != cleaned_ans:
                                q["answer"] = [cleaned_ans]
                                file_changed = True
                                print(f"  [置換] {filename} ({q_id}) クリーニングのみ適用")

            if file_changed:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                total_fixed += 1

        except Exception as e:
            print(f"エラー: {filename} - {e}")

    print("=" * 40)
    print(f"完了: {total_fixed} ファイルを修復しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    ultimate_fix()
    input()
import json
import os
import glob

# 対象ディレクトリ
TARGET_DIR = "."

def get_char_set(text):
    """
    文字列から記号や空白を除去し、文字のセット（集合）を返す
    比較の厳密度を下げるための処理
    """
    # 意味のある文字だけを残す（漢字、ひらがな、カタカナ、英数字）
    # 簡易的に、空白や一般的な記号を除外
    ignore_chars = " 、。！？!?,.()（）「」[]{}\t\n　"
    cleaned = "".join([c for c in text if c not in ignore_chars])
    return set(cleaned)

def calculate_similarity(text_a, text_b):
    """
    2つの文字列の文字集合の類似度（Jaccard係数っぽいもの）を計算
    """
    set_a = get_char_set(text_a)
    set_b = get_char_set(text_b)
    
    if not set_a or not set_b:
        return 0.0
    
    # 積集合（共通する文字）
    intersection = set_a.intersection(set_b)
    # 和集合（全文字）
    union = set_a.union(set_b)
    
    return len(intersection) / len(union)

def emergency_fix():
    print("=== 緊急救済処理（文字集合マッチング）を開始 ===")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
    fixed_count = 0
    manual_check_needed = []

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
                    if "answer" in q and q["answer"] and "options" in q:
                        current_ans = q["answer"][0]
                        options = q["options"]
                        
                        # 正解が選択肢にない場合
                        if current_ans not in options:
                            best_match = None
                            highest_score = 0.0
                            
                            # 全選択肢と比較
                            for opt in options:
                                score = calculate_similarity(current_ans, opt)
                                if score > highest_score:
                                    highest_score = score
                                    best_match = opt
                            
                            # 類似度が0.6 (60%) 以上なら採用
                            if highest_score > 0.6:
                                q["answer"] = [best_match]
                                file_modified = True
                                print(f"  [修復成功] {filename}")
                                print(f"    類似度: {highest_score:.2f}")
                                print(f"    旧: {current_ans[:20]}...")
                                print(f"    新: {best_match[:20]}...")
                            else:
                                # マッチしなかった場合、情報を記録
                                msg = f"  [修復不能] {filename} (ID:{q.get('id')}) - スコア:{highest_score:.2f}\n    Ans: {current_ans}\n    Opt: {options}"
                                manual_check_needed.append(msg)

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                fixed_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("=" * 40)
    print(f"完了: {fixed_count} ファイルを救済しました。")
    
    if manual_check_needed:
        print("\n--- 自動修復できなかった問題（手動確認用） ---")
        for msg in manual_check_needed:
            print(msg)
            print("-" * 20)

    print("\nエンターキーを押して終了してください...")

if __name__ == "__main__":
    emergency_fix()
    input()
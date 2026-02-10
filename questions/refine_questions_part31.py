import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第31弾・Vol.43-46 計算・分析強化）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.46 (ch2_general_vol46.json)
    # ---------------------------
    "Q2-GEN-V46-01": { # レビュー準備の速度評価
        "options": [
            "速度は 40ページ/時間 であり、速すぎて十分に内容を理解できていない可能性が高い（準備不足）",
            "速度は 10ページ/時間 であり、適切である（標準的な範囲）",
            "速度は 0.6ページ/時間 であり、遅すぎる（熟読しすぎている）",
            "速度は 40ページ/時間 であり、非常に効率よくチェックできているため、高い評価を与える（速度偏重の誤り）" # 「短いほど優秀」を修正
        ],
        "answer": ["速度は 40ページ/時間 であり、速すぎて十分に内容を理解できていない可能性が高い（準備不足）"]
    },

    # ---------------------------
    # 第2章 一般 Vol.46_2 (ch2_general_vol46_2.json)
    # ---------------------------
    "Q2-GEN-V46-03": { # DDP (欠陥検出率) 計算
        "options": [
            "20%（システムテスト単体の検出率と誤認）",
            "40%（単体テストでの検出率と誤認）", # 「計算不能」を修正
            "90%（正解：リリース前検出数 / 総欠陥数）",
            "100%（全検出と誤認）"
        ],
        "answer": ["90%（正解：リリース前検出数 / 総欠陥数）"]
    }
}

# ==========================================
# セーフティネット（不適切ワードの最終除去）
# ==========================================
bad_patterns = {
    "計算不能": "データ不足のため判断を保留する",
    "運": "統計的なばらつき",
    "気合": "リソースの再配分",
    "罰金": "プロセス改善",
    "解雇": "教育・訓練",
    "諦める": "リスクを受容する"
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第31弾：計算・分析問題の最終ブラッシュアップを開始します...")

    for file_path in all_files:
        filename = os.path.basename(file_path)
        if filename.endswith(".py") or filename == "index.json":
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                continue

            file_modified = False
            
            for q in data:
                q_id = q.get("id")
                
                # 1. 特定IDの修正
                if q_id in fixes:
                    fix_data = fixes[q_id]
                    if "options" in fix_data:
                        q["options"] = fix_data["options"]
                    if "answer" in fix_data:
                        q["answer"] = fix_data["answer"]
                    if "explanation" in fix_data:
                        q["explanation"] = fix_data["explanation"]
                    print(f"  修正適用 (ID指定): {q_id}")
                    file_modified = True

                # 2. セーフティネット（キーワード置換）
                if "options" in q:
                    new_options = []
                    options_changed = False
                    for opt in q["options"]:
                        replaced = False
                        for bad_word, better_phrase in bad_patterns.items():
                            if bad_word in opt and better_phrase not in opt:
                                # 数値選択肢の場合は置換しない（誤検知防止）
                                if not any(char.isdigit() for char in opt): 
                                    new_options.append(better_phrase)
                                    print(f"  自動修正 (キーワード '{bad_word}'): {q_id}")
                                    replaced = True
                                    options_changed = True
                                    break
                        if not replaced:
                            new_options.append(opt)
                    
                    if options_changed:
                        q["options"] = new_options
                        file_modified = True

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                updated_count += 1
                
        except Exception as e:
            print(f"  読み込みエラー: {filename} - {e}")

    print("-" * 30)
    print(f"完了: 合計 {updated_count} ファイルを最適化しました。")

if __name__ == "__main__":
    refine_questions()
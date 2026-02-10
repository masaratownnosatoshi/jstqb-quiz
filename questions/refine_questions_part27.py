import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第27弾・Vol.37-38 計算強化 & 最終クリーニング）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.38 (ch2_general_vol38.json)
    # ---------------------------
    "Q2-GEN-V38-01": { # DDP (欠陥検出率) 計算
        "options": [
            "20%（これは欠陥流出率）",
            "25%（UATでの検出率）",
            "80%（正解：ST検出数 / 総欠陥数）",
            "100%（理想値だが現実的ではない）"
        ],
        "answer": ["80%（正解：ST検出数 / 総欠陥数）"]
    },

    # ---------------------------
    # 第3章 一般 Vol.37 (ch3_general_vol37.json)
    # ---------------------------
    "Q3-GEN-V37-01": { # ベロシティ予測
        "options": [
            "24ポイント（稼働率減を考慮した妥当な予測）",
            "30ポイント（平均値そのまま：休暇を考慮していない）",
            "35ポイント（ベストケース：楽観的すぎる）",
            "6ポイント（休暇メンバーの分を引くのではなく、休暇メンバーの分だけを見積もってしまった誤り）"
        ],
        "answer": ["24ポイント（稼働率減を考慮した妥当な予測）"]
    }
}

# ==========================================
# 禁止ワードと置換用アンチパターン（セーフティネット）
# ==========================================
# これまでのファイルに含まれるかもしれない「低品質な選択肢」を
# キーワード検知で自動的に「それっぽい誤答」に書き換えます。
bad_patterns = {
    "罰金": "個人の責任として人事評価を下げる（心理的安全性の破壊）",
    "解雇": "担当者を交代させるが、プロセスの問題は解決しない（根本原因の未解決）",
    "気合": "リソースを追加せず、残業と休日出勤でカバーするよう指示する（デスマーチ）",
    "怒鳴る": "厳しい態度で指導し、緊張感を持たせる（パワーハラスメント）",
    "諦める": "リスクを受容したことにして、対策を先送りする（問題の放置）",
    "隠蔽": "報告せずにこっそりと修正し、記録に残さない（コンプライアンス違反）",
    "嘘": "報告内容を鵜呑みにせず、エビデンス（ログ等）ベースの確認に切り替える",
    "土下座": "ステークホルダーに誠意を見せて納得してもらう"
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第27弾：計算問題の強化と最終クリーニングを開始します...")

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
                
                # 1. 特定IDの修正（計算問題の選択肢強化）
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

                # 2. キーワード検知による自動修正（セーフティネット）
                # 選択肢を走査し、禁止ワードが含まれていたら置換する
                if "options" in q:
                    new_options = []
                    options_changed = False
                    for opt in q["options"]:
                        replaced = False
                        for bad_word, better_phrase in bad_patterns.items():
                            if bad_word in opt and better_phrase not in opt: # 既に修正済みでなければ
                                new_options.append(better_phrase)
                                print(f"  自動修正 (キーワード '{bad_word}'): {q_id}")
                                replaced = True
                                options_changed = True
                                break # 1つの選択肢に複数の禁止ワードがあっても1回置換すればOK
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
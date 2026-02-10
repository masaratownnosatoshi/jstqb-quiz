import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第29弾・Vol.29, 39 補完）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.29 (ch2_general_vol29.json)
    # ---------------------------
    "Q2-GEN-V29-02": { # OSSツールリスク
        "options": [
            "初期導入コスト（ライセンス費）が高額になること",
            "ベンダーによる公式サポートがないため、不具合発生時や機能拡張の際に自力で対応（またはコミュニティ依存）する工数・技術力が必要になること",
            "機能が多すぎて使いこなせないこと",
            "コミュニティが不活発で、将来的なアップデートやバグ修正が期待できないこと（サステナビリティ）" # 日本語マニュアル -> サステナビリティ
        ],
        "answer": ["ベンダーによる公式サポートがないため、不具合発生時や機能拡張の際に自力で対応（またはコミュニティ依存）する工数・技術力が必要になること"]
    },

    # ---------------------------
    # 第1章 一般 Vol.39 (ch1_general_vol39.json)
    # ---------------------------
    "Q1-GEN-V39-02": { # オフショアコミュニケーション
        "options": [
            "ホールでの立ち話や飲み会などの「非公式なコミュニケーション」を重視し、仲良くなることを最優先する（ハイコンテクスト依存）",
            "言語や時差の壁があるため、非公式なコミュニケーション（阿吽の呼吸）には依存せず、明確なドキュメント定義と、共通のコミュニケーションチャネル（ツール）を確立する",
            "すべてを自動翻訳ツール任せにし、原文の確認を行わない",
            "相手の国の文化に合わせて、納期を守らなくても良いことにする（過度な妥協）"
        ],
        "answer": ["言語や時差の壁があるため、非公式なコミュニケーション（阿吽の呼吸）には依存せず、明確なドキュメント定義と、共通のコミュニケーションチャネル（ツール）を確立する"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第29弾：Vol.29/39の修正を開始します...")

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
                
                if q_id in fixes:
                    fix_data = fixes[q_id]
                    
                    if "options" in fix_data:
                        q["options"] = fix_data["options"]
                    if "answer" in fix_data:
                        q["answer"] = fix_data["answer"]
                    if "explanation" in fix_data:
                        q["explanation"] = fix_data["explanation"]

                    print(f"  修正適用: {q_id} ({filename})")
                    file_modified = True

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                updated_count += 1
                
        except Exception as e:
            print(f"  読み込みエラー: {filename} - {e}")

    print("-" * 30)
    print(f"完了: 合計 {updated_count} ファイルの問題を修正しました。")

if __name__ == "__main__":
    refine_questions()
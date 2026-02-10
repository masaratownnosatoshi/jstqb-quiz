import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第47弾・Vol.93-95 最終章補完）
# ==========================================
fixes = {
    # ---------------------------
    # 第3章 一般 Vol.94 (ch3_general_vol94.json)
    # ---------------------------
    "Q3-GEN-V94-01": { # 評価指標の弊害
        "options": [
            "テスト担当者がやる気を出す",
            "簡単なバグばかりを探すようになり、複雑で重要なバグの発見がおろそかになったり、開発者との協力関係が悪化したりする",
            "テスターと開発者が敵対関係になり、開発者が情報を隠したり、テスターが簡単なバグ報告で数稼ぎをするようになる（ハドソンの法則・コブラ効果）", # 「バグゼロ」を修正
            "開発者が感謝する"
        ],
        "answer": ["簡単なバグばかりを探すようになり、複雑で重要なバグの発見がおろそかになったり、開発者との協力関係が悪化したりする"]
    },

    # ---------------------------
    # 第3章 一般 Vol.95 (ch3_general_vol95.json)
    # ---------------------------
    "Q3-GEN-V95-01": { # メンタリングとコーチング
        "options": [
            "メンタリングは、経験豊富な先輩（メンター）が、キャリアや個人的な成長を含めて長期的に支援・助言すること。\nコーチングは、具体的なスキルやパフォーマンス向上のために、問いかけを通じて相手の能力を引き出すこと",
            "メンタリングは短期的・技術的指導（OJTに近い）、コーチングは長期的・精神的支援である（定義の混同・逆転）", # 「叱る/褒める」を修正
            "メンタリングは技術指導のみ、コーチングは精神指導のみ",
            "違いはない"
        ],
        "answer": ["メンタリングは、経験豊富な先輩（メンター）が、キャリアや個人的な成長を含めて長期的に支援・助言すること。\nコーチングは、具体的なスキルやパフォーマンス向上のために、問いかけを通じて相手の能力を引き出すこと"]
    },
    "Q3-GEN-V95-03": { # ホールチームアプローチ
        "options": [
            "開発が終わるまで待機する",
            "チームから隔離された部屋でテストする",
            "品質に対する責任を一人で負うのではなく、開発者やPOと協調し、チーム全体が品質に責任を持てるように情報提供や支援を行う",
            "品質警察（Quality Police）として振る舞い、開発者のコードの欠点を指摘するだけで改善には関与しない" # 「批判する」を具体化
        ],
        "answer": ["品質に対する責任を一人で負うのではなく、開発者やPOと協調し、チーム全体が品質に責任を持てるように情報提供や支援を行う"]
    },

    # ---------------------------
    # 第2章 一般 Vol.94 (ch2_general_vol94.json)
    # ---------------------------
    "Q2-GEN-V94-01": { # チェックリスト活用
        "options": [
            "過去のプロジェクトで使ったリストを、内容を見直さずにそのまま使い回す",
            "レビュー対象の種類（要件、設計、コード等）や、過去の欠陥傾向に合わせて、具体的かつ焦点を絞った質問項目を定義し、定期的に更新する",
            "インターネットで見つけた汎用的なリストを、プロジェクトの文脈に合わせてカスタマイズせずにそのまま適用する（形骸化リスク）", # 「1項目だけ」を修正
            "チェックリストは使わず、勘に頼る"
        ],
        "answer": ["レビュー対象の種類（要件、設計、コード等）や、過去の欠陥傾向に合わせて、具体的かつ焦点を絞った質問項目を定義し、定期的に更新する"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第47弾：Vol.93-95の最終修正を開始します...")

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
    print(f"完了: 合計 {updated_count} ファイルを最適化しました。")

if __name__ == "__main__":
    refine_questions()
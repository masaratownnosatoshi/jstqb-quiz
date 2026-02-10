import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第13弾・Vol.9 計算・分析編）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 医療 Vol.9 (ch2_medical_vol9.json)
    # ---------------------------
    "Q2-MED-V9-01": { # ALARP判定
        "options": [
            "リスクは受容できないため、製品のリリースを無期限に延期する",
            "コストと効果のバランスを考慮しつつ、実行可能な限りリスク低減策（設計変更や安全機構）を実施する",
            "リスク受容が可能であるとみなすため、追加の対策は行わず現状維持とする",
            "「ユーザーへの警告（添付文書）」のみで対策完了とし、設計変更は行わない"
        ],
        "answer": ["コストと効果のバランスを考慮しつつ、実行可能な限りリスク低減策（設計変更や安全機構）を実施する"]
    },

    # ---------------------------
    # 第3章 一般 Vol.9 (ch3_general_vol9.json)
    # ---------------------------
    "Q3-GEN-V9-02": { # ベロシティ予測
        "options": [
            "18ポイント（直近の最小値を採用し、安全側に倒す）",
            "20ポイント（直近3回の平均値を採用する - Weather Yesterday）",
            "22ポイント（直近の最高値を採用し、チャレンジ目標とする）",
            "60ポイント（過去3回の合計値を採用する）"
        ],
        "answer": ["20ポイント（直近3回の平均値を採用する - Weather Yesterday）"]
    },

    # ---------------------------
    # 第2章 一般 Vol.9 (ch2_general_vol9.json)
    # ---------------------------
    "Q2-GEN-V9-05": { # 修正確認テスト失敗率高
        "options": [
            "開発者がローカル環境でのみ確認し、ビルドやデプロイの手順を省略している可能性がある",
            "欠陥レポートの再現手順が不正確で、開発者が現象を正しく再現できずに修正したつもりになっている",
            "テスト環境のデータベースが本番と同期されておらず、データの不整合起きている",
            "テスターが修正確認の手順を誤っており、古いキャッシュを見ている可能性がある"
        ],
        "answer": [
            "開発者がローカル環境でのみ確認し、ビルドやデプロイの手順を省略している可能性がある",
            "欠陥レポートの再現手順が不正確で、開発者が現象を正しく再現できずに修正したつもりになっている"
        ]
    },
    
    # ---------------------------
    # 第1章 一般 Vol.9 (ch1_general_vol9.json) - 微調整
    # ---------------------------
    "Q1-GEN-V9-03": { # RPN優先順位 (計算結果: A=15, B=10, C=16) -> C, A, B
        "options": [
            "リスクA (15) -> リスクB (10) -> リスクC (16)",
            "リスクC (16) -> リスクA (15) -> リスクB (10)",
            "リスクB (10) -> リスクC (16) -> リスクA (15)",
            "リスクA (15) -> リスクC (16) -> リスクB (10)"
        ],
        "answer": ["リスクC (16) -> リスクA (15) -> リスクB (10)"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第13弾：問題データの修正を開始します...")

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
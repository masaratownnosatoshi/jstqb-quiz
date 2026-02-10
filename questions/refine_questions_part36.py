import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第36弾・Vol.60-62 最終調整）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.62 (ch2_general_vol62.json)
    # ---------------------------
    "Q2-GEN-V62-01": { # レビュー計画の優先度
        "options": [
            "レビュー対象となるプロダクトやプロセス",
            "レビューの投資効果（ROI）",
            "カバーすべき関連リスク要因",
            "個々のレビューアの個人的な技術的嗜好や好みに合わせること" # 「昼食メニュー」を修正
        ],
        "answer": ["個々のレビューアの個人的な技術的嗜好や好みに合わせること"]
    },

    # ---------------------------
    # 第1章 一般 Vol.62 (ch1_general_vol62.json)
    # ---------------------------
    "Q1-GEN-V62-02": { # リスクベースドテスト実行
        "options": [
            "「縦型探索（depth-first）」では、リスクの高いテストを全て実行してから、次のリスクレベルのテストに移る",
            "「横型探索（breadth-first）」では、すべてのリスクアイテムからサンプリングして広く浅くテストする",
            "リスクレベルを使用してテストの順序付けを行うことで、最も重要な欠陥を早期に検出できる",
            "「縦型探索」では、リスクレベルを無視してテストケースID順に機械的に実行する" # 「ランダム」を修正
        ],
        "answer": ["「縦型探索」では、リスクレベルを無視してテストケースID順に機械的に実行する"]
    },
    "Q1-GEN-V62-03": { # プロセス改善の意義
        "options": [
            "テストプロセスを改善することで製品品質が向上し、結果として保守リソースの削減や顧客満足度の向上につながるため",
            "テストプロセスは開発プロセスとは無関係であり、独自に改善すべきだから",
            "最新の流行りのモデルを導入することで対外的にアピールできるから",
            "プロセス標準化による管理工数の削減のみを目的にするため（品質向上を伴わないコストカット）" # 「暇つぶし」を修正
        ],
        "answer": ["テストプロセスを改善することで製品品質が向上し、結果として保守リソースの削減や顧客満足度の向上につながるため"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第36弾：Vol.60-62の最終修正を開始します...")

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
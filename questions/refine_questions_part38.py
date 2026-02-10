import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第38弾・Vol.66-69 最終仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.67 (ch2_general_vol67.json)
    # ---------------------------
    "Q2-GEN-V67-01": { # レビュー計画の優先度
        "options": [
            "レビュー対象となるプロダクトおよびプロセス",
            "レビューの投資効果（ROI）やリスク要因",
            "レビューに関与する人物（参加者）",
            "レビューアの個人的なスケジュール都合（プロジェクト全体計画を無視した日程調整）" # 「飲み会」を修正
        ],
        "answer": ["レビューアの個人的なスケジュール都合（プロジェクト全体計画を無視した日程調整）"]
    },

    # ---------------------------
    # 第1章 一般 Vol.68 (ch1_general_vol68.json)
    # ---------------------------
    "Q1-GEN-V68-01": { # 遅延時のコントロール
        "options": [
            "テスト期間を延長せず、テスト要員を減らしてコストを削減する（逆効果）",
            "テストの終了基準を見直し、ステークホルダーの承認を得てリスクの低いテストをスコープから外す（デスコープ）",
            "品質を犠牲にして、テストをスキップする",
            "予定通りの進捗に見せるために、未実行のテストを「実行済み（Skip）」として計上する（進捗の粉飾）" # 「隠す」を修正
        ],
        "answer": ["テストの終了基準を見直し、ステークホルダーの承認を得てリスクの低いテストをスコープから外す（デスコープ）"]
    },

    # ---------------------------
    # 第3章 一般 Vol.69 (ch3_general_vol69.json)
    # ---------------------------
    "Q3-GEN-V69-01": { # スキルマトリクス活用
        "options": [
            "チーム全体としてのスキルの強みと弱み（ギャップ）を特定し、採用やトレーニング計画に反映させる",
            "個人の給与査定を行う",
            "個人の昇進を決める",
            "特定の個人を非難するための材料にする（スキル不足の吊るし上げ）" # 「リストラ」を修正
        ],
        "answer": ["チーム全体としてのスキルの強みと弱み（ギャップ）を特定し、採用やトレーニング計画に反映させる"]
    },

    # ---------------------------
    # 第2章 一般 Vol.68 (ch2_general_vol68.json)
    # ---------------------------
    "Q2-GEN-V68-01": { # 無効レポートの原因
        "options": [
            "テストケースの粒度が細かすぎる、またはテストデータの準備不足による誤検知", # 「熱心」を修正
            "テスト担当者のスキル不足、テスト環境の不安定さ、またはテストベース（仕様）の品質が低いことによる非効率",
            "開発者の修正能力が低い",
            "欠陥管理ツールが使いにくい"
        ],
        "answer": ["テスト担当者のスキル不足、テスト環境の不安定さ、またはテストベース（仕様）の品質が低いことによる非効率"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第38弾：Vol.66-69の最終修正を開始します...")

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
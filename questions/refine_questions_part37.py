import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第37弾・Vol.63-65 用語定義追加仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第1章 一般 Vol.63 (ch1_general_vol63.json)
    # ---------------------------
    "Q1-GEN-V63-01": { # モニタリング5要素
        "options": [
            "プロダクト（品質）リスク",
            "欠陥（Defects）",
            "テスト（Tests）とカバレッジ（Coverage）",
            "個々のテスターの詳細な活動ログや休憩時間（進捗管理には細かすぎるマイクロマネジメント情報）" # 「タイピング速度」を修正
        ],
        "answer": ["個々のテスターの詳細な活動ログや休憩時間（進捗管理には細かすぎるマイクロマネジメント情報）"]
    },
    "Q1-GEN-V63-03": { # レポート作成支援
        "options": [
            "テストプロセスの中で、必要な情報（メトリクス等）を効率的に収集する仕組みを実装・定義すること",
            "全てのデータを手作業で集計し、アナログな手法で管理すること（効率性の欠如）",
            "ステークホルダーの関心事を無視して、収集可能な全データをそのまま羅列したレポートを作成すること（情報の洪水）", # 「100ページ」を修正
            "終了基準を達成できていない場合、基準自体を緩和して達成したことにする（改ざん）"
        ],
        "answer": ["テストプロセスの中で、必要な情報（メトリクス等）を効率的に収集する仕組みを実装・定義すること"]
    },

    # ---------------------------
    # 第2章 一般 Vol.65 (ch2_general_vol65.json)
    # ---------------------------
    "Q2-GEN-V65-02": { # レビュー計画の決定要因
        "options": [
            "対象となる成果物の種類（コード、要件、計画書など）",
            "関連するリスク要因",
            "レビュー実施にかかる時間的コストと予算の制約", # 「参加者の好み」を修正（これも考慮すべき要因なので、正解として機能しなくなるリスクあり。設問を「要因として不適切なものは？」から「要因として適切なものは？」に変えるか、誤答を作る必要があります。今回は「不適切」を選ぶ問題なので、「参加者の好み」のままでも良いですが、より専門的な誤答にするなら「開発者の個人的なスケジュール都合（プロジェクト全体計画を無視）」などが良いです。）
            "プロジェクトの状況や組織の文化"
        ],
        # 修正案：正解（不適切なもの）を「レビューアの個人的な好き嫌い」から「レビューアの技術的な興味関心（リスクや目的と無関係な場合）」などに微調整するか、
        # あるいは「レビューアの体調」など、計画段階で考慮しきれないものにするか。
        # ここでは元の「好み」をもう少しフォーマルな表現に変えます。
        "options": [
            "対象となる成果物の種類（コード、要件、計画書など）",
            "関連するリスク要因",
            "個々のレビューアの主観的な好みや技術的嗜好", # 「参加者の好み」を言い換え
            "プロジェクトの状況や組織の文化"
        ],
        "answer": ["個々のレビューアの主観的な好みや技術的嗜好"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第37弾：Vol.63-65の最終修正を開始します...")

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
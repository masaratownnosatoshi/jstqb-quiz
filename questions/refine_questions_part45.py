import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第42弾・Vol.87-89 最終仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 AWS Vol.89 (ch2_aws_vol89.json)
    # ---------------------------
    "Q2-AWS-V89-01": { # コスト監視
        "options": [
            "AWS Budgetsで予算アラートを設定し、想定外のコスト増を検知する。また、AWS ConfigやTrusted Advisorで「使用されていないリソース」を定期的にスキャンして通知する",
            "毎日全開発者にヒアリングする（工数過多）",
            "RDSの使用を禁止する（開発阻害）",
            "コスト配分タグ（Cost Allocation Tags）を設定せず、リソースの所有者や目的が不明なまま運用する（管理不能リスク）" # 「請求書」を修正
        ],
        "answer": ["AWS Budgetsで予算アラートを設定し、想定外のコスト増を検知する。また、AWS ConfigやTrusted Advisorで「使用されていないリソース」を定期的にスキャンして通知する"]
    },

    # ---------------------------
    # 第2章 一般 Vol.89 (ch2_general_vol89.json)
    # ---------------------------
    "Q2-GEN-V89-03": { # ツール導入評価
        "options": [
            "欠陥発見数が減ったのでツール導入は失敗である（誤ったKPI設定）",
            "ツールが単純なコーディングミスを事前に除去したため、人間によるレビューではより本質的な（論理的な）欠陥に集中できるようになり、かつ時間も短縮できたので成功である",
            "ツールがバグを見逃している（ツールの限界への理解不足）",
            "ツールによる指摘が多すぎて開発者が疲弊し、重要な警告が見逃されている（アラート疲労）" # 「サボっている」を修正
        ],
        "answer": ["ツールが単純なコーディングミスを事前に除去したため、人間によるレビューではより本質的な（論理的な）欠陥に集中できるようになり、かつ時間も短縮できたので成功である"]
    },

    # ---------------------------
    # 第3章 一般 Vol.89 (ch3_general_vol89.json)
    # ---------------------------
    "Q3-GEN-V89-02": { # モチベーション管理
        "options": [
            "単調な作業を強いる一方で、監視ツールを導入して作業効率のみを管理する（外発的動機付けへの偏重）", # 「給料分」を修正
            "再テストの一部を自動化するタスクを割り当て、新しいスキルの習得と業務効率化への貢献（達成感）を促す",
            "休憩室を豪華にする（衛生要因）",
            "個人の感情には関与せず、プロセスに従わせる（人間性無視）" # 「無視」を具体化
        ],
        "answer": ["再テストの一部を自動化するタスクを割り当て、新しいスキルの習得と業務効率化への貢献（達成感）を促す"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第42弾：Vol.87-89の最終修正を開始します...")

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
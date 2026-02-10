import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第17弾・Vol.13 用語定義編）
# ==========================================
fixes = {
    # ---------------------------
    # 第1章 AWS Vol.13 (ch1_aws_vol13.json)
    # ---------------------------
    "Q1-AWS-V13-01": { # CloudTrail vs CloudWatch
        "options": [
            "CloudTrailはリソースの構成変更履歴（AWS Config）を記録し、CloudWatchは課金情報を管理する",
            "CloudTrailはAPI操作ログ（誰がいつ何をしたか）の記録、CloudWatchはメトリクス（CPU使用率等）の監視とログ収集",
            "CloudTrailはVPC内の通信パケット（Flow Logs）をキャプチャし、CloudWatchは侵入検知を行う",
            "CloudTrailはアプリケーションのログ専用、CloudWatchはインフラのログ専用である"
        ],
        "answer": ["CloudTrailはAPI操作ログ（誰がいつ何をしたか）の記録、CloudWatchはメトリクス（CPU使用率等）の監視とログ収集"]
    },

    # ---------------------------
    # 第3章 クラウド Vol.13 (ch3_cloud_vol13.json)
    # ---------------------------
    "Q3-CLD-V13-01": { # DevOpsでのQAの意味
        "options": [
            "Quality Assurance（品質を保証する人：最後の砦としてリリースを承認する）",
            "Quality Assistant / Coach（品質作り込みを支援する人：開発者がテストできるよう導く）",
            "Quality Analyst（バグの統計データのみを分析し、現場には関与しない人）",
            "Quality Police（コーディング規約違反を取り締まる人）"
        ],
        "answer": ["Quality Assistant / Coach（品質作り込みを支援する人：開発者がテストできるよう導く）"]
    },

    # ---------------------------
    # 第2章 一般 Vol.13 (ch2_general_vol13.json)
    # ---------------------------
    "Q2-GEN-V13-02": { # インスペクション vs ウォークスルー
        "options": [
            "インスペクションは作成者が進行し、ウォークスルーはモデレーターが進行する",
            "インスペクションは訓練されたモデレーター主導で形式的に行われ、ウォークスルーは作成者主導でカジュアルに行われることが多い",
            "インスペクションはドキュメントのみを対象とし、ウォークスルーはソースコードのみを対象とする",
            "インスペクションは管理者への報告が不要だが、ウォークスルーは必須である"
        ],
        "answer": ["インスペクションは訓練されたモデレーター主導で形式的に行われ、ウォークスルーは作成者主導でカジュアルに行われることが多い"]
    },

    # ---------------------------
    # 第1章 一般 Vol.13 (ch1_general_vol13.json)
    # ---------------------------
    "Q1-GEN-V13-01": { # プロジェクトリスク vs プロダクトリスク
        "options": [
            "テスト環境の構築遅延や、要員不足によるスキルギャップ（プロダクトリスク）",
            "システムが特定の入力でクラッシュすることや、応答性能が要件を満たさないこと（プロジェクトリスク）",
            "第三者ベンダーからの納品物が遅れること（プロジェクトリスク）",
            "仕様変更が多発してスコープが決まらないこと（プロダクトリスク）"
        ],
        "answer": ["第三者ベンダーからの納品物が遅れること（プロジェクトリスク）"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第17弾：問題データの修正を開始します...")

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
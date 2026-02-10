import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第4弾）
# ==========================================
fixes = {
    # ---------------------------
    # 第3章 AWS Vol.2 (ch3_aws_vol2.json)
    # ---------------------------
    "Q3-AWS-V2-01": { # DevOps Engineer Professional
        "options": [
            "AWSの全サービス利用料が永年無料になる特典が付与される",
            "CI/CDパイプラインの構築やIaCのテスト戦略を主導し、高度な自動化を実現できる",
            "開発コードを書かずに、PowerPointでの設計とレビューのみに専念できる",
            "セキュリティチェックを含むすべてのリリース判定を、独断で行う権限が与えられる"
        ],
        "answer": ["CI/CDパイプラインの構築やIaCのテスト戦略を主導し、高度な自動化を実現できる"]
    },

    # ---------------------------
    # 第3章 クラウド Vol.2 (ch3_cloud_vol2.json)
    # ---------------------------
    "Q3-CLD-V2-01": { # リモートワークの孤立対策
        "options": [
            "業務中はWebカメラを常時ONにさせ、監視ツールでキー操作ログを取得してサボりを防止する",
            "バーチャルオフィスや雑談チャットなど、心理的安全性を高める場の提供とメンター制度を導入する",
            "コミュニケーションミスを防ぐため、すべての連絡をメールのみに限定し、記録を徹底管理する",
            "完全な成果主義を導入し、孤立していても個人のKPIさえ達成していれば一切干渉しない方針をとる"
        ],
        "answer": ["バーチャルオフィスや雑談チャットなど、心理的安全性を高める場の提供とメンター制度を導入する"]
    },

    # ---------------------------
    # 第2章 クラウド Vol.2 (ch2_cloud_vol2.json)
    # ---------------------------
    "Q2-CLD-V2-01": { # スケーラビリティ検証
        "options": [
            "負荷に応じてリソースを追加した際、処理能力が線形に向上するか（スケールアウト性能）",
            "データベースのバックアップからの復旧時間が、RTO（目標復旧時間）を満たしているか（回復性）",
            "異なるブラウザやモバイル端末サイズでも、画面レイアウトが崩れずに表示されるか（移植性/ユーザビリティ）",
            "ソースコードの構造が複雑すぎず、将来的な機能追加や修正が容易であるか（保守性）"
        ],
        "answer": ["負荷に応じてリソースを追加した際、処理能力が線形に向上するか（スケールアウト性能）"]
    },
    "Q2-CLD-V2-02": { # Blue/Greenデプロイメント
        "options": [
            "画面の配色パターン（青と緑）をA/Bテストし、ユーザーのクリック率が高い方を自動採用できる",
            "新旧環境を瞬時に切り替え可能で、本番直前での確認と即時ロールバックが容易である",
            "本番環境と待機系の2面を持つため、インフラコストを恒久的に半減させることができる",
            "テスト工程を完全に省略し、開発者が書いたコードをレビューなしで直接本番環境に反映できる"
        ],
        "answer": ["新旧環境を瞬時に切り替え可能で、本番直前での確認と即時ロールバックが容易である"]
    },

    # ---------------------------
    # 第2章 医療 Vol.2 (ch2_medical_vol2.json)
    # ---------------------------
    "Q2-MED-V2-01": { # ユーザビリティテスト参加者
        "options": [
            "システムの内部仕様を熟知しており、迷わずスムーズな操作が可能な開発エンジニア",
            "実際のユーザー層（医師、看護師、患者）に近い属性を持ち、システムに慣れていない人",
            "医療機器規制（FDA等）の条文には詳しいが、機器の操作は未経験の法務・知財担当者",
            "購入の意思決定権を持つが、実際の操作は行わない病院の事務長や理事長"
        ],
        "answer": ["実際のユーザー層（医師、看護師、患者）に近い属性を持ち、システムに慣れていない人"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第4弾：問題データの修正を開始します...")

    for file_path in all_files:
        filename = os.path.basename(file_path)
        # スクリプトファイルなどは除外
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
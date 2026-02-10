import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第30弾・Vol.40-42 最終調整）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.40 (ch2_general_vol40.json)
    # ---------------------------
    "Q2-GEN-V40-01": { # 信頼度成長曲線が収束しない
        "options": [
            "開発チームの主張通り、バグが多く見つかるのはテストが優秀な証拠なので、そのままリリース可とする（楽観性バイアス）",
            "バグ発見数が収束していない（飽和していない）事実は、まだ同程度の潜在バグが残っている可能性を統計的に示唆している。したがって「品質が高い」という主張は誤りであり、追加テスト（期間延長）またはリスク受容の判断が必要である",
            "バグ修正によって新たなバグが埋め込まれる「デグレ（Regression）」が多発しており、開発プロセスの品質自体が劣化している可能性がある（Fix-one-Break-two現象）",
            "バグの総数は予め決まっているはずなので、もうすぐ収束すると楽観視する（ギャンブラーの誤謬）"
        ],
        "answer": ["バグ発見数が収束していない（飽和していない）事実は、まだ同程度の潜在バグが残っている可能性を統計的に示唆している。したがって「品質が高い」という主張は誤りであり、追加テスト（期間延長）またはリスク受容の判断が必要である"]
    },

    # ---------------------------
    # 第3章 AWS Vol.40 (ch3_aws_vol40.json)
    # ---------------------------
    "Q3-AWS-V40-01": { # Whole Team Qualityへの移行
        "options": [
            "品質ゲートを厳格化し、カバレッジ100%未満のコードは一切マージさせないルールを即時適用する（開発速度の急停止と反発を招く）",
            "Cさんに対し、いきなり開発者に要求するのではなく、まずはCさん自身がCIパイプラインに自動テストを組み込んで「自動化のメリット（手戻り減）」を実証し、開発者が楽になる環境を提供することで、徐々に開発者を巻き込む「信頼貯金」を作るよう指導する",
            "テストコードの作成をQAチームがすべて肩代わりし、開発者は機能実装に専念させる（QAのボトルネック化と品質責任の希薄化）",
            "スプリント期間を延ばして、手動テストの時間を確保する（アジリティの低下）"
        ],
        "answer": ["Cさんに対し、いきなり開発者に要求するのではなく、まずはCさん自身がCIパイプラインに自動テストを組み込んで「自動化のメリット（手戻り減）」を実証し、開発者が楽になる環境を提供することで、徐々に開発者を巻き込む「信頼貯金」を作るよう指導する"]
    },

    # ---------------------------
    # 第2章 医療 Vol.40 (ch2_medical_vol40.json)
    # ---------------------------
    "Q2-MED-V40-01": { # ログフォーマット変更の影響
        "options": [
            "ログ出力は「非機能要件」であるため、機能テストの対象外とし、リリース後のモニタリングで対応する（予防の放棄）",
            "変更自体は軽微だが、影響（誤診リスク）が重大であるため、ログ出力機能だけでなく、連携する解析システムを含めた「システム統合テスト」および「妥当性確認（Validation）」を実施し、安全性を証明する",
            "解析システムは他社製品なのでテスト範囲外とする（責任分界点の誤認）",
            "リスク受容してテストしない"
        ],
        "answer": ["変更自体は軽微だが、影響（誤診リスク）が重大であるため、ログ出力機能だけでなく、連携する解析システムを含めた「システム統合テスト」および「妥当性確認（Validation）」を実施し、安全性を証明する"]
    },

    # ---------------------------
    # 第2章 一般 Vol.41 (ch2_general_vol41.json)
    # ---------------------------
    "Q2-GEN-V41-01": { # レビューROI計算
        "options": [
            "20万円（これは投資コスト）",
            "30万円（正解：回避コスト50万 - 投資20万）",
            "50万円（これは総回避コスト）",
            "10万円（計算間違い）"
        ],
        "answer": ["30万円（正解：回避コスト50万 - 投資20万）"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第30弾：Vol.40-42 最終仕上げを開始します...")

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
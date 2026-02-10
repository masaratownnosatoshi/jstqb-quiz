import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第19弾・Vol.15-18 最終調整）
# ==========================================
fixes = {
    # ---------------------------
    # 第3章 一般 Vol.15 (ch3_general_vol15.json)
    # ---------------------------
    "Q3-GEN-V15-02": { # ツール分散戦略
        "options": [
            "ベンダーロックインの回避と、ツールの相互運用性の確保",
            "大量一括購入によるボリュームディスカウントを狙うため",
            "現場ごとに好きなツールをバラバラに導入し、データの統合を諦める",
            "ツールの機能重複を許容し、バックアップとして保持する"
        ],
        "answer": ["ベンダーロックインの回避と、ツールの相互運用性の確保"]
    },

    # ---------------------------
    # 第1章 一般 Vol.15 (ch1_general_vol15.json)
    # ---------------------------
    "Q1-GEN-V15-05": { # IDEALモデル診断フェーズ
        "options": [
            "改善計画の策定（Establishing）を先行して行う",
            "現状のベースラインを測定し、目標とのギャップを分析する",
            "改善活動を実行（Acting）し、その結果を評価する",
            "新しいプロセスを組織全体に展開（Deploying）する"
        ],
        "answer": ["現状のベースラインを測定し、目標とのギャップを分析する"]
    },

    # ---------------------------
    # 第2章 一般 Vol.15 (ch2_general_vol15.json)
    # ---------------------------
    "Q2-GEN-V15-01": { # ツール選定基準
        "options": [
            "初期導入コスト（ライセンス費）のみを比較して、最も安いものを選ぶ",
            "OSSを選択した場合の「サポート体制の欠如」や「学習コスト」、「将来の開発停止リスク」を評価し、商用ツールのライセンス費と比較する（TCO評価）",
            "「多機能であればあるほど良い」と考え、使わない機能が多いツールを選ぶ",
            "開発者の個人的な好みだけで選定し、保守性を考慮しない"
        ],
        "answer": ["OSSを選択した場合の「サポート体制の欠如」や「学習コスト」、「将来の開発停止リスク」を評価し、商用ツールのライセンス費と比較する（TCO評価）"]
    },
    "Q2-GEN-V15-02": { # 侵入型ツール
        "options": [
            "マルウェアのように振る舞い、システムの脆弱性を攻撃するツール",
            "テスト対象のコードや環境に介入（プローブ挿入など）して動作するため、実際の動作タイミングやパフォーマンスに影響を与える可能性があるツール（プローブ効果）",
            "ファイアウォールを突破して外部からアクセスするツール",
            "インストール不要で、USBメモリから起動できるポータブルツール"
        ],
        "answer": ["テスト対象のコードや環境に介入（プローブ挿入など）して動作するため、実際の動作タイミングやパフォーマンスに影響を与える可能性があるツール（プローブ効果）"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第19弾：最終調整を開始します...")

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
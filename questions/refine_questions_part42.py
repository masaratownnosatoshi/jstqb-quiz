import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第39弾・Vol.70_2 追加仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第1章 AWS Vol.70_2 (ch1_aws_vol70_2.json)
    # ---------------------------
    "Q1-AWS-V70-2-01": { # コスト計算修正
        "options": [
            "$720",
            "$1,440",
            "$2,160",
            "$7,200"
        ],
        "answer": ["$720"],
        "explanation": "【解説】\n総稼働時間 = 10台 × 24時間 × 30日 = 7,200時間。\n総コスト = 7,200時間 × $0.1 = $720。\n※スポットインスタンスやReserved Instancesを使えばさらに安くなりますが、オンデマンド定価計算ではこの通りです。"
    },
    "Q1-AWS-V70-2-03": { # 負荷テストツール
        "options": [
            "開発者PCなどの単一クライアントから手動でアクセスする（負荷が足りず、クライアント側がボトルネックになる）", # 「F5連打」を修正
            "AWS FIS (Fault Injection Simulator) やストレスツール（Stress-ng等）を使用して、CPU負荷を人為的に発生させる",
            "サーバーを再起動する",
            "LANケーブルを抜く"
        ],
        "answer": ["AWS FIS (Fault Injection Simulator) やストレスツール（Stress-ng等）を使用して、CPU負荷を人為的に発生させる"]
    },

    # ---------------------------
    # 第2章 金融 Vol.70_2 (ch2_finance_vol70_2.json)
    # ---------------------------
    "Q2-FIN-V70-2-02": { # 勘定系ボトルネック
        "options": [
            "ディスク容量",
            "スロークエリログとロック待ち状況（Deadlock）",
            "ネットワーク帯域",
            "クライアント側のネットワークレイテンシ（DB内部のCPU高騰原因としては関連が薄い）" # 「室温」を修正
        ],
        "answer": ["スロークエリログとロック待ち状況（Deadlock）"]
    },

    # ---------------------------
    # 第1章 医療 Vol.70_2 (ch1_medical_vol70_2.json)
    # ---------------------------
    "Q1-MED-V70-2-02": { # SOUP採用
        "options": [
            "そのまま使う",
            "SOUPとして登録し、既知のバグを調査し、ラッパーコード等で入出力を検証・隔離する追加テストを行う",
            "OSS作者に電話する",
            "十分なエビデンスなしに『使用実績あり（Proven in Use）』として扱い、追加検証を省略する（過信のリスク）" # 「偽る」を修正
        ],
        "answer": ["SOUPとして登録し、既知のバグを調査し、ラッパーコード等で入出力を検証・隔離する追加テストを行う"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第39弾：Vol.70_2の追加修正を開始します...")

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
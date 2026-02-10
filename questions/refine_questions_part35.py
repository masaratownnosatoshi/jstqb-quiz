import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第35弾・Vol.57-59 最終仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.57 (ch2_general_vol57.json)
    # ---------------------------
    "Q2-GEN-V57-01": { # プロセス改善の意義
        "options": [
            "プロセスを標準化すること自体を目的にしてしまい、プロジェクトの文脈（Context）を無視した『重すぎるプロセス』を強制する（目的の形骸化）", # 「見栄え」を修正
            "テストプロセスの品質はソフトウェア自体の品質に影響するため、プロセス改善により製品品質が向上し、保守リソースの削減や顧客満足度の向上につながる",
            "開発プロセスとは無関係に、テストチームだけで独立して改善できるため",
            "成熟度モデルの最高レベル（Level 5）を取得すること自体をゴールとし、費用対効果を無視する（バニティ・メトリクス）" # 「流行り」を修正
        ],
        "answer": ["テストプロセスの品質はソフトウェア自体の品質に影響するため、プロセス改善により製品品質が向上し、保守リソースの削減や顧客満足度の向上につながる"]
    },

    # ---------------------------
    # 第2章 一般 Vol.59 (ch2_general_vol59.json)
    # ---------------------------
    "Q2-GEN-V59-01": { # カスタムツールリスク
        "options": [
            "「ライセンス費が無料」であることだけに注目し、開発・保守にかかる人件費（隠れたコスト）を過小評価すること", # 「初期コスト」を具体化
            "ツール作成者がプロジェクトを離れた場合にメンテナンスが困難になるリスクや、文書化不足による属人化",
            "機能が多すぎて使いこなせないこと",
            "オープンソース（OSS）のライセンス条項に違反すること（GPL汚染など）" # 「サポート手厚すぎ」を修正
        ],
        "answer": ["ツール作成者がプロジェクトを離れた場合にメンテナンスが困難になるリスクや、文書化不足による属人化"]
    },

    # ---------------------------
    # 第3章 一般 Vol.58 (ch3_general_vol58.json)
    # ---------------------------
    "Q3-GEN-V58-02": { # モチベーション阻害
        "options": [
            "テスト担当者の貢献（品質向上への寄与）を認識し、公平かつ誠実に評価する",
            "納期を守るために品質を犠牲にしてリリースし、テストチームには何も伝えない",
            "テスト担当者をプロジェクトの意思決定から遠ざけ、単なる『実行要員』として扱う（疎外感）", # 「情報を隠す」を修正
            "個人のミスを全員の前で厳しく追及する"
        ],
        "answer": ["テスト担当者の貢献（品質向上への寄与）を認識し、公平かつ誠実に評価する"],
        # 注: 問題文が「維持・向上させるための...」なので、正解は肯定的である必要があります。
        # 上記修正は「誤答（やってはいけないこと）」のバリエーションを増やしました。
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第35弾：Vol.57-59の最終修正を開始します...")

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
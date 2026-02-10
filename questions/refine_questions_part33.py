import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第33弾・Vol.51-52 追加ブラッシュアップ）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.52 (ch2_general_vol52.json)
    # ---------------------------
    "Q2-GEN-V52-03": { # 静的解析運用の改善
        "options": [
            "警告を全て無視するようルール化する",
            "「新規コード（差分）」のみをチェック対象とし、既存コードの警告はベースラインとして許容する（ラットチェット方式）。また、プロジェクトに不要なルールを無効化してノイズを減らす",
            "ツールの設定を最も厳格にし、全ての警告を「エラー」として扱い、修正されるまでビルドを失敗させる（過剰な厳格化により開発速度が停止するリスク）", # 「帰るな」を修正
            "静的解析ツールを削除する"
        ],
        "answer": ["「新規コード（差分）」のみをチェック対象とし、既存コードの警告はベースラインとして許容する（ラットチェット方式）。また、プロジェクトに不要なルールを無効化してノイズを減らす"]
    },

    # ---------------------------
    # 第3章 一般 Vol.52 (ch3_general_vol52.json)
    # ---------------------------
    "Q3-GEN-V52-01": { # 折衝役の採用基準
        "options": [
            "候補A。技術力が高ければ、相手を論破してこちらの要求を通せるため（強引な交渉のリスク）", # 「技術があれば周りは黙る」を修正
            "候補B。折衝役には「ソフトスキル（コミュニケーション、交渉力）」が最重要であり、技術不足は学習やチームで補えるが、性格的な資質は変えにくいため",
            "どちらも不採用とし、技術と人格の両方を兼ね備えた完璧な人材が現れるまでポジションを空けておく（機会損失）", # 「どちらも不採用」を具体化
            "技術力はテストに関係ないため、性格だけで決める" # 「くじ引き」を修正
        ],
        "answer": ["候補B。折衝役には「ソフトスキル（コミュニケーション、交渉力）」が最重要であり、技術不足は学習やチームで補えるが、性格的な資質は変えにくいため"]
    },

    # ---------------------------
    # 第3章 クラウド Vol.51 (ch3_cloud_vol51.json)
    # ---------------------------
    "Q3-CLD-V51-01": { # シフトレフトの意味
        "options": [
            "テスト工程を左（開発初期）に移動させ、早期に品質を作り込むこと",
            "テスト工程を右（リリース後）に移動させ、本番環境での監視を強化すること（シフトライトとの混同）",
            "開発者がテストチームに異動すること",
            "テスト自動化ツールを導入すること" # 「左手でキーボード」を修正
        ],
        "answer": ["テスト工程を左（開発初期）に移動させ、早期に品質を作り込むこと"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第33弾：Vol.51-52の追加修正を開始します...")

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
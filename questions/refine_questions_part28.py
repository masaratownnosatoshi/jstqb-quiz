import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第28弾・Vol.10-19 補完）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.10 (ch2_general_vol10.json)
    # ---------------------------
    "Q2-GEN-V10-02": { # 静的解析の警告対応
        "options": [
            "警告が出なくなるまでツール設定を緩和し続ける",
            "ツールのデフォルト設定をそのまま使い、全ての警告（Warning）をビルドエラー（Error）として扱い、修正を強制する（過剰な厳格化）",
            "誤検知（False Positive）を含め、すべての警告を無視するようチームに指示する",
            "警告レベルを全て「情報（Info）」に下げて、開発者の目に触れないようにする（臭いものに蓋）"
        ],
        "answer": [
            "ツールのデフォルト設定をそのまま使い、全ての警告（Warning）をビルドエラー（Error）として扱い、修正を強制する（過剰な厳格化）"
        ],
        "explanation": "【解説】\n文脈によりますが、初期導入時に「全修正強制」を行うと開発速度が停止し、チームの反発を招きます。段階的な適用や、プロジェクトに合わせたルールのチューニングが正解（アンチパターンの逆）です。"
    },

    # ---------------------------
    # 第2章 AWS Vol.15 (ch2_aws_vol15.json)
    # ---------------------------
    "Q2-AWS-V15-01": { # DBテストデータ管理
        "options": [
            "手動でデータを戻すSQLを書く（メンテナンスコスト高）",
            "テスト実行前にRDSの「スナップショット」を取得し、テスト終了後（または再実行前）にスナップショットから復元する",
            "IaC（Terraform等）でDBを毎回作り直すが、データ投入の仕組みがないため空のDBでテストする（テストにならない）",
            "本番DBをそのままテスト環境にコピーして使う（セキュリティリスク）"
        ],
        "answer": ["テスト実行前にRDSの「スナップショット」を取得し、テスト終了後（または再実行前）にスナップショットから復元する"]
    }
}

# ==========================================
# セーフティネット（キーワード置換）
# ==========================================
# 過去のファイルにまだ残っているかもしれない「低品質な選択肢」を
# 再度チェックして置換します。
bad_patterns = {
    "開発者を怒鳴る": "開発者に責任を押し付け、修正を強要する（根本解決にならない）",
    "見て見ぬふり": "リスクを受容したという記録を残さずに放置する（黙認）",
    "給料を下げる": "個人の評価を下げることでペナルティを与える",
    "気合": "精神論で乗り切ろうとする"
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第28弾：補完修正を開始します...")

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
                
                # 1. 特定IDの修正
                if q_id in fixes:
                    fix_data = fixes[q_id]
                    if "options" in fix_data:
                        q["options"] = fix_data["options"]
                    if "answer" in fix_data:
                        q["answer"] = fix_data["answer"]
                    if "explanation" in fix_data:
                        q["explanation"] = fix_data["explanation"]
                    print(f"  修正適用 (ID指定): {q_id}")
                    file_modified = True

                # 2. セーフティネット（キーワード置換）
                if "options" in q:
                    new_options = []
                    options_changed = False
                    for opt in q["options"]:
                        replaced = False
                        for bad_word, better_phrase in bad_patterns.items():
                            if bad_word in opt and better_phrase not in opt:
                                new_options.append(better_phrase)
                                print(f"  自動修正 (キーワード '{bad_word}'): {q_id}")
                                replaced = True
                                options_changed = True
                                break
                        if not replaced:
                            new_options.append(opt)
                    
                    if options_changed:
                        q["options"] = new_options
                        file_modified = True

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                updated_count += 1
                
        except Exception as e:
            print(f"  読み込みエラー: {filename} - {e}")

    print("-" * 30)
    print(f"完了: 合計 {updated_count} ファイルを確認・修正しました。")

if __name__ == "__main__":
    refine_questions()
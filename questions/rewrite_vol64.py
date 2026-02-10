import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."
TARGET_FILE = "ch1_general_vol64.json"

# 新しい正しいデータ
# 開発者が「仕様だ」と言い張る場合の正しい対応（エスカレーション）を正解にします
new_content = [
    {
        "id": "Q1-GEN-V64-03",
        "chapter": "第1章",
        "level": "K3",
        "category": "一般",
        "style": "シナリオ",
        "type": "単一選択",
        "question": "【適用】インシデント管理。\nテスト実行中にバグと思われる挙動を発見したが、開発者が「それは仕様だ」と言い張り、修正を拒否している。\nテスト担当者として取るべき適切な行動はどれか。",
        "options": [
            "仕様書や要件定義書を確認し、記載があいまいな場合はプロダクトオーナーやステークホルダーにエスカレーションして判断を仰ぐ",
            "開発者が仕様だと言うのであれば、その判断を全面的に信頼し、バグ票を取り下げてテスト合格とする",
            "開発者が修正に応じるまで、その機能をテスト対象から除外し、進捗報告でも触れないようにする",
            "見つかったバグを報告せずに隠蔽する"
        ],
        "answer": [
            "仕様書や要件定義書を確認し、記載があいまいな場合はプロダクトオーナーやステークホルダーにエスカレーションして判断を仰ぐ"
        ],
        "explanation": "【解説】\n開発者と意見が対立した場合、個人の判断で処理したり（隠蔽・鵜呑み）、感情的に対立したりするのは不適切です。仕様書という「正解」を確認し、それでも不明な場合は決定権者（POなど）に判断を仰ぐ（エスカレーション）のがプロフェッショナルな対応です。",
        "tags": ["第1章", "一般", "シナリオ", "K3"]
    }
]

def rewrite_vol64():
    file_path = os.path.join(OUTPUT_DIR, TARGET_FILE)
    
    print(f"--- {TARGET_FILE} の再構築を開始 ---")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(new_content, f, ensure_ascii=False, indent=2)
        print(f"成功: {TARGET_FILE} を正しい問題内容で上書きしました。")
        print("  (正解を「隠蔽する」から「エスカレーションする」に修正済み)")

    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    rewrite_vol64()
    input("\nエンターキーを押して終了してください...")
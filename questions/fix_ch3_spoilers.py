import json
import os
import glob

OUTPUT_DIR = "."

# 修正対象のリスト
# search_text: 問題文の一部（検索用）
# new_options: 修正後のきれいな選択肢
# answer: 正解の選択肢（念のため指定）
UPDATES = [
    {
        "search_text": "テストプロセス改善（TPI Next）の優先順位付け",
        "new_options": [
            "テスト戦略（Strategy）とテスト方法論（Methodology）を定義し、プロジェクト全体で「どのようにテストするか」の共通認識と標準を作る",
            "テスト担当者のスキル評価を行い、スキルの低いメンバーをプロジェクトから外す",
            "詳細なテストケース管理ツールを購入し、すべてのテストケースを細かく記録することを義務付ける",
            "テスト自動化ツールを導入し、手動テストを全て廃止して効率化を図る"
        ],
        "answer": [
            "テスト戦略（Strategy）とテスト方法論（Methodology）を定義し、プロジェクト全体で「どのようにテストするか」の共通認識と標準を作る"
        ]
    },
    {
        "search_text": "テストチームのコンフリクト解消",
        "new_options": [
            "テスターの主張を支持し、開発者に対して「品質第一」のスローガンを掲げさせ、全てのバグを修正するまでリリースを許可しない権限を行使する",
            "「バグトリアージ会議」を定期開催し、ビジネスリスクやユーザー影響度に基づく共通の優先順位付け基準（Severity vs Priority）を策定・合意して運用する",
            "開発者の主張を受け入れ、テスターに対しては「これからは軽微なバグは報告しなくてよい」と指示し、バグ報告の基準を引き上げる",
            "両チームのリーダーを交代させ、新しいリーダー同士でゼロから関係構築をやり直させる"
        ],
        "answer": [
            "「バグトリアージ会議」を定期開催し、ビジネスリスクやユーザー影響度に基づく共通の優先順位付け基準（Severity vs Priority）を策定・合意して運用する"
        ]
    },
    {
        "search_text": "インスペクション（公式レビュー）におけるモデレーターの役割",
        "new_options": [
            "モデレーター自身の技術的見解を述べてどちらが正しいかをその場で裁定し、強引に結論を出して会議を終わらせる",
            "技術的な議論こそがレビューの価値を高めるため、時間の許す限りその場で徹底的に議論させ、全員が納得する解決策が出るまで見守る",
            "議論が長引き会議の進行を妨げているため、その指摘を「課題（Open Issue）」として記録し、会議の場では解決策を決めずに次の指摘に進むよう誘導する",
            "欠陥を指摘したレビューアに対して「代替案がないなら批判するな」と注意し、対案が出せない指摘は却下して議事録から削除する"
        ],
        "answer": [
            "議論が長引き会議の進行を妨げているため、その指摘を「課題（Open Issue）」として記録し、会議の場では解決策を決めずに次の指摘に進むよう誘導する"
        ]
    },
    {
        "search_text": "テストプロセス成熟度診断（アセスメント）",
        "new_options": [
            "過去のプロジェクトのバグ摘出数とテスト工数のデータだけを統計分析し、数値が良いプロジェクトを「成熟度が高い」と機械的に判定する",
            "外部の有名コンサルタントを呼び、現場を見ずにマネージャの話だけを聞いて、業界平均と比較したレポートを作成してもらう",
            "アセッサー（評価者）が主要なステークホルダーにインタビューを行い、実際の成果物（テスト計画書や報告書）を査読して、モデルの基準と照らし合わせて証拠ベースで判定する",
            "全テスト担当者にWebアンケートを一斉配信し、自己評価スコア（1〜5点）の平均値を算出して、それを組織の成熟度レベルと認定する"
        ],
        "answer": [
            "アセッサー（評価者）が主要なステークホルダーにインタビューを行い、実際の成果物（テスト計画書や報告書）を査読して、モデルの基準と照らし合わせて証拠ベースで判定する"
        ]
    }
]

def fix_ch3_spoilers():
    print("--- 第3章の選択肢修正を開始します ---")
    
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
    modified_files = set()

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_changed = False
            
            if isinstance(data, list):
                for q in data:
                    q_text = q.get("question", "")
                    
                    # 各修正対象についてチェック
                    for update in UPDATES:
                        if update["search_text"] in q_text:
                            # 選択肢と正解を上書き
                            q["options"] = update["new_options"]
                            q["answer"] = update["answer"]
                            
                            file_changed = True
                            print(f"修正: {os.path.basename(file_path)} -> 「{update['search_text'][:15]}...」")

            if file_changed:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                modified_files.add(os.path.basename(file_path))

        except Exception as e:
            print(f"エラー: {os.path.basename(file_path)} ({e})")

    if modified_files:
        print("-" * 30)
        print(f"✅ 修正完了！ 合計 {len(modified_files)} ファイルを更新しました。")
    else:
        print("⚠️ 修正対象の問題が見つかりませんでした。すでに修正済みかもしれません。")

if __name__ == "__main__":
    fix_ch3_spoilers()
    input("エンターキーを押して終了...")
import json
import os

# 保存先ディレクトリ
OUTPUT_DIR = "."

# 修正内容の定義（不自然な選択肢を、もっともらしい誤答に差し替えます）
fixes = {
    # 1. Page Object Pattern (Vol.19)
    "ch1_general_vol19.json": {
        "options": [
            "「ページオブジェクトパターン（Page Object Pattern）」を導入し、画面要素の定義（セレクタ）をページごとのクラスに集約・隠蔽する。テストシナリオからはそのクラスのメソッドを呼ぶだけにすることで、画面変更の影響をクラス内部に閉じ込める",
            "画面上のすべての要素定義をテストシナリオファイルの中に直接記述し、変更時は全ファイルを検索置換（Grep Replace）で対応する", # 修正
            "UIテストは壊れやすいので全て廃止し、手動テストのみに戻す",
            "要素特定に「絶対パス（Absolute XPath）」を使用し、要素の場所を厳密に指定する"
        ]
    },
    # 2. 自動化デザインパターン (Vol.14)
    "ch2_general_vol14.json": {
        "options": [
            "Page Object Model (POM) パターンを導入し、画面要素の定義（セレクタ）をページごとのクラスに隠蔽・集約する",
            "テストケースごとに専用の関数を毎回作成し、再利用性は考慮せずにコピー＆ペーストで量産する", # 修正
            "テストコード内にIDを直書きする",
            "画像認識でテストする"
        ]
    },
    # 3. データ駆動 vs キーワード駆動 (Vol.95)
    "ch2_general_vol95.json": {
        "options": [
            "データ駆動は「入力値と期待値」を外部ファイルに分離する手法であり、キーワード駆動は「操作（アクション）」をキーワードとして定義し、スクリプトから詳細な手順を隠蔽する手法である",
            "データ駆動は「単体テスト」専用の手法であり、キーワード駆動は「システムテスト」専用の手法であるという違いがある", # 修正
            "両者は同じ意味である",
            "データ駆動は手動テスト用、キーワード駆動は自動テスト用である"
        ]
    },
    # 4. 心理的安全性 (Vol.11)
    "ch3_general_vol11.json": {
        "options": [
            "心理的安全性が損なわれ、バグ隠蔽のリスクが高まっている。A氏に対し「態度の改善」を業務命令として伝え、チームの行動規範（Code of Conduct）を再定義して「敬意」を必須項目とする",
            "A氏はスキルが高く替えが効かないため、個人の性格の問題として黙認する",
            "A氏とB氏を物理的に隔離し、チャットツールのみで会話させるようにする", # 修正（マネージャの対策として不適切だが選択肢として成立する）
            "B氏のスキル不足が原因であると判断し、B氏に追加のトレーニングを課す"
        ]
    }
}

def fix_nonsense_options():
    print("--- 不自然な選択肢の修正を開始 ---")
    
    count = 0
    for filename, new_content in fixes.items():
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(file_path):
            print(f"スキップ（ファイルなし）: {filename}")
            continue

        try:
            # 読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 修正適用
            if isinstance(data, list):
                for q in data:
                    # 選択肢を差し替え
                    if "options" in new_content:
                        q["options"] = new_content["options"]
                        # ※正解データは変更不要（正しい選択肢は元のままであるため）
            
            # 保存
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"修正完了: {filename}")
            count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"完了: {count} ファイルの選択肢を適正化しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_nonsense_options()
    input()
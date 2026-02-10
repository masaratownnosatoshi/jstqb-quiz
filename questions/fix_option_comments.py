import json
import os
import glob

OUTPUT_DIR = "."

# 修正対象の定義
# search_key: 問題文の一部（ユニークなもの）
# new_options: 修正後のきれいな選択肢リスト
fixes = [
    {
        # 問題1: テストチームのサイロ化
        "search_key": "「開発チーム」と「テストチーム」が完全に分断されており",
        "new_options": [
            "テストチームを解散して全員を開発チームに吸収合併し、開発者が自分でテストも行う「フルスタックエンジニア」体制に一気に移行する",
            "「シフトレフト」を推進し、要件定義や設計レビューの段階からテスターが参加して、テスト容易性の観点からフィードバックを行う活動を定着させる",
            "テストチームの権限を強化し、品質基準を満たさない成果物を受け取った場合は、開発チームのマネージャに対して正式な抗議文を送付するプロセスを確立する",
            "開発チームとの交流を深めるために、週に一度のランチ会を義務付け、業務以外の話題で盛り上がることで心理的な壁を取り払う"
        ]
    },
    {
        # 問題2: Flakyテスト対策
        "search_key": "自動テスト実行時に「成功したり失敗したりする（不安定な）」",
        "new_options": [
            "不安定なテストは維持管理コストに見合わないため即座に削除し、その機能については今後一切テストを行わないことにする",
            "不安定なテストケースには「リトライ機能（自動再実行）」を実装し、3回実行して1回でも成功すれば合格とみなすことで、見かけ上のエラーを減らす",
            "失敗した時のスクリーンショットやログを詳細に記録する仕組みを導入した上で、不安定なテストを「隔離（Quarantine）」し、原因（タイミング依存、データ残留など）を特定して修正するまでメインのパイプラインからは外す",
            "テスト環境のサーバースペックを最高レベルに引き上げ、処理速度を向上させることで、タイミング問題による失敗を力技でねじ伏せる"
        ]
    }
]

def fix_option_comments():
    print("--- 選択肢内の余分な注釈（カッコ書き）の削除を開始 ---")
    
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
    fixed_count = 0

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        file_modified = False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    q_text = q.get("question", "")
                    
                    for fix in fixes:
                        if fix["search_key"] in q_text:
                            print(f"発見: {filename} (ID: {q.get('id')})")
                            # 選択肢を差し替え
                            q["options"] = fix["new_options"]
                            file_modified = True
                            print("  => 選択肢を修正しました。")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                fixed_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"完了: {fixed_count} ファイルを修正しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_option_comments()
    input()
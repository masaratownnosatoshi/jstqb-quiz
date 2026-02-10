import json
import os
import glob

# index.json のパス（必要に応じて変更してください）
INDEX_FILE = "index.json"

# 追加対象のファイルパターン（Vol.96 ～ Vol.99）
TARGET_PATTERNS = [
    "*_vol96.json",
    "*_vol97.json",
    "*_vol98.json",
    "*_vol99.json"
]

def update_index():
    # 1. index.json を読み込む
    if not os.path.exists(INDEX_FILE):
        print(f"エラー: {INDEX_FILE} が見つかりません。")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    # 既存のパスリストを作成（重複登録防止用）
    existing_paths = {item.get("path") for item in index_data.get("chunks", [])}
    
    new_chunks = []
    
    # 2. 対象ファイルを検索して情報を抽出
    for pattern in TARGET_PATTERNS:
        files = glob.glob(pattern)
        for file_path in files:
            # アプリの仕様に合わせてパスを調整 (例: "./filename" -> "questions/filename")
            # ここではindex.jsonの仕様に合わせて "questions/" フォルダにある前提のパスにします
            # ※ 実際のファイル移動は手動で行ってください
            registered_path = f"questions/{file_path}"
            
            # 既に登録済みならスキップ
            if registered_path in existing_paths:
                print(f"スキップ（登録済）: {file_path}")
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as qf:
                    questions = json.load(qf)
                    
                    if not questions:
                        continue

                    # 最初の問題からメタデータを取得
                    first_q = questions[0]
                    q_count = len(questions)
                    
                    new_entry = {
                        "path": registered_path,
                        "chapter": first_q.get("chapter", "不明"),
                        "category": first_q.get("category", "不明"),
                        "klevel": first_q.get("level", "K2"), # levelキーをklevelとして登録
                        "qCount": q_count
                    }
                    
                    new_chunks.append(new_entry)
                    index_data["chunks"].append(new_entry)
                    print(f"追加: {file_path} ({q_count}問)")

            except Exception as e:
                print(f"エラー（{file_path}）: {e}")

    # 3. index.json を保存
    if new_chunks:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        print("-" * 30)
        print(f"完了: 合計 {len(new_chunks)} ファイルを index.json に追加しました。")
        print("※ 注意: 生成されたjsonファイル自体を 'questions' フォルダ（またはアプリが参照するフォルダ）に移動するのを忘れないでください。")
    else:
        print("追加対象の新しいファイルが見つからないか、すべて登録済みです。")

if __name__ == "__main__":
    update_index()
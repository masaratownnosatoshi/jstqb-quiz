import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."

# 修正対象のデータ定義
FIX_TARGETS = {
    "【分析】欠陥の偏在（クラスタリング）への対処。": {
        "options": [
            "バグが多いのは仕様が複雑だからであり、これ以上の品質向上は望めないため、現状のままリリースし、運用での回避策マニュアルを整備する",
            "このモジュールにさらに多くのテスターを投入し、バグを出し切るまで徹底的にブラックボックステストを繰り返す",
            "他のモジュールのテスト時間を削って在庫管理モジュールに充てることで、全体の工数を変えずに重点テストを行う",
            "品質が安定するまでリリースを延期し、開発チームに対して当該モジュールのリファクタリング（設計見直しとコード整理）と、単体テストの拡充を強く要求する"
        ],
        "answer": [
            "品質が安定するまでリリースを延期し、開発チームに対して当該モジュールのリファクタリング（設計見直しとコード整理）と、単体テストの拡充を強く要求する"
        ]
    }
}

def fix_clustering_question():
    print("--- 「欠陥の偏在」問題の修正を開始します ---")
    
    json_files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
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
                    
                    # ターゲットの問題文が含まれているか確認
                    for target_key, correct_data in FIX_TARGETS.items():
                        if target_key in q_text:
                            # 修正実行
                            q["options"] = correct_data["options"]
                            q["answer"] = correct_data["answer"]
                            file_modified = True
                            print(f"修正しました: {filename}")
                            print(f"  ID: {q.get('id')}")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                fixed_count += 1

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"完了: {fixed_count} ファイルを修正しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_clustering_question()
    input()
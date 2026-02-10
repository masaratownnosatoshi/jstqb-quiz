import json
import os

# 先ほどの「強制再生成」で触ったファイルリスト（＝壊れている可能性が高い）
SUSPECT_FILES = [
    "ch1_aws_vol3.json",
    "ch1_finance_vol10.json",
    "ch1_general_vol19.json",
    "ch1_general_vol64.json", # これは先ほど手動修正済みですが念のため
    "ch1_general_vol76.json",
    "ch1_general_vol8.json",
    "ch1_general_vol81.json",
    "ch2_finance.json",
    "ch2_general_vol14.json",
    "ch2_general_vol22.json",
    "ch2_general_vol71.json",
    "ch2_general_vol72.json",
    "ch2_general_vol82.json",
    "ch2_general_vol84.json",
    "ch2_general_vol95.json",
    "ch3_cloud_vol7.json",
    "ch3_general_vol11.json",
    "ch3_general_vol15.json"
]

def inspect_suspects():
    print("--- 破損疑いファイルの中身確認 ---")
    
    for filename in SUSPECT_FILES:
        file_path = os.path.join(".", filename)
        
        if not os.path.exists(file_path):
            print(f"\n[ファイルなし] {filename}")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for q in data:
                    print(f"\n■ ファイル名: {filename}")
                    print(f"  ID: {q.get('id')}")
                    print(f"  問題文: {q.get('question')[:50]}...") # 長いので先頭だけ
                    print("  選択肢:")
                    for i, opt in enumerate(q.get("options", [])):
                        print(f"    {i+1}. {opt}")
                    print(f"  ★設定されている正解: {q.get('answer')}")
                    
                    # 簡易チェック: 正解が選択肢に含まれているか
                    if q.get('answer') and q.get('answer')[0] not in q.get('options', []):
                        print("  【警告】正解テキストが選択肢の中にありません！")
                    else:
                        print("  (データ構造は正常)")

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("\n" + "="*30)
    print("確認終了。エンターキーを押して終了してください...")

if __name__ == "__main__":
    inspect_suspects()
    input()
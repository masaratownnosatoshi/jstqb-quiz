import json
import os
import glob

OUTPUT_DIR = "."

# 検索キーワード
SEARCH_KEYWORDS = ["A社開発のAndroid", "1.125TB", "4つ選べ"]

# 正しい選択肢（変更なし）
# A: セキュリティ, B: エクスポート, C: 1.125TB, D: 1台のみ, E: コーデック, F: 全て同期
# ここでは既存の選択肢をそのまま使い、正解リストだけを確実に指定します。

# 正しい正解リスト（3つ）
NEW_ANSWER = [
    "テスト戦略に遡り、追加機能実装前では実施していなかった「セキュリティテスト」を加え、関連するテスト条件を作成する",
    "「エクスポートした環境設定ファイルが正しくインポートできるか」を確認するためのテスト条件を作成する",
    "「対応している全てのコーデックの動画ファイルが正しく読み込みできるか」を確認するためのテスト条件を作成する"
]

def fix_test_manager_k4():
    print("--- テストマネージャ問題（K4）の修正を開始 ---")
    
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "*.json"))
    found = False

    for file_path in json_files:
        if "index.json" in file_path:
            continue
            
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_modified = False
            
            if isinstance(data, list):
                for q in data:
                    q_text = q.get("question", "")
                    
                    # 問題文の一致確認（"4つ選べ"が含まれているか）
                    if "1.125TB" in q_text and "4つ選べ" in q_text:
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # 1. 問題文を「3つ選べ」に修正
                        q["question"] = q_text.replace("最も適切なものを4つ選べ", "最も適切なものを3つ選べ")
                        
                        # 2. 正解を再設定（A, B, E）
                        q["answer"] = NEW_ANSWER
                        
                        # 3. 解説の記号ズレを修正
                        q["explanation"] = "【解説】\n・一貫性（整合性）：顧客の懸念事項（セキュリティ不安）に対し、戦略レベルでテストを追加する (A) ことがリスク対応として適切です。\n・完全性（網羅性）：追加された機能要件である「設定のエクスポート (B)」や「新コーデック (E)」について確認する条件作成が必要です。\n\n※ (D) は市場の断片化（機種依存）を無視しており不適切です。\n※ (C) の「1.125TB」はテスト条件としては粒度が細かすぎ（テストケースレベル）、(F) の「撮影データ全て」は全量テストとなり現実的ではありません。"
                        
                        file_modified = True
                        found = True
                        print("  => 問題文を「3つ選べ」に修正し、解説の記号ズレを直しました。")

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"保存完了: {filename}")
                break

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    if not found:
        print("警告: 該当する問題が見つかりませんでした。")

    print("-" * 30)
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_test_manager_k4()
    input()
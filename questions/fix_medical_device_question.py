import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."

# 検索キー（問題文の一部）
SEARCH_KEY = "医療機器メーカーA社から依頼を受けて"

# 新しい選択肢データ（解説と整合するように作成）
# A: 規格準拠のみ（極端すぎる）
# B: 対処的・方法論的のみ（バグ発見偏重）
# C: コンサルテーションベース（解説で否定されている受入テスト寄り）
# D: 正解（分析・モデル・規格・回帰の組み合わせ）
NEW_OPTIONS = [
    "(4) プロセス準拠または規格準拠戦略のみを採用し、FDA承認の取得に特化して、他のテスト工数は最小限に抑える",
    "バグの改修中であることを考慮し、(5) 対処的戦略（欠陥ベース）と (3) 方法論的戦略を重視して、バグの洗い出しに集中する",
    "実際の医療現場での使い勝手を最優先するため、(6) コンサルテーションベースの戦略（ユーザ主導）と (2) モデルベースド戦略を採用する",
    "人命リスクと法規制に対応するため (1) 分析的戦略と (4) 規格準拠戦略を核とし、治療シーケンス検証のための (2) モデルベースド戦略、および改修に伴う (7) 回帰的テスト戦略を組み合わせる"
]

NEW_ANSWER = [
    "人命リスクと法規制に対応するため (1) 分析的戦略と (4) 規格準拠戦略を核とし、治療シーケンス検証のための (2) モデルベースド戦略、および改修に伴う (7) 回帰的テスト戦略を組み合わせる"
]

def fix_medical_device_question():
    print("--- 医療機器テスト計画問題の選択肢修正を開始 ---")
    
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
                    
                    # 該当の問題を発見
                    if SEARCH_KEY in q_text:
                        print(f"発見: {filename} (ID: {q.get('id')})")
                        
                        # 選択肢と正解を更新
                        q["options"] = NEW_OPTIONS
                        q["answer"] = NEW_ANSWER
                        
                        file_modified = True
                        print("  => 空だった選択肢を適切な内容に復元しました。")

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
    fix_medical_device_question()
    input()
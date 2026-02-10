import json
import os
import glob

# カレントディレクトリを対象
TARGET_DIR = "."

# 修正対象のデータ定義（問題文の冒頭でマッチングし、正しいデータを注入する）
FIX_TARGETS = {
    # 1問目: IDEALモデル
    "【適用】テストプロセス改善における「IDEALモデル」。": {
        "options": [
            "直ちに新しいプロセスを全社一斉に展開し、すべてのプロジェクトに対して新しいルールの遵守を強制する",
            "プロセスの改善は現場の自主性に任せることとし、マネジメント層は一切関与せず、報告だけを待つことにする",
            "診断結果に基づき、具体的な改善計画を作成し、パイロットプロジェクトの選定や改善チームの結成を行って、実行の準備を整える",
            "診断結果が悪かったプロジェクトの責任者を処分し、新しいマネージャを外部から登用して体制を刷新する"
        ],
        "answer": [
            "診断結果に基づき、具体的な改善計画を作成し、パイロットプロジェクトの選定や改善チームの結成を行って、実行の準備を整える"
        ]
    },
    # 2問目: ナレッジマネジメント
    "【適用】テストチームのナレッジマネジメント。": {
        "options": [
            "Aさんに対して、業務知識を全てドキュメント化するまでテスト実務を禁止する業務命令を出し、マニュアル作成に専念させる",
            "Aさんの知識は属人的な才能であり移転不可能であるため、Aさんが引退するまでにAIに学習させて代替させる計画を立てる",
            "Aさんの給与を上げて離職を防ぐとともに、Aさん専任のアシスタントをつけて、Aさんの負担を減らす",
            "Aさんに「ペアテスト」や「モブテスト」のファシリテーターを依頼し、実際のテスト活動を通じて他のメンバーに思考プロセスや観点を共有・伝承させる"
        ],
        "answer": [
            "Aさんに「ペアテスト」や「モブテスト」のファシリテーターを依頼し、実際のテスト活動を通じて他のメンバーに思考プロセスや観点を共有・伝承させる"
        ]
    }
}

def fix_specific_questions():
    print("--- ピンポイント修正を開始します ---")
    
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
                            # 修正実行（データの上書き）
                            q["options"] = correct_data["options"]
                            q["answer"] = correct_data["answer"]
                            file_modified = True
                            print(f"修正しました: {filename}")
                            print(f"  対象: {target_key[:20]}...")

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
    fix_specific_questions()
    input()
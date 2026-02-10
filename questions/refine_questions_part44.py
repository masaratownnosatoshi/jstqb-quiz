import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第44弾・Vol.84-86 最終仕上げ）
# ==========================================
fixes = {
    # ---------------------------
    # 第1章 一般 Vol.86 (ch1_general_vol86.json)
    # ---------------------------
    "Q1-GEN-V86-01": { # 終了基準未達時の対応
        "options": [
            "基準未達なので、無条件でリリースを延期する（ビジネス判断の欠如）",
            "欠陥の発生確率と影響度（リスク）を再評価し、ビジネスオーナーに対して「回避策があるためリスク受容可能である」という根拠を示して、特例承認（Waiver）による条件付きリリースを提案する",
            "欠陥の重要度を勝手に「中」に下げて、基準をクリアしたことにする（改ざん）",
            "リリース判定会議（Go/No-Go）を開催せず、PMの独断でリリースを強行する（ガバナンスの欠如）" # 「叱責」を修正
        ],
        "answer": ["欠陥の発生確率と影響度（リスク）を再評価し、ビジネスオーナーに対して「回避策があるためリスク受容可能である」という根拠を示して、特例承認（Waiver）による条件付きリリースを提案する"]
    },

    # ---------------------------
    # 第1章 一般 Vol.84 (ch1_general_vol84.json)
    # ---------------------------
    "Q1-GEN-V84-01": { # ステークホルダー報告
        "options": [
            "スタックトレースのログを見せて、技術的な深刻さを説明する（相手の理解度を無視）",
            "「製品の発売には問題ない」とだけ伝える（根拠不足）",
            "「重大な問題があるが、回避策があるためビジネス影響（発売延期リスク）は低い」という要約と、顧客への案内案を提示する",
            "発生した欠陥の技術的な詳細情報だけを羅列し、ビジネスへの影響については言及しない（相手の関心を無視）" # 「謝罪」を修正
        ],
        "answer": ["「重大な問題があるが、回避策があるためビジネス影響（発売延期リスク）は低い」という要約と、顧客への案内案を提示する"]
    },
    "Q1-GEN-V84-02": { # テストコントロール
        "options": [
            "テストケースを全て実行するまでリリースを延期する（ビジネス機会の損失）",
            "残りのテストケースに対してリスク分析を行い、リスクレベル「高・中」のケースのみを実行し、「低」のケースはデスコープ（実施しない）判断を行う",
            "テスト実行のスピードを上げるため、結果の記録（エビデンス）を省略するよう指示する（監査リスクの増大）", # 「ランダム」を修正
            "テスト実行速度を3倍にするよう命令する（実現不可能な要求）"
        ],
        "answer": ["残りのテストケースに対してリスク分析を行い、リスクレベル「高・中」のケースのみを実行し、「低」のケースはデスコープ（実施しない）判断を行う"]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第44弾：Vol.84-86の最終修正を開始します...")

    for file_path in all_files:
        filename = os.path.basename(file_path)
        if filename.endswith(".py") or filename == "index.json":
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                continue

            file_modified = False
            
            for q in data:
                q_id = q.get("id")
                
                if q_id in fixes:
                    fix_data = fixes[q_id]
                    
                    if "options" in fix_data:
                        q["options"] = fix_data["options"]
                    if "answer" in fix_data:
                        q["answer"] = fix_data["answer"]
                    if "explanation" in fix_data:
                        q["explanation"] = fix_data["explanation"]

                    print(f"  修正適用: {q_id} ({filename})")
                    file_modified = True

            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                updated_count += 1
                
        except Exception as e:
            print(f"  読み込みエラー: {filename} - {e}")

    print("-" * 30)
    print(f"完了: 合計 {updated_count} ファイルを最適化しました。")

if __name__ == "__main__":
    refine_questions()
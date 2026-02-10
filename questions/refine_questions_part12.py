import json
import os
import glob

# ファイルが保存されているディレクトリ
BASE_DIR = "."

# ==========================================
# 修正データ定義（第12弾・Vol.8修正）
# ==========================================
fixes = {
    # ---------------------------
    # 第2章 一般 Vol.8 (ch2_general_vol8.json)
    # ---------------------------
    "Q2-GEN-V8-01": { # ODC (Orthogonal Defect Classification)
        "options": [
            "開発者個人のスキル不足を特定し、人事評価の減点材料として利用する",
            "欠陥の「種類」や「トリガー」などを多角的に分類し、開発プロセスの弱点を統計的に分析する",
            "バグの修正にかかった時間のみを計測し、開発スピードを競わせる",
            "発見された順に番号を振り、単なる管理IDとして扱う"
        ],
        "answer": ["欠陥の「種類」や「トリガー」などを多角的に分類し、開発プロセスの弱点を統計的に分析する"]
    },
    "Q2-GEN-V8-02": { # 結合テストでの単体バグ多発
        "options": [
            "結合テストの網羅性が高く、優秀なテストケースが作成されている証拠である",
            "単体テスト（ユニットテスト）が不十分、または実施されていない（品質の作り込み不足）",
            "仕様書の記述が曖昧であり、開発者が要件を理解できていない",
            "テスト環境のハードウェアスペックが不足している"
        ],
        "answer": ["単体テスト（ユニットテスト）が不十分、または実施されていない（品質の作り込み不足）"]
    },
    "Q2-GEN-V8-03": { # フォールトと故障
        "options": [
            "フォールト（欠陥）と故障（Failure）は同義語であり、文脈によって使い分けるだけである",
            "フォールト（欠陥）が実行されることで、システムが意図しない動作をするのが故障（Failure）",
            "故障（Failure）が原因となって、ソースコード上にフォールト（欠陥）が自動的に生成される",
            "フォールトはハードウェアの物理的な破損を指し、故障はソフトウェアの論理的な誤りを指す"
        ],
        "answer": ["フォールト（欠陥）が実行されることで、システムが意図しない動作をするのが故障（Failure）"]
    },

    # ---------------------------
    # 第2章 医療 Vol.8 (ch2_medical_vol8.json)
    # ---------------------------
    "Q2-MED-V8-01": { # ツールバリデーション
        "options": [
            "OSS（オープンソース）であるため、バリデーションなしでそのまま使用しても規制上の問題はない",
            "ツールバリデーション（Tool Validation）を実施し、そのツールが意図通りに機能し、品質記録の完全性を保てることを確認・文書化する",
            "OSSの利用はリスクが高すぎるため全面的に禁止し、高額な商用ツールのみを採用する",
            "開発者のローカルPCのみで使用し、公式な記録としては残さない運用にする"
        ],
        "answer": ["ツールバリデーション（Tool Validation）を実施し、そのツールが意図通りに機能し、品質記録の完全性を保てることを確認・文書化する"]
    },

    # ---------------------------
    # 第3章 クラウド Vol.8 (ch3_cloud_vol8.json)
    # ---------------------------
    "Q3-CLD-V8-01": { # FinOpsでのQA役割
        "options": [
            "コスト管理は経理部門の仕事であるため、QAチームは一切関与しない",
            "テスト環境のコスト効率を監視し、無駄なリソース消費（ゾンビインスタンス等）を削減する文化を醸成する",
            "クラウド利用料の請求書を処理し、支払い手続きを行う",
            "AWSのサポートセンターに対して、利用料金の値引き交渉を行う"
        ],
        "answer": ["テスト環境のコスト効率を監視し、無駄なリソース消費（ゾンビインスタンス等）を削減する文化を醸成する"]
    },

    # ---------------------------
    # 第3章 一般 Vol.8 (ch3_general_vol8.json)
    # ---------------------------
    "Q3-GEN-V8-01": { # TAE (Test Automation Engineer) スキル
        "options": [
            "手動テストの実行経験のみ（プログラミング知識は不要）",
            "プログラミング能力、テスト設計能力、および自動化アーキテクチャの構築能力",
            "マウス操作やタイピングの速度が極めて速いこと",
            "サーバーラックの設置や配線などの物理的なハードウェア知識"
        ],
        "answer": ["プログラミング能力、テスト設計能力、および自動化アーキテクチャの構築能力"]
    },
    "Q3-GEN-V8-02": { # 自動化チームと手動チームの分断
        "options": [
            "両チームを統合し、自動化エンジニアを手動テスターの中に配置して、自動化可能なケースを一緒に選定する（ハイブリッド化）",
            "自動化チームを解散し、開発者にテストコード作成をすべて委託する",
            "「自動化」をサービスとして手動チームに提供する形にし、定期的な同期ミーティングを設ける",
            "専門性を高めるため、両チームの交流を禁止し、完全に独立した組織として運営する"
        ],
        "answer": [
            "両チームを統合し、自動化エンジニアを手動テスターの中に配置して、自動化可能なケースを一緒に選定する（ハイブリッド化）",
            "「自動化」をサービスとして手動チームに提供する形にし、定期的な同期ミーティングを設ける"
        ]
    }
}

def refine_questions():
    all_files = glob.glob(os.path.join(BASE_DIR, "*.json"))
    updated_count = 0

    print("第12弾：問題データの修正を開始します...")

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
    print(f"完了: 合計 {updated_count} ファイルの問題を修正しました。")

if __name__ == "__main__":
    refine_questions()
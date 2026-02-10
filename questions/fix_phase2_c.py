import json
import os

# 修正設定（ファイル名 -> 問題ID -> 新しい選択肢テキスト）
FIX_MAP = {
    "ch1_general_vol83.json": {
        "Q1-GEN-V83-02": "自動テストはコストに見合わないと判断して全廃し、すべて手動テストに戻す"
    },
    "ch1_general_vol89.json": {
        "Q1-GEN-V89-03": "マネージャに叱責されるのを恐れ、進捗報告データを改ざんして順調に進んでいるように見せかける"
    },
    "ch2_cloud.json": {
        "Q2-CLD-04": "特定クラウドベンダーの独自機能（プロプライエタリなサービス）にフル依存し、他社への移行性（ポータビリティ）を考慮しない"
    },
    "ch2_medical_vol12.json": {
        "Q2-MED-V12-01": "誤検知はAIの特性（仕様）であるとして、改善を行わずにユーザーマニュアルに免責事項を記載するだけで済ませる"
    },
    "ch2_medical_vol3.json": {
        "Q2-MED-V3-01": "院内ネットワークに接続しないスタンドアロン機器であるため、セキュリティリスクはないと判断して侵入テストを省略する"
    },
    "ch2_medical_vol8.json": {
        "Q2-MED-V8-01": "自社環境での適合性検証（PoC）を行わず、インターネット上の評判や公式サイトの情報だけを信じて本番導入を決定する"
    },
    "ch3_aws_vol30.json": {
        "Q3-AWS-V30-01": "感情的な対立を避けるため、開発チームと運用チームの直接会話を禁止し、ドキュメントとチケットのみでやり取りさせる"
    },
    "ch3_cloud_vol10.json": {
        "Q3-CLD-V10-01": "SREチームの定型業務を守るため、開発チームからのアラート対応依頼や相談を全て拒否する"
    }
}

OUTPUT_DIR = "."

def fix_phase2_c():
    print("--- Phase 2-C: 医療・クラウド・AWS系残りの修正を開始 ---")
    
    fixed_count = 0
    
    for filename, id_map in FIX_MAP.items():
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(file_path):
            print(f"スキップ（ファイルなし）: {filename}")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_modified = False
            
            if isinstance(data, list):
                for q in data:
                    q_id = q.get("id")
                    
                    if q_id in id_map:
                        new_text = id_map[q_id]
                        # 修正対象のパターン
                        garbage_patterns = ["統計的なばらつき", "報告せずにこっそりと修正し"]
                        
                        if "options" in q:
                            new_options = []
                            replaced = False
                            for opt in q["options"]:
                                if any(g in opt for g in garbage_patterns):
                                    new_options.append(new_text)
                                    replaced = True
                                else:
                                    new_options.append(opt)
                            
                            if replaced:
                                q["options"] = new_options
                                file_modified = True
                                print(f"修正: {filename} (ID: {q_id})")
                                print(f"  -> 不適切な選択肢を修正しました。")
            
            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                fixed_count += 1
            else:
                print(f"変更なし: {filename} (対象のゴミデータが見つかりませんでした)")

        except Exception as e:
            print(f"エラー: {filename} ({e})")

    print("-" * 30)
    print(f"Phase 2-C 完了: {fixed_count} ファイルを修正しました。")
    print("エンターキーを押して終了してください...")

if __name__ == "__main__":
    fix_phase2_c()
    input()
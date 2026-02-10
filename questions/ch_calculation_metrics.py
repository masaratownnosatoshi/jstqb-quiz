import json
import os

OUTPUT_FILE = "ch_calculation_metrics.json"

new_questions = [
  {
    "id": "Q-CALC-METRIC-01",
    "chapter": "第2章",
    "level": "K3",
    "category": "モニタリング",
    "style": "計算",
    "type": "単一選択",
    "question": "【計算】システムの可用性（Availability）。\nあるシステムの運用データは以下の通りであった。\n\n・MTBF（平均故障間隔）：200時間\n・MTTR（平均修復時間）：4時間\n\nこのシステムの「稼働率（可用性）」として、最も近い値はどれか。",
    "options": [
      "95.0%",
      "96.0%",
      "98.0%",
      "99.9%"
    ],
    "answer": [
      "98.0%"
    ],
    "explanation": "【解説】\n可用性（稼働率） = MTBF ÷ (MTBF + MTTR)\n$$200 \\div (200 + 4) = 200 \\div 204 \\approx 0.9803$$\n\nしたがって、約98.0%となります。\n（稼働している時間の割合を求める計算です）",
    "tags": ["計算", "信頼性", "MTBF"]
  },
  {
    "id": "Q-CALC-METRIC-02",
    "chapter": "第2章",
    "level": "K3",
    "category": "モニタリング",
    "style": "計算",
    "type": "単一選択",
    "question": "【計算】重み付け欠陥密度の算出。\nモジュール規模：10 KLOC\n検出された欠陥の内訳と重み（Weight）は以下の通り。\n\n・致命的（W=10）：2件\n・重要（W=5）：10件\n・軽微（W=1）：20件\n\nこのモジュールの「重み付け欠陥密度（Weighted Defect Density）」はいくつか。",
    "options": [
      "3.2 /KLOC",
      "9.0 /KLOC",
      "32.0 /KLOC",
      "90.0 /KLOC"
    ],
    "answer": [
      "9.0 /KLOC"
    ],
    "explanation": "【解説】\n1. 重み付き総スコアを算出：\n   $$(2 \\times 10) + (10 \\times 5) + (20 \\times 1) = 20 + 50 + 20 = 90$$\n2. 密度を計算（スコア ÷ 規模）：\n   $$90 \\div 10 \\text{ KLOC} = 9.0$$\n\n単なる件数（32件）ではなく、重要度を加味した品質評価に使用します。",
    "tags": ["計算", "メトリクス", "品質分析"]
  },
  {
    "id": "Q-CALC-METRIC-03",
    "chapter": "第2章",
    "level": "K4",
    "category": "モニタリング",
    "style": "計算",
    "type": "単一選択",
    "question": "【計算】DDP（欠陥検出率）の算出。\nシステムテスト終了時点で「80件」のバグを検出し、修正してリリースした。\nしかしリリース後、半年間の運用で新たに「20件」のバグが市場で発見された。\n\nこのシステムテストにおける DDP（Defect Detection Percentage）は何％か。",
    "options": [
      "20%",
      "25%",
      "80%",
      "100%"
    ],
    "answer": [
      "80%"
    ],
    "explanation": "【解説】\nDDP = テストで見つけたバグ ÷ (テストで見つけたバグ ＋ リリース後に見つかったバグ)\n$$80 \\div (80 + 20) = 80 \\div 100 = 0.8$$\n\nつまり、潜在していたバグ全体の80%をテスト段階で除去できていたことになります。",
    "tags": ["計算", "メトリクス", "DDP"]
  },
  {
    "id": "Q-CALC-METRIC-04",
    "chapter": "第1章",
    "level": "K3",
    "category": "リスク管理",
    "style": "計算",
    "type": "単一選択",
    "question": "【計算】リスクエクスポージャー（期待損失額）の試算。\nある機能にセキュリティ脆弱性が残っている確率が「10%」と見積もられた。\nもし脆弱性が突かれて情報漏洩が発生した場合、損害賠償や対応費用で「5,000万円」の損失が出ると想定される。\n\nこのリスクに対する「リスクエクスポージャー（金額）」はいくらか。",
    "options": [
      "50万円",
      "500万円",
      "5,000万円",
      "5,500万円"
    ],
    "answer": [
      "500万円"
    ],
    "explanation": "【解説】\nリスクエクスポージャー（期待値） = 発生確率 × インパクト（損失額）\n$$0.1 (10\\%) \\times 5,000\\text{万円} = 500\\text{万円}$$\n\nリスク対応費用（緩和策のコスト）が500万円以下であれば、対策を実施する経済的合理性があると判断できます。",
    "tags": ["計算", "リスク", "見積もり"]
  },
  {
    "id": "Q-CALC-METRIC-05",
    "chapter": "第2章",
    "level": "K3",
    "category": "モニタリング",
    "style": "計算",
    "type": "単一選択",
    "question": "【計算】テスト進捗の遅延予測。\n・テスト総数：400件\n・当初計画：1日40件のペースで、10日間で完了予定。\n・現在、5日目が終了した時点で、完了数は「150件」である。\n\n今後も現在の実績ペース（平均速度）が続くと仮定した場合、テスト完了日は当初予定から何日遅れるか。",
    "options": [
      "遅れない（オンタイム）",
      "約2日遅れ",
      "約4日遅れ",
      "約7日遅れ"
    ],
    "answer": [
      "約4日遅れ"
    ],
    "explanation": "【解説】\n1. 現在の実績ペース算出：\n   $$150\\text{件} \\div 5\\text{日} = 30\\text{件/日}$$\n2. 残りのテスト数：\n   $$400 - 150 = 250\\text{件}$$\n3. 完了までの追加日数：\n   $$250 \\div 30 \\approx 8.33\\text{日} \\to 9\\text{日（切り上げ）}$$\n4. 総日数と遅延：\n   経過5日 ＋ 今後9日 ＝ 14日。\n   当初予定は10日だったので、$$14 - 10 = 4\\text{日}$$ の遅延となります。",
    "tags": ["計算", "スケジュール", "進捗予測"]
  }
]

def create_metric_calculations():
    print(f"--- メトリクス計算問題ファイル {OUTPUT_FILE} の作成 ---")
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_questions, f, ensure_ascii=False, indent=2)
        print(f"✅ 作成完了: {len(new_questions)} 問を追加しました。")
        print("注意: 最後に必ず regenerate_index.py を実行してください。")
        
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    create_metric_calculations()
    input("エンターキーを押して終了...")
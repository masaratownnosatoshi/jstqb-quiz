import json
import os

OUTPUT_FILE = "ch3_ai_extra_high_3.json"

new_questions = [
  {
    "id": "Q-AI-HIGH-3-01",
    "chapter": "第3章",
    "level": "K4",
    "category": "安全性",
    "style": "シナリオ",
    "type": "単一選択",
    "question": "【分析】自動運転システムの安全性評価において、機能安全（ISO 26262）の範囲外となる「システム自体は故障していないが、性能限界や環境要因によって危険な振る舞いをする（例：逆光でカメラが白飛びして歩行者を見落とす）」リスクを扱いたい。\n\nこの評価に対応する規格・概念として最も適切なものはどれか。",
    "options": [
      "SOTIF（Safety Of The Intended Functionality / ISO 21448）",
      "ASPICE（Automotive SPICE）",
      "FMEA（Failure Mode and Effects Analysis）",
      "GDPR（General Data Protection Regulation）"
    ],
    "answer": [
      "SOTIF（Safety Of The Intended Functionality / ISO 21448）"
    ],
    "explanation": "【解説】\n故障していなくても発生する危険（未知の危険な状況や、センサーの性能限界など）を扱うのが「SOTIF（意図された機能の安全性）」です。\n従来の機能安全（ISO 26262）は「故障」によるリスクを扱いますが、AI/自動運転では故障していなくても危険が生じるため、SOTIFの観点が必須となります。",
    "tags": ["AI", "安全性", "SOTIF", "自動運転"]
  },
  {
    "id": "Q-AI-HIGH-3-02",
    "chapter": "第3章",
    "level": "K4",
    "category": "継続的学習",
    "style": "シナリオ",
    "type": "単一選択",
    "question": "【分析】運用中のチャットボットに対し、最新の流行語に対応させるために新しいデータを追加して再学習を行った。\nすると、流行語には詳しくなった一方で、以前は正しく答えられていた基本的な挨拶や一般的な質問に対して誤答するようになってしまった。\n\nこの現象を何と呼び、どのような対策が有効か。",
    "options": [
      "現象：破滅的忘却（Catastrophic Forgetting） / 対策：過去の重要データを混ぜて再学習する（リハーサル法）",
      "現象：勾配消失 / 対策：層を浅くする",
      "現象：過学習 / 対策：データを減らす",
      "現象：データバイアス / 対策：公平性指標を導入する"
    ],
    "answer": [
      "現象：破滅的忘却（Catastrophic Forgetting） / 対策：過去の重要データを混ぜて再学習する（リハーサル法）"
    ],
    "explanation": "【解説】\n新しいタスクを学習すると、以前学習した知識が上書きされて失われてしまう現象を「破滅的忘却」と呼びます。\nこれを防ぐには、新しいデータだけでなく、過去のデータの一部も一緒に学習させる手法（リハーサルなど）が有効です。",
    "tags": ["AI", "再学習", "破滅的忘却"]
  },
  {
    "id": "Q-AI-HIGH-3-03",
    "chapter": "第3章",
    "level": "K4",
    "category": "テストオラクル",
    "style": "文章",
    "type": "単一選択",
    "question": "【適用】生成AI（画像生成や文章要約など）のテストにおいて、正解が一意に定まらないため、「期待結果」を厳密に定義することが難しい。\nこのような場合に使用される、絶対的な正解ではなく「ある程度の範囲や統計的な尤もらしさ」を基準とするオラクルを何と呼ぶか。",
    "options": [
      "確率的オラクル（Stochastic Oracle） / 統計的オラクル",
      "回帰オラクル（Regression Oracle）",
      "ヒューリスティックオラクル（Heuristic Oracle）",
      "モデルベースオラクル（Model-based Oracle）"
    ],
    "answer": [
      "確率的オラクル（Stochastic Oracle） / 統計的オラクル"
    ],
    "explanation": "【解説】\nAIのように出力が確率的に変動する場合や、正解が一つでない（画像生成など）場合、単一の期待値と比較することはできません。\n代わりに、多数の出力の分布や統計的特性（平均、分散、類似度スコアなど）を用いて合否を判定するものを「確率的オラクル」や「統計的オラクル」と呼びます。",
    "tags": ["AI", "テストオラクル", "生成AI"]
  },
  {
    "id": "Q-AI-HIGH-3-04",
    "chapter": "第3章",
    "level": "K3",
    "category": "非機能要件",
    "style": "分析",
    "type": "単一選択",
    "question": "【分析】エッジデバイス（スマートフォンやIoT機器）に搭載するAIモデルを開発している。\nモデルの精度（Accuracy）は非常に高いが、バッテリー消費が激しく、推論に時間がかかりすぎるという課題がある。\n\nこの課題を解決するために検討すべき技術的アプローチとして、最も適切なものはどれか。",
    "options": [
      "モデルの量子化（Quantization）や蒸留（Distillation）を行い、モデルサイズを軽量化する",
      "学習データを増量して、さらに精度を高める",
      "サーバーのGPUを増設して、クラウド側での処理能力を上げる",
      "アンサンブル学習を導入して、複数のモデルで予測する"
    ],
    "answer": [
      "モデルの量子化（Quantization）や蒸留（Distillation）を行い、モデルサイズを軽量化する"
    ],
    "explanation": "【解説】\nエッジAIでは「推論速度」や「消費電力」といった非機能要件が重要です。\n巨大なモデルを小さく軽くするための技術として、パラメータのビット数を減らす「量子化」や、大きなモデルの知識を小さなモデルに移す「蒸留」などが用いられます。",
    "tags": ["AI", "非機能要件", "軽量化"]
  },
  {
    "id": "Q-AI-HIGH-3-05",
    "chapter": "第3章",
    "level": "K4",
    "category": "データ品質",
    "style": "文章",
    "type": "単一選択",
    "question": "【評価】AI開発における「データ品質」の評価軸として、単にデータが正確であること（Accuracy）以外に重要な特性はどれか。\n特に、AIが「未知の状況」に対応できず、想定外の挙動をするリスクを低減するために重要な観点を選べ。",
    "options": [
      "網羅性（Completeness）と多様性（Diversity）",
      "機密性（Confidentiality）",
      "可用性（Availability）",
      "冗長性（Redundancy）"
    ],
    "answer": [
      "網羅性（Completeness）と多様性（Diversity）"
    ],
    "explanation": "【解説】\nAIは「学習データに含まれていないパターン」には弱いため、データの「網羅性（あらゆるケースが含まれているか）」と「多様性（偏りなくバリエーションがあるか）」が極めて重要です。\nここが不足していると、特定の条件下で極端に性能が落ちる原因となります。",
    "tags": ["AI", "データ", "品質特性"]
  }
]

def create_ch3_high_3():
    print(f"--- 第3章 追加難問Part3 {OUTPUT_FILE} の作成 ---")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_questions, f, ensure_ascii=False, indent=2)
        print(f"✅ 作成完了: {len(new_questions)} 問を追加しました。")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    create_ch3_high_3()
    input("エンターキーを押して終了...")
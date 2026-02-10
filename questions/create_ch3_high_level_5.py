import json
import os

OUTPUT_FILE = "ch3_ai_extra_high_5.json"

new_questions = [
  {
    "id": "Q-AI-HIGH-5-01",
    "chapter": "第3章",
    "level": "K4",
    "category": "強化学習",
    "style": "シナリオ",
    "type": "単一選択",
    "question": "【分析】お掃除ロボットの強化学習において、「ゴミを吸い取る」ことではなく「床にゴミがない状態にする」ことを報酬（Reward）として設定した。\nすると、ロボットはゴミを吸わずに「ゴミをカーペットの下に隠す」という行動をとるようになってしまった。\n\nこの現象を指す用語として、最も適切なものはどれか。",
    "options": [
      "報酬ハッキング（Reward Hacking / Specification Gaming）",
      "探索と活用のジレンマ（Exploration-Exploitation Dilemma）",
      "破滅的忘却（Catastrophic Forgetting）",
      "勾配消失（Vanishing Gradient）"
    ],
    "answer": [
      "報酬ハッキング（Reward Hacking / Specification Gaming）"
    ],
    "explanation": "【解説】\nAIが、設計者が意図したゴールではなく、報酬関数を最大化するための「抜け穴」を見つけて、予期せぬ行動をとることを「報酬ハッキング」と呼びます。\n報酬の設計（仕様）が不完全であることが原因です。",
    "tags": ["AI", "強化学習", "報酬ハッキング"]
  },
  {
    "id": "Q-AI-HIGH-5-02",
    "chapter": "第3章",
    "level": "K4",
    "category": "AIセキュリティ",
    "style": "シナリオ",
    "type": "単一選択",
    "question": "【分析】攻撃者が、公開されている顔認証APIに対して特定の入力を繰り返し送り、返ってくる信頼度スコア（Confidence Score）の変化を分析した。\nその結果、攻撃者は学習データに含まれていた特定の個人の顔画像を復元することに成功した。\n\nこの攻撃手法はどれか。",
    "options": [
      "モデルインバージョン攻撃（Model Inversion Attack）",
      "モデル抽出攻撃（Model Extraction Attack）",
      "回避攻撃（Evasion Attack）",
      "ポイズニング攻撃（Poisoning Attack）"
    ],
    "answer": [
      "モデルインバージョン攻撃（Model Inversion Attack）"
    ],
    "explanation": "【解説】\nモデルの出力（スコアなど）から、学習に使われた「生データ（個人情報など）」を逆算・復元しようとする攻撃を「モデルインバージョン攻撃」と呼びます。\nこれはプライバシー侵害の重大なリスクとなります。",
    "tags": ["AI", "セキュリティ", "プライバシー", "攻撃手法"]
  },
  {
    "id": "Q-AI-HIGH-5-03",
    "chapter": "第3章",
    "level": "K4",
    "category": "公平性評価",
    "style": "分析",
    "type": "単一選択",
    "question": "【分析】ある大学入試AIの公平性を検証した。\n・全体で見ると、男子の合格率が女子より高く、バイアスがあるように見えた。\n・しかし、学部ごと（理系・文系）に分けて分析すると、どの学部でも女子の合格率の方が高かった。\n（原因は、合格率の低い最難関学部に女子の志願者が集中していたためであった）\n\nこのように、データを細分化すると全体の傾向とは逆の結果が現れる現象を何と呼ぶか。",
    "options": [
      "シンプソンのパラドックス（Simpson's Paradox）",
      "モラベックのパラドックス（Moravec's Paradox）",
      "確証バイアス（Confirmation Bias）",
      "生存者バイアス（Survivorship Bias）"
    ],
    "answer": [
      "シンプソンのパラドックス（Simpson's Paradox）"
    ],
    "explanation": "【解説】\n集団全体で見た時の相関と、分割したサブグループで見た時の相関が異なったり、逆転したりする現象を「シンプソンのパラドックス」と呼びます。\n公平性評価においては、全体だけでなく内訳を見ないと誤った結論（AIが差別している、あるいはしていない）を導く危険があります。",
    "tags": ["AI", "公平性", "統計", "パラドックス"]
  },
  {
    "id": "Q-AI-HIGH-5-04",
    "chapter": "第3章",
    "level": "K4",
    "category": "学習データ分割",
    "style": "適用",
    "type": "単一選択",
    "question": "【適用】株価予測AIモデルを構築するため、過去10年分の時系列データを用意した。\nモデルの性能を正しく評価するための「交差検証（Cross Validation）」の方法として、最も適切なものはどれか。",
    "options": [
      "時系列分割（Time Series Split）：過去のデータで学習し、それより未来のデータでテストする順序を守る",
      "k分割交差検証（k-fold CV）：データをランダムにシャッフルして分割し、平均スコアを取る",
      "層化k分割交差検証（Stratified k-fold）：各分割内の株価上昇・下落の割合を均等にする",
      "Leave-One-Out検証：データ1つを除いて学習し、その1つを予測する"
    ],
    "answer": [
      "時系列分割（Time Series Split）：過去のデータで学習し、それより未来のデータでテストする順序を守る"
    ],
    "explanation": "【解説】\n時系列データにおいてランダムなシャッフル（k-fold）を行うと、「未来のデータで学習して過去を予測する（リーク）」ことが起きてしまい、不正に高い精度が出てしまいます。\n必ず「過去→未来」の時間順序を維持した検証（Walk-forward validationなど）が必要です。",
    "tags": ["AI", "データ", "時系列", "検証手法"]
  },
  {
    "id": "Q-AI-HIGH-5-05",
    "chapter": "第3章",
    "level": "K4",
    "category": "MLOps",
    "style": "分析",
    "type": "単一選択",
    "question": "【分析】開発環境（Offline）でのテストでは正解率98%を記録した画像分類モデルを本番環境（Online）にデプロイしたところ、エラーが多発し、全く機能しなかった。\n調査の結果、学習時に使用した画像データは「PNG形式・前処理済み」だったが、本番で入力される画像は「JPEG形式・生データ」であり、画素値の分布が異なっていたことが判明した。\n\nこの問題を指す専門用語はどれか。",
    "options": [
      "トレーニング・サービング・スキュー（Training-Serving Skew）",
      "モデルの蒸留（Model Distillation）",
      "ハイパーパラメータの不整合",
      "勾配爆発（Exploding Gradient）"
    ],
    "answer": [
      "トレーニング・サービング・スキュー（Training-Serving Skew）"
    ],
    "explanation": "【解説】\n学習時（Training）と推論時（Serving）で、データの処理パイプラインやインフラ、データ形式などが異なるために性能が乖離する現象を「Training-Serving Skew（学習と推論の歪み）」と呼びます。\n前処理ロジックをコードベースで共有するなどの対策が必要です。",
    "tags": ["AI", "MLOps", "障害事例"]
  }
]

def create_ch3_high_5():
    print(f"--- 第3章 追加難問Part5 {OUTPUT_FILE} の作成 ---")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_questions, f, ensure_ascii=False, indent=2)
        print(f"✅ 作成完了: {len(new_questions)} 問を追加しました。")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    create_ch3_high_5()
    input("エンターキーを押して終了...")
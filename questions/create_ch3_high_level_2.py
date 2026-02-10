import json
import os

OUTPUT_FILE = "ch3_ai_extra_high_2.json"

new_questions = [
  {
    "id": "Q-AI-HIGH-2-01",
    "chapter": "第3章",
    "level": "K4",
    "category": "モデル評価",
    "style": "シナリオ",
    "type": "単一選択",
    "question": "【分析】クレジットカードの不正利用検知モデルを開発している。\n全取引データの「99.9%」は正常取引で、不正取引はわずか「0.1%」である。\n開発したモデルは「全ての取引を『正常』と予測する」だけの単純なものだったが、正解率（Accuracy）は「99.9%」と算出された。\n\nこのモデルの性能を正しく評価するために使用すべき指標はどれか。",
    "options": [
      "正解率（Accuracy）と特異度（Specificity）",
      "適合率（Precision）、再現率（Recall）、およびF値（F1-score）",
      "平均絶対誤差（MAE）",
      "決定係数（R2スコア）"
    ],
    "answer": [
      "適合率（Precision）、再現率（Recall）、およびF値（F1-score）"
    ],
    "explanation": "【解説】\nデータに極端な偏り（不均衡データ）がある場合、正解率（Accuracy）は役に立ちません（何も検知しなくても高得点になるため）。\n不正（少数派クラス）をどれだけ正しく見つけられたかを示す「再現率（Recall）」や、それらを統合した「F値」で評価する必要があります。",
    "tags": ["AI", "メトリクス", "不均衡データ"]
  },
  {
    "id": "Q-AI-HIGH-2-02",
    "chapter": "第3章",
    "level": "K4",
    "category": "運用モニタリング",
    "style": "シナリオ",
    "type": "単一選択",
    "question": "【分析】夏服の売上予測モデルを構築し、7月にリリースして高精度を記録した。\nしかし、11月に入るとモデルの予測精度が急激に低下した。\n入力データの形式やシステム構成に変更はない。\n\nこの現象の原因として最も可能性が高く、どのような対策が必要か。",
    "options": [
      "原因：過学習（Overfitting） / 対策：ドロップアウト層を追加する",
      "原因：勾配消失（Vanishing Gradient） / 対策：活性化関数をReLUに変更する",
      "原因：コンセプトドリフト（Concept Drift） / 対策：直近のデータを含めてモデルを再学習させる",
      "原因：データポイズニング / 対策：セキュリティログを監査する"
    ],
    "answer": [
      "原因：コンセプトドリフト（Concept Drift） / 対策：直近のデータを含めてモデルを再学習させる"
    ],
    "explanation": "【解説】\n時間の経過や環境の変化（季節の変わり目など）により、入力データと正解の関係性が変化することを「コンセプトドリフト（またはデータドリフト）」と呼びます。\n夏服の傾向で学習したモデルは冬服の予測には適さないため、最新データでの再学習が必要です。",
    "tags": ["AI", "ドリフト", "運用"]
  },
  {
    "id": "Q-AI-HIGH-2-03",
    "chapter": "第3章",
    "level": "K4",
    "category": "説明可能性（XAI）",
    "style": "文章",
    "type": "単一選択",
    "question": "【適用】ディープラーニングを用いた融資審査AIが、ある顧客の申請を却下した。\n顧客から「なぜ却下されたのか理由を知りたい」と問い合わせがあったが、モデル自体はブラックボックスである。\n\n特定の入力（この顧客のデータ）に対して、どの特徴量が予測に寄与したかを近似的に説明するために適したツール/手法はどれか。",
    "options": [
      "LIME（Local Interpretable Model-agnostic Explanations）",
      "グリッドサーチ（Grid Search）",
      "主成分分析（PCA）",
      "GAN（Generative Adversarial Networks）"
    ],
    "answer": [
      "LIME（Local Interpretable Model-agnostic Explanations）"
    ],
    "explanation": "【解説】\nLIMEは、ブラックボックスモデルの特定の予測結果に対し、その周辺のデータを少し変化させて挙動を見ることで、「局所的（Local）な説明」を生成する技術です。\nこれにより、「年収が低かったから」「勤続年数が短かったから」といった理由付けが可能になります。",
    "tags": ["AI", "XAI", "説明可能性"]
  },
  {
    "id": "Q-AI-HIGH-2-04",
    "chapter": "第3章",
    "level": "K4",
    "category": "学習状況の分析",
    "style": "グラフ分析",
    "type": "単一選択",
    "question": "【分析】ニューラルネットワークの学習曲線（Learning Curve）を確認したところ、以下の傾向が見られた。\n\n・訓練データ（Training）の損失（Loss）は、エポックが進むにつれて限りなく0に近づいている。\n・検証データ（Validation）の損失は、途中まで下がっていたが、ある時点から逆に上昇し始めた。\n\nこの状態は何と呼ばれ、適切な対処法はどれか。",
    "options": [
      "状態：学習不足（Underfitting） / 対処：学習時間を延ばす",
      "状態：過学習（Overfitting） / 対処：アーリーストップ（Early Stopping）を適用する",
      "状態：勾配爆発 / 対処：勾配クリッピングを行う",
      "状態：最適収束 / 対処：特になし（学習完了）"
    ],
    "answer": [
      "状態：過学習（Overfitting） / 対処：アーリーストップ（Early Stopping）を適用する"
    ],
    "explanation": "【解説】\n訓練データだけに過剰に適応し、検証データ（未知データ）での性能が悪化し始める現象は「過学習（オーバーフィッティング）」です。\n検証ロスが上がり始めた時点で学習を打ち切る「アーリーストップ」などが有効な対策です。",
    "tags": ["AI", "過学習", "グラフ分析"]
  },
  {
    "id": "Q-AI-HIGH-2-05",
    "chapter": "第3章",
    "level": "K3",
    "category": "テスト環境",
    "style": "文章",
    "type": "単一選択",
    "question": "【適用】自動運転車のAI制御システムをテストしたい。\n実車を使って「子供が飛び出してくる」などの危険なシナリオをテストするのはリスクが高く、コストもかかる。\n\n実機（ハードウェア）の一部または全部をコンピュータ上のモデルで模擬し、安全かつ大量にテストを実行するための環境として、最も適切な用語はどれか。",
    "options": [
      "フィールドテスト（Field Testing）",
      "A/Bテスト",
      "SiL（Software in the Loop） / HiL（Hardware in the Loop）シミュレーション",
      "静的解析（Static Analysis）"
    ],
    "answer": [
      "SiL（Software in the Loop） / HiL（Hardware in the Loop）シミュレーション"
    ],
    "explanation": "【解説】\n高リスク・高コストなAIシステムのテストには「シミュレータ」が不可欠です。\n・SiL：ハードウェアも含めてソフトで模擬する。\n・HiL：実際のECU（ハードウェア）をシミュレータに接続してテストする。\nこれらにより、現実では再現困難なエッジケースを安全に検証できます。",
    "tags": ["AI", "テスト環境", "自動運転"]
  }
]

def create_ch3_high_2():
    print(f"--- 第3章 追加難問Part2 {OUTPUT_FILE} の作成 ---")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_questions, f, ensure_ascii=False, indent=2)
        print(f"✅ 作成完了: {len(new_questions)} 問を追加しました。")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    create_ch3_high_2()
    input("エンターキーを押して終了...")
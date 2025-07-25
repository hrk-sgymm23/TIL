# 機械学習について

## 参考

- https://zenn.dev/yoshikawat64m/articles/009_ml_overview
- https://www.youtube.com/watch?v=EeSerya_9XE

## 機械学習とは

- コンピュータが経験から学ぶ技術のこと
- 人工知能の仕組みを担う部分
- 予測や分別を行うメイン機能

### 機械学習の実装
- 入力データ(画像、音声、自然言語)を数値に変換する必要がある
- **入力値**と出力される**目標値**
- 機械学習とは何をしているのか
  - **入力と出力の関係性や規則性を見つけ出す**

- パラメータ
  - 評価軸=誤差
  - 二次関数の切片と傾きがパラメータに当たる
  - 評価軸=評価関数...良し悪しを判断するための関数(式)

- モデル
  - 機械学習ではデータの特性を数式で表現したもの
  - モデル...データの規則性を表現した箱のもの
  - 学習済モデル...学習後数式が明確になったものを学習済みモデルという

- 推論
  - 学習した結果をもとに何かの出力を行うこと
  - 学習=規則性を見つけること

## AI、ディープラーニングとの違い

### AI
- Artificial Intelligence(人工知能)
  - 機械学習、ディープラーニングを内干した言葉
  - 人工知能 >>> 機械学習 >>> ディープラーニング
- 人間と同じような判断ができる技術のことを指す


### ディープラーニング
- 目的
  - 数値予測、画像分析、グループ分け
- 手法
  - 回帰分析、SVM、決定木分析、ディープラーニング


### 機械学習の3大分類

- 教師あり学習
  - 正解があるデータで学ぶ
  - 例: たくさんの猫と犬の写真を見せてどっちか判別できるようにする
- 教師なし学習
  - 正解は教えずにデータの中の塊やパターンを見つける
  - 例: 似た性格に人をグループ分けする
- 強化学習
  - 試行錯誤しながらご褒美をもらって学ぶ
  - 例: ゲームで勝ったらポイントを与える活法を学ぶ


## 教師あり学習
- 入力から何かを予測をしたい場合を考える
- 予測する対象の正解データが事前に得られる場合、入力から正解データを出力するモデルを学習する方法のこと
- 答えとなるデータも一緒に学習させる
  - 答えとなるデータを「目標値」や「出力データ」「教師データ」という
- 答え(実測値)と予測した値(予測値)の差である誤差を小さくしたい

### 教師あり学習の種類
- 回帰
  - 数値を予測
- 分類
  - カテゴリを予測

## 教師なし学習
- 与えられたデータの特徴や法則性を自動的に抽出

### 教師なし学習の種類
- クラスタリング
  - 類似データをグループ化
  - 主な活用法...顧客の属性わけ
- 次元削減
  - データから重要な情報を抽出
  - 主成分分析...データ圧縮やデータの可視化をしたい場合

## 強化学習
- 活用シーンは限定的



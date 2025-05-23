# データマネジメントに出てくる単語を調べる

## データカタログについて

出典: https://blog.trocco.io/glossary/data-catalog

### データカタログとは
- 「どのようなデータ構造であるか」「今どこにあるのか」「どのように取得されたのか」などのデータの説明するデータをメタデータという
- データカタログはメタデータを管理するシステムのことを指す
- メタデータの管理を通じて大元のデータに対してより高度なデータマネジメントを可能にするのがデータカタログの意義

<データカタログの例>(chatgptより生成)
| メタデータの項目 | 内容 |
| --- | --- |
| データセット名 | web_access_logs |
| 保存場所 | BigQuery: project.dataset.web_access_logs |
| データの更新頻度 | 毎日午前3時にバッチ処理で更新 |
| データの所有者 | marketing-team@datacompany.com |
| 取得方法 | GA4からバッチ処理で取得 |
| 利用用途 | ユーザー行動分析、コンバージョン分析など |
| データのスキーマ | user_id (string), session_id (string), ... |
| 注意事項 | access_timeはUTC。JSTに変換が必要。 |
| 最終更新日 | 2025-04-12 |


### データカタログの管理例
- ツールやクラウドのマネージドサービスを使う
- Google Cloudの場合
  - [Data Catalog の概要](https://cloud.google.com/data-catalog/docs/concepts/overview?hl=ja)


## データクレンジングについて

出典: https://www.nttdata-gsl.co.jp/related/column/how-to-start-data-cleansing.html

### データクレンジングとは
- データクレンジングとはデータ品質を向上させるためにデータを洗浄すること。データクリーニングとも呼ばれる

### なぜデータクレンジングが必要なのか
- 企業が保有するデータを活用しようとした際、部署ごと担当者ごとにデータが違うため、データを十分に活用できないケースがある
- なぜならデータの粒度や表記方法が違うから
  - データの半角全角
  - 空白や区切り文字
  - 法人格
  - 住所や電話番号
- 結果、検索しても必要なデータを見つけることができない。また同じデータが重複していることの気づかない場合、同じ業務を重複してしまうことがある。
- 上記のようなデータを「ダーティーデータ」という

### ダーティーデータが生まれる原因
- 誤登録
- 重複登録
- 表記の揺れ
- 情報の欠如

### データクレンジングの導入の理想的な進め方

#### 保有しているデータ資産の状況を把握
- どのデータがどのように汚れているかがわからなければ、どのようにクレンジングするかを判断できない
- データ欠損、表記の揺れ、誤表記、生合成、精度、重複といった基準に基づき、現状を確認することがスタート

#### 改善するためのルールとそれに沿った実行
- 改善するためのルートを定め、やっとクレンジングを実行できる。改善に向けたルールとして考えられるものは変換する作業が必要
- 全角は数値として認識されないため、半角に修正が必要


## ELT/ETL

- ELT/ETL違い...つまり、ETLとELTでは変換処理を行う順番と場所が異なる
- 

出典: 
  https://it-trend.jp/etl/article/252-0002
  https://blog.trocco.io/glossary/elt


### ELT
- **様々なデータを抽出/変換してデータベースに統合**
- ETLとは様々なデータを利用しやすい形に変換して保管する工程のこと
- Extract, Transform, Loadのことをさす
- ETLにてデータを収集し編集し使用しやすい形に統一されたDBとして統合することで効率化を図ることが可能。
  - 上記にて保存されるDBはDWH
 
- データ抽出と同時に分析用の加工も行う
- DWHに直接データマートを作成する

### ETL
- Extract, Load, Transformのことをさす
- **データが蓄積されたデータベース内でデータ変換**
- ETLでは専用ツールを使って変換したデータをDWHなどのDB保存する

- データをそのまま抽出しDWH上で分析用の加工も行う
- 生データと加工データが併存する
- ELTの方が運用コストが高くなりがち

## データレイク

出典: 
  https://aws.amazon.com/jp/what-is/data-lake/
  https://www.talend.com/jp/resources/what-is-data-lake/

### データレイクとは
- 規模に関わらず全ての構造化データと非構造化データを一元的に保存できる
- データをそのままの形で保存できるため、データを構造化しておく必要がない
- またダッシュボードや可視化、ビックデータ処理、リアルタイム分析などの様々なタイプの分析を実行し的確な意思決定に役立てることができる

- データレイクの仕組みはスキーマオンリードと呼ばれる原則に基づいている
- これは格納前のデータが適合する必要のある事前定義されたスキーマが必要ないことをさす


### データレイク VS データウェアハウス
<共通>
- 両方とも組織内の様々なデータストアに統合するストレージリポジトリ
- 両方とも様々なアプリケーションにデータを投入するワンストップのデータストアを作成することを目的とする
<違い>
- スキーマオンリード vs スキーマオンライト
- ユーザーのアクセシビリティが単純 vs 複雑
- 柔軟　vs 硬直

## データウェアハウス
出典: https://www.intra-mart.jp/im-press/useful/data_warehouse
- データウェアハウスとは膨大なデータを整理しながら目的別に保管するDBのこと

### DBとの違い
- DBは多方面に蓄積されたデータの集合であり、保存されているのは生のデータ
- 生のデータで保存されているままではデータ分析が困難

- DWHは分析に必要なデータが業務横断的に管理できる形で整理されているため「分析に特化したデータの集合体」と言える

### データレイクとの違い
- データレイクは分散しているデータを一箇所に集めたシステムを指す
- DWHやDBと似た概念を持つが保管されるデータ内容が違う
  - データレイクでは動画や画像、文書、メールなどのあらゆるデータが加工されることなく保管可能

### データマートとの違い
- データマートは特定の目的に利用するデータ倉庫のこと
- DWHに蓄えられたデータからさらに使いやすいように目的に合わせて作成する
- DWH、データレイク、DBより小規模でデータを抽出して使う

## データマート

- 出典:
  - https://talend.com/jp/resources/what-is-data-mart/
  - https://www.nttdata-value.co.jp/glossary/data-mart
- データマートは特定のユーザーグループのニーズに対するサブジェクト思考のDB
- システムに蓄積された膨大なデータの中からデータ利用者の用途、目的などに応じて必要なものだけを抽出、加工、利用しやすい形に各校したDBのこと
- 反対に特定の目的に限定せず複数のシステムからデータを集めてきた倉庫のものをDWH
- つまりデータマートはDWHから特定の目的に合わせて抜き出したもの

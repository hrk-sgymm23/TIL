# データマネジメントに出てくる単語を調べる

## データカタログについて

出典: https://blog.trocco.io/glossary/data-catalog

### データカタログとは

- 「どのようなデータ構造であるか」「今どこにあるのか」「どのように取得されたのか」などのデータの説明するデータをメタデータという。
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


## データクレンジングとは

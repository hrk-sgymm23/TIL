# リヴァプールの結果、選手データをまとめたファンサイトを作る

## 技術スタック
- Versel
  - Next,Reactをホスティング
- CloudRun
  - Flaskアプリをホスティング
-　試合結果や選手情報取得
  - https://www.football-data.org/
- FireStore
  - football-data.orgより入手したデータを演算し、結果を格納する。
  - フロントエンドより演算した結果を参照

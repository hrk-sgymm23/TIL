# リヴァプールの結果、選手データをまとめたファンサイトを作る

# 技術スタック
- Versel
  - Next,Reactをホスティング
- CloudRun
  - Flaskアプリをホスティング
- https://www.football-data.org/
  - 試合結果や選手情報取得
- FireStore
  - football-data.orgより入手したデータを演算し、結果を格納する。
  - フロントエンドより演算した結果を参照
 
# 作りたい機能
- 試合結果をAPIが更新されたタイミングで反映
- 上記のタイミングでXに公式アカウントを作って試合結果を通知
- 選手のスタッツを計測しランキング形式で表示

# 考えること
- バッチ処理がメインになるが、試合は定期的ではなく不定であるためどのようにするか
- Cloud Runに対するAPI制限、スケーリング制限

# football-data.orgを使ってみる
- 会員登録
https://www.football-data.org/client/register

`x-auth-token`をリクエストに含める
<img width="1440" alt="スクリーンショット 2024-09-30 22 08 04" src="https://github.com/user-attachments/assets/4b1c4938-86a3-457d-b484-817103e6373a">

## APIの仕様を考慮した構成

football-data.orgでは1分間10リクエストまで。
アクセスがあるたびにfootball-data.orgにアクセスしていてはアクセス制限にすぐ到達してしまう。
そのため、１時間に一回football-data.orgにアクセスしFireStoreへ演算に必要なデータを格納するようなjobを作成する。





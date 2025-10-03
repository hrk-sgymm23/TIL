# コンテナ基礎/Docker Compose

## Docker Compose
- 複数コンテナによるマイクロサービスを作成/管理するための仕組み
  - YAML形式でネットワーク、ボリューム、コンテナを一括定義
  - 専用の`docker compose`コマンドで一括管理
- ここのdockerコマンドをYAMLに直したような状態
  - ここのコンテナをdocker composeではサービスという
- ログ
  - `docker compose logs {service name}`でログ出力
- ただし単一ファイル専用

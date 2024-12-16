# GCEにおけるポート解放

セキュリティグループを設定し、任意のポートを許可する
- [【5】GCP(GCE)でRailsアプリを外部IPアドレス+3000番ポートで動かしてみる(環境変数COMPOSE_FILE、GCE+Docker+Rails+Puma+PostgreSQL)](https://sakura-bird1.hatenablog.com/entry/2019/03/12/034427#6-3000%E7%95%AA%E3%83%9D%E3%83%BC%E3%83%88%E3%82%92%E9%96%8B%E3%81%91%E3%82%8B)

`gcloud compute ssh`の`-L`オプションを使ってポートフォワードする
- [Google Compute Engine で SSH Port Forwarding する]

# `exec /usr/bin/entrypoint.sh: exec format error`

https://qiita.com/OmeletteCurry19/items/fd057a7448aa3072fd1e

以下のようにして解消
```bash
$ cd backend/
# --platform linux/amd64をつける
$ docker build --platform linux/amd64  -t ass-rails-ecr-staging .
$ docker tag ass-rails-ecr-staging:latest 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/ass-rails-ecr-staging:stg
```

## 一旦リソース削除

RDS,ALB,ECSは削除→戻す際は依存関係に気を付ける

## DBのスナップショットが有効になっていたため調査
```terraform
resource "aws_db_instance" "main" {
~
  skip_final_snapshot             = true
~
```
`skip_final_snapshot`をtrueにすることで削除する際にスナップショットを作成しなくできる。

## VPC料金がかかってる理由
- https://techblog.forgevision.com/entry/AWS/public-ipv4-cost

> 2024 年 2 月1 日以降、サービスに接続されているかどうかに関係なく、すべてのパブリック IPv4 アドレスに対して、IP あたり 0.005 USD/時間（およそ 3.6 ドル/月）の料金が発生します。日本円に換算しますと、2023 年 8 月 4 日時点の為替レートは、1 USD あたり 142.66 円となっておりますので、IP あたりおよそ 513 円/月の費用が発生することとなります。


## NatGateway　vs VPCエンドポイント

### VPCエンドポイント
1エンドポイントにつき0.014USD/h
- 1ヶ月10.08USD
- ASSは5個必要なので50USD/m

### NATGateway
1ゲートウェイにつき0.062USD
- 1ヶ月33USD
- ASSは2個必要なので66USD

### どのような構成にするか

- NAT & Endpointだと帰って高くつく
- どちらにせよエンドポイントは必要
- NATオンリーで対応、、

### NATを節約したい
- [サーバレスでNAT Gatewayの起動・停止を管理してみた](https://www.ntt-tx.co.jp/column/dojo_aws_blog/20180411/)
laambdaでやろう

### Terraformで管理したい
- [TerraformでAWS Lambdaをデプロイする方法](https://qiita.com/curlneko/items/15607f8ef319cc97a75e)

### 次やること
- Lambdaで簡単なコードをterraform管理できるようにする
- 上記ができたらNatGateway作成
- そしてNatGatewayを自動作成、自動停止するコードを実装しEventBridgeで提示実行できるようにする





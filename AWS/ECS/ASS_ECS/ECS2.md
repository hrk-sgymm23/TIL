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

## 下記を参考にterraformでlambdaを実装
https://zenn.dev/not75743/articles/7a7d3a2fc7e788#%E5%AE%9F%E8%A1%8C
https://qiita.com/TheParkSider/items/bd4dd71a282761508bd4

```terraform
~
# ファイル名.関数名
handler = main.handler
~
```

### Lambda x terraformにおける環境変数について

```terraform
  filename         = var.file_name
  source_code_hash = var.code_hash
  function_name    = var.function_name
  role             = aws_iam_role.lambda_role.arn
  runtime          = "python3.9"
  handler          = var.handler
  # 下記を追加
  environment {
    variables = var.environments_variables
  }
}
```

### NATGWように必要な環境変数を整理

#### 削除
- ElasticIP
- SubnetId
- route_table_id
- NatGatewayの値は変動するため、SDKの`decribe`でその都度値をとってくる

#### 起動
- ElasticIP
- SubnetId
- route_table_id
- Natgateway Name(任意の名前)

### ルートテーブルの取り扱いについて
> はい、ルートテーブルの削除ではなく、NATゲートウェイに関連するルートを解除することは可能です。現在のコードで使用している client.delete_route は、ルートテーブル自体を削除するのではなく、特定のルートを削除しています。これにより、ルートテーブルは保持され、特定のルート（この場合はNATゲートウェイへのデフォルトルート）が削除されます。関連付けを解除するためには、ルートテーブルから特定のルートを削除するだけで十分です。既にその処理を実行するためのコードが含まれています：

```terraform
def delete_route_to_nat_gateway(route_table_id):
    logger.info('Deleting route to NAT Gateway...')
    
    response = client.delete_route(
        DestinationCidrBlock = '0.0.0.0/0',
        RouteTableId = route_table_id
    )
    logger.info(response)
```

## NATGateway,サブネット、ルートテーブルの関係性を再確認

- NATGateway自体にはルートテーブルを関連づけることはできない
- 正確にはパブリックサブネットに配置されたNATGatwayを用いてプライベートサブネットないのインスタンスがインターネットにアクセスすることが可能

ルートテーブルは共有できるものとして実装する

## zipファイルが見つからないエラー
```bash
module.natgateway_stop_func.aws_lambda_function.main: Creating...
╷
│ Error: creating Lambda Function (ass-natgw-stop-func-staging): operation error Lambda: CreateFunction, https response error StatusCode: 400, RequestID: 008d9cc3-9e2c-439f-a684-78b305dfa9b1, InvalidParameterValueException: Uploaded file must be a non-empty zip
│
│   with module.natgateway_stop_func.aws_lambda_function.main,
│   on ../../../modules/lambda/main.tf line 17, in resource "aws_lambda_function" "main":
│   17: resource "aws_lambda_function" "main" {
│
```

- zipファイルを開くとzipファイルが空であった
  - かくファイル反対だった。。。
 
## AWSSDK boto3 `waiter`について

https://qiita.com/kimihiro_n/items/f3ce86472152b2676004#waiter

```python
s3 = boto3.client('s3')

# object ができるまで待機する waiter を作成
waiter = s3.get_waiter('object_exists')

# NewObject.txt が作成されるまで sleep する
waiter.wait(Bucket='test_bucket', Key='NewObject.txt')
```

## LambdaをEventBridgeSchedulerで制御する(Terraform)

https://qiita.com/neruneruo/items/34d5092af44d79914849

`target`の書き方
```terraform
~
  target {
    arn      = aws_lambda_function.example.arn
    role_arn = aws_iam_role.eventbridge_scheduler.arn
  }
~
```

## 実際にLambda実行の際以下エラー
```bash
START RequestId: 186ad679-4183-4261-88b2-aa29c5ccdac4 Version: $LATEST
[INFO]	2024-07-07T08:48:32.383Z	186ad679-4183-4261-88b2-aa29c5ccdac4	Execute to Stopping NAT Gateway...
[INFO]	2024-07-07T08:48:32.383Z	186ad679-4183-4261-88b2-aa29c5ccdac4	Detach NatGateway Route...
[INFO]	2024-07-07T08:48:32.716Z	186ad679-4183-4261-88b2-aa29c5ccdac4	Delete NatGateway...
[INFO]	2024-07-07T08:48:32.790Z	186ad679-4183-4261-88b2-aa29c5ccdac4	{'NatGateways': [{'CreateTime': datetime.datetime(2024, 7, 7, 8, 43, 21, tzinfo=tzlocal()), 'NatGatewayAddresses': [{'AllocationId': 'eipalloc-0b7685e76d75fdcff', 'NetworkInterfaceId': 'eni-050585371c1e5c83f', 'PrivateIp': '172.10.0.127', 'PublicIp': '52.192.162.89', 'AssociationId': 'eipassoc-046b3ce7eaa0a340d', 'IsPrimary': True, 'Status': 'succeeded'}], 'NatGatewayId': 'nat-0e9e2c78c20df634b', 'State': 'available', 'SubnetId': 'subnet-02e9079cab760dce6', 'VpcId': 'vpc-0c5d0041a8f0d951a', 'Tags': [{'Key': 'Zone', 'Value': 'ap-northeast-1a'}], 'ConnectivityType': 'public'}], 'ResponseMetadata': {'RequestId': '2952260c-babc-44e1-bcc1-724665058d34', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '2952260c-babc-44e1-bcc1-724665058d34', 'cache-control': 'no-cache, no-store', 'strict-transport-security': 'max-age=31536000; includeSubDomains', 'vary': 'accept-encoding', 'content-type': 'text/xml;charset=UTF-8', 'transfer-encoding': 'chunked', 'date': 'Sun, 07 Jul 2024 08:48:32 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}
2024-07-07T08:48:35.401Z 186ad679-4183-4261-88b2-aa29c5ccdac4 Task timed out after 3.02 seconds

END RequestId: 186ad679-4183-4261-88b2-aa29c5ccdac4
REPORT RequestId: 186ad679-4183-4261-88b2-aa29c5ccdac4	Duration: 3018.67 ms	Billed Duration: 3000 ms	Memory Size: 128 MB	Max Memory Used: 85 MB	Init Duration: 502.96 ms	
```

上記タイムアウト300sで解決

## lambdaにてルートが紐づけられていないというエラー
ルートテーブルにて一つのCIDRへ向く設定は一つしか作成できない
`0.0.0.0/0`にたいし一つしかNATを紐付けられない

## NAT作成の際にEIPを毎回作るのではなくTerraformで作成したものを流用する

- AllocationIDをoutputに出力させ環境変数に埋め込む
```terraform
  environments_variables = {
    EipId1          = local.eip_id_list[0],
    EipId2          = local.eip_id_list[1],
    SubnetId1       = local.subnet_list[0],
    SubnetId2       = local.subnet_list[1],
    RouteTableId1   = local.route_table_id_list[0],
    RouteTableId2   = local.route_table_id_list[1],
    NatGatewayName1 = "${var.common_name}-Nat-GW-${var.environment}-1"
    NatGatewayName2 = "${var.common_name}-Nat-GW-${var.environment}-2"
  }
```

停止側でElasticIPを開放してしまっていたため修正。。。

# ALB作成

## terraform `aws_elb_service_account`について
[Terraform で ALB のアクセスログを設定するときに InvalidConfigurationRequest と出たら](https://kakakakakku.hatenablog.com/entry/2023/06/05/221205)

> エラーを解消する前に，ALB のアクセスログを Amazon S3 に流す場合は「ELB (Elastic Load Balancing) サービスアカウント」に対して Amazon S3 への権限を与える必要があるという仕様を以下のドキュメントを読んで理解しておく．さらにアカウントはリージョンごとに異なる点も要注意

 ## 作業手順

 - SGのモジュール作成
 - ALBモジュール作成
   - 前項で作成したSGのモジュールを参照する

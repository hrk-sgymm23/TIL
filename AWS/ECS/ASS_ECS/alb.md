# ALB作成

## terraform `aws_elb_service_account`について
[Terraform で ALB のアクセスログを設定するときに InvalidConfigurationRequest と出たら](https://kakakakakku.hatenablog.com/entry/2023/06/05/221205)

> エラーを解消する前に，ALB のアクセスログを Amazon S3 に流す場合は「ELB (Elastic Load Balancing) サービスアカウント」に対して Amazon S3 への権限を与える必要があるという仕様を以下のドキュメントを読んで理解しておく．さらにアカウントはリージョンごとに異なる点も要注意

 ## 作業手順

 - SGのモジュール作成
 - ALBモジュール作成
   - 前項で作成したSGのモジュールを参照する
  
 # ALBログバケット作成

 ## `Inappropriate value for attribute "policy": string required.`
 ```bash
Plan: 18 to add, 0 to change, 0 to destroy.
╷
│ Error: Incorrect attribute value type
│
│   on ../../../modules/alb/main.tf line 170, in resource "aws_s3_bucket_policy" "alb_log":
│  170:   policy = data.aws_iam_policy_document.alb_log
│     ├────────────────
│     │ data.aws_iam_policy_document.alb_log is object with 9 attributes
│
│ Inappropriate value for attribute "policy": string required.
```

## 末尾に`json`をつける
```terraform
resource "aws_s3_bucket_policy" "alb_log" {
  bucket = aws_s3_bucket.alb_log_stg.id
  # jsondecode関数を使う
  policy = data.aws_iam_policy_document.alb_log.json
}

data "aws_iam_policy_document" "alb_log" {
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["arn:aws:s3:::${aws_s3_bucket.alb_log_stg.id}/*"]
    principals {
      type        = "AWS"
      identifiers = [data.aws_elb_service_account.main.arn]
    }
  }
}
```

# `apply`時にエラー
```bash
 Error: creating ELBv2 Listener (arn:aws:elasticloadbalancing:ap-northeast-1:730335441282:loadbalancer/app/ass/7328d7b38fe00851): ValidationError: A certificate must be specified for HTTPS listeners
│ 	status code: 400, request id: 5d02a89c-2fe6-4c68-83d1-e9cdae28fe28
│
│   with module.alb_stg.aws_lb_listener.https,
│   on ../../../modules/alb/main.tf line 104, in resource "aws_lb_listener" "https":
│  104: resource "aws_lb_listener" "https" {
│
╵
╷
│ Error: error creating S3 bucket ACL for ass-alb-log-staging: AccessControlListNotSupported: The bucket does not allow ACLs
│ 	status code: 400, request id: VH8SSHKG7HSK0EK5, host id: SoGBhx6Nb2vG4TbxUc9K5wns8dVSyk6N5zLNuHhGMtQVMd5uXrebfMlow9VsCmB69iZRdWCTa8mOVDFB0pgQ+w==
│
│   with module.alb_stg.aws_s3_bucket_acl.alb_log_stg,
│   on ../../../modules/alb/main.tf line 144, in resource "aws_s3_bucket_acl" "alb_log_stg":
│  144: resource "aws_s3_bucket_acl" "alb_log_stg" {
```

# ALBの命名変更時にエラー
```bash
│ Error: deleting LB: OperationNotPermitted: Load balancer 'arn:aws:elasticloadbalancing:ap-northeast-1:730335441282:loadbalancer/app/ass/7328d7b38fe00851' cannot be deleted because deletion protection is enabled
│ 	status code: 400, request id: 02210dd2-60cd-4cc4-b561-6650c06023ed
```


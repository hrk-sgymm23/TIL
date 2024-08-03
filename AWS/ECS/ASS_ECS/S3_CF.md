# フロントエンド構築

## S3とCloudFrontを構築

`variable.tf`で変数を定義
```terraform
variable "environment" {
    description = "environment common name"
    type        = string
}

variable "service" {
    description = "service name"
    type        = string
}

variable "common_name" {
    description = "common name"
    type        = string
}
```


`terrafom.tfvars`で変数の値を定義
```terraform
environment = "staging"
service     = "ass-web"
common_name = "ass-stg"
```

`xxx.tf`で上記で作成した変数を利用
```terraform
module ass_web_s3_stg {
    source = "../../../modules/s3"
    common_name  = var.common_name
}
```

## s3のみ構築の際にエラー
```bash
error creating S3 bucket ACL for ass-staging: AccessControlListNotSupported: The bucket does not allow ACLs
│ 	status code: 400, request id: MJC8BFSRAM7FT92D, host id: cyp7Lnm/uaEy56YBVnFZ6LUPZLJHw/+f56Tr1zOaOjvz23i5kd2r37LbiXHp5KxJutV2PZgNuhvvVobSEkTTtA==
```

https://dev.classmethod.jp/articles/s3-acl-error-from-202304/
> 上記acl = "private"は既定 ACLという事前定義済みの許可設定です。が、前述の通り2023年4月以降はまずACLを有効にする必要があります。無効になっていたのでAccessControlListNotSupported: The bucket does not allow ACLsエラーが発生しました。

静的ページ表示のためACLは無効とした。

## CloudFront構築時に以下エラー
```bash
Error: Reference to undeclared resource
│
│   on ../../../modules/cloudfront/main.tf line 4, in resource "aws_cloudfront_distribution" "static-www":
│    4:         domain_name = aws_s3_bucket.main.bucket_regional_domain_name
│
│ A managed resource "aws_s3_bucket" "main" has not been declared in module.ass_web_cf_stg.
```

## Outputを使う
https://dev.classmethod.jp/articles/terraform_module_coordination/

## module間で値を参照したい

### 今回はcloudfrontの設定にてs3のidとドメインを指定したい
`modules/s3/output.tf`
```terraform
output "id" {
    value = aws_s3_bucket.main.id
}

output "bucket_regional_domain_name" {
    value = aws_s3_bucket.main.bucket_regional_domain_name
}
```

`modules/cloudfront/variable.tf`
```terraform
variable "s3_bucket_domain_name" {
    description = "bucket domain name"
    type        = string
}

variable "s3_bucket_id" {
    description = "bucket id"
    type        = string
}
```

`modules/cloudfront/main.tf`
```terraform
resource "aws_cloudfront_distribution" "static-www" {
    # aliases = ["${var.site_domain}"]
    origin {
        domain_name = var.s3_bucket_domain_name
        origin_id   = var.s3_bucket_id
~
```

`envirements/stg/web/s3.tf`
```terraform
module "ass_web_s3_stg" {
  source      = "../../../modules/s3"
  common_name = "${var.common_name}-${var.environment}"
}
```

`envirements/stg/web/cloudfront.tf`
`modules`.`s3の定義したmodule名`.`変数名`を指定する
```terraform
module "ass_web_cf_stg" {
  source                = "../../../modules/cloudfront"
  common_name           = "${var.common_name}-${var.environment}-distribusion"
  s3_bucket_domain_name = module.ass_web_s3_stg.bucket_regional_domain_name
  s3_bucket_id          = module.ass_web_s3_stg.id
}
```

### CloudFrontの`viewercertificate`について

```bash
viewer_certificate {
    # cloudfrontへのリンクを使う場合はtruebに設定
    cloudfront_default_certificate = true
}
```
## 次はs3の設定にて`aws_cloudfront_origin_access_identity.static-www.iam_arn`を参照したい
`modules/cloudfront/output.tf`
```terraform
output "oai_identifiers" {
    value = aws_cloudfront_origin_access_identity.static-www.iam_arn
}
```

`modules/cloudfront/variable.tf`
```terraform
variable "oai_identifiers" {
    description = "oai name"
    type        = string
}
```

`modules/cloudfront/main.tf`
```terraform
data "aws_iam_policy_document" "static-www" {
    statement {
        sid    = "Allow CloudFront"
        effect = "Allow"
        principals {
            type        = "AWS"
            # 定義したvariableを設定
            identifiers = [var.oai_identifiers]
        }
~
```

`enviroments/stg/web/s3.tf`
```terradform
module "ass_web_s3_stg" {
  source      = "../../../modules/s3"
  common_name = "${var.common_name}-${var.environment}"
  # 以下で利用
  oai_identifiers = module.ass_web_cf_stg.oai_identifiers
}
```

## S3へアップロード

```bash
$ ass/frontend/app

$ npm run build
```

```bash
$ aws s3 sync --delete ./build/ s3://ass-staging
$ aws cloudfront create-invalidation --distribution-id E2I7XFCFXR9YF6 --paths "/*"
```

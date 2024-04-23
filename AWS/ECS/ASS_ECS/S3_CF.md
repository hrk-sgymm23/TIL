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

### Outputを使う
https://dev.classmethod.jp/articles/terraform_module_coordination/
```bash
```




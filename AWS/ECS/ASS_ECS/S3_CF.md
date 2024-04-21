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

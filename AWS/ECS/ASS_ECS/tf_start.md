# ASS ECS Nginx

## 参考
- [【Rails+Docker】RailsプロジェクトのDocker化](https://zenn.dev/prune/books/28c2d690e11e45/viewer/e87aa4)
- [terraform入門: 環境構築 + AWS S3作ってみる(´・ω・｀)](https://zenn.dev/cureapp/articles/07fca4c86a0114)

## Terraform環境構築
```bash
$ export AWS_PROFILE=xxx
```

`main.tf`
```terraform
terraform {
    required_version = ">= 1.8.1"

required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 4.16"
        }
    }
}

provider "aws" {
    region = "ap-northeast-1"
}
```

- 下記エラーが出たがbrewでterraformを入れ直して解決
```
terraform init

Initializing the backend...
╷
│ Error: Unsupported Terraform Core version
│
│   on main.tf line 2, in terraform:
│    2:     required_version = ">= 1.8.1"
│
│ This configuration does not support Terraform version 1.5.0. To proceed, either choose another supported Terraform version or update this version constraint. Version constraints are
│ normally set for good reason, so updating the constraint may lead to other errors or unexpected behavior.
╵
```

## S3を作る
`enviroment/s3.tf`
```

## `terraform plan`でエラー
```bash
terraform plan

Planning failed. Terraform encountered an error while generating this plan.

╷
│ Error: Invalid provider configuration
│
│ Provider "registry.terraform.io/hashicorp/aws" requires explicit configuration. Add a provider block to the root module and configure the provider's required arguments as described in
│ the provider documentation.
│
╵
╷
│ Error: Invalid AWS Region:
│
│   with provider["registry.terraform.io/hashicorp/aws"],
│   on <empty> line 0:
│   (source code not available)
```

下記で解決できるか？
https://qiita.com/aiko-han/items/3878ddcdc0d2f069ad36

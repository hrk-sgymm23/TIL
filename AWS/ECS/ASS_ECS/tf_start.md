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
上記で解決できた

## `init`~`apply`

```bash
terraform init

Initializing the backend...

Initializing provider plugins...
- Reusing previous version of hashicorp/aws from the dependency lock file
- Installing hashicorp/aws v4.67.0...
- Installed hashicorp/aws v4.67.0 (signed by HashiCorp)

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_s3_bucket.sample will be created
  + resource "aws_s3_bucket" "sample" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "sample-bucket-test-0417"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = (known after apply)
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags_all                    = (known after apply)
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_s3_bucket.sample will be created
  + resource "aws_s3_bucket" "sample" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "sample-bucket-test-0417"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = (known after apply)
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags_all                    = (known after apply)
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_s3_bucket.sample: Creating...
aws_s3_bucket.sample: Creation complete after 2s [id=sample-bucket-test-0417]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

## ディレクトリ構成
```bash
ass_infra
└── enviroment
    ├── main.tf
    ├── provider.tf
    ├── s3.tf
    └── terraform.tfstate
```

下記の構成が参考になりそう
https://qiita.com/hatsu/items/8b30e68ba7252a749fe7#shared%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80

## `shared`フォルダを作る
`ass-tfstate-bucket`
https://ap-northeast-1.console.aws.amazon.com/s3/buckets/ass-tfstate-bucket?region=ap-northeast-1&bucketType=general&tab=objects


## `tfatate`を管理するs3を作成


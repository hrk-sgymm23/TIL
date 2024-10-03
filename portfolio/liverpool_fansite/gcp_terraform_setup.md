# GoogleCloudとTerraformのセットアップを行う

https://zenn.dev/oyasumipants/articles/8f0ac1a3395520#%F0%9F%92%BB-%E5%AE%9F%E9%9A%9B%E3%81%AE%E3%82%B3%E3%83%BC%E3%83%89

## gcloud CLIの設定
```bash
$ gcloud init
```
上記にて新規作成したプロジェクトをactivate

# tfstateをGCS管理にする

## GCSを作成

```bash
backend_setup
├── main.tf
├── provider.tf
└── variable.tf
```

`main.tf`
```hcl
resource "google_storage_bucket" "terraform_state" {
  name     = "liverpool-state-bucket"
  location = "ASIA"
  versioning {
    enabled = true
  }
}
```

`provider.tf`
```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
```

`variable.tf`
```bash
variable "project_id" {
  default = "[PROJECT_ID]"
}
variable "region" {
  default = "asia-northeast1"
}
```

## tfstateを移動

`backend.tf`
```
terraform {
  backend "gcs" {
    bucket = "liverpool-state-bucket"
    # 環境ごとに別のプレフィックスを用意
    prefix = "stg/setup"
  }
}
```



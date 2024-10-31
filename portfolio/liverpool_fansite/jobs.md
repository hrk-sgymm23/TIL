# FireStoreに定期的に書き込みに行くJobを作る

## 必要なリソース
- ArtifactRegistry
- CloudRun Jobs
- Sceduler
下記は今回既存のものを流用
- SerivceAccount(SecretManger,FireStore)
- SecretManger

## 必要な設定
- ArtifactRegistry
  - CloudRun用のサービスアカウントのアクセスを許可
- SecretManger
  - CloudRun用のサービスアカウントのアクセスを許可

## アプリケーションコードとDockerfileを用意しビルドしプッシュし実行
```bash
$ docker build --platform linux/amd64 -t asia-northeast1-docker.pkg.dev/liverpool-fansite/liverpool-fansite-jobs-stg/liverpool-jobs-app:latest
$ docker push asia-northeast1-docker.pkg.dev/liverpool-fansite/liverpool-fansite-jobs-stg/liverpool-jobs-app:latest

# ジョブの実行
$ gcloud run jobs execute liverpool-fansite-cloudrun-jobs-stg --region asia-northeast1
```


## Google Cloud　jobsリソースを作成
```hcl
# ServiceAccont
# Secret Manager のアクセス権限を持つサービスアカウントを作成
resource "google_service_account" "liverpool_fansite_sa" {
  project      = var.project_id
  account_id   = "${var.project_id}-sa"
  display_name = "Liverpool Fansite Service Account"
}

# Secret Manager の読み取り権限をサービスアカウントに付与
resource "google_project_iam_member" "secret_access" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.liverpool_fansite_sa.email}"
}

resource "google_project_iam_member" "firestore_admin_access" {
  project = var.project_id
  role    = "roles/datastore.owner"
  member  = "serviceAccount:${google_service_account.liverpool_fansite_sa.email}"
}

# CloudRun Jobs
resource "google_cloud_run_v2_job" "default" {
  name     = "${var.project_id}-cloudrun-jobs-stg"
  location = var.region
  project  = var.project_id

  template {
    template {
      service_account = google_service_account.liverpool_fansite_sa.email
      containers {
        image = "asia-northeast1-docker.pkg.dev/${var.project_id}/liverpool-fansite-jobs-stg/liverpool-jobs-app:latest"
        env {
          name = "FIRESTORE_DB_NAME"
          value_source {
            secret_key_ref {
              secret  = "firestore_name"
              version = "latest"
            }
          }
        }
      }
    }
  }
}

```


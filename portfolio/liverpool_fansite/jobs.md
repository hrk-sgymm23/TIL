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

# RunとJobsのTerraformコード

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

# CloudRun
resource "google_cloud_run_service" "liverpool_fansite_stg" {
  name     = "${var.project_id}-cloudrun-stg"
  location = var.region
  project  = var.project_id

  template {
    spec {
      service_account_name = google_service_account.liverpool_fansite_sa.email
      containers {
        image = "asia-northeast1-docker.pkg.dev/${var.project_id}/liverpool-fansite-stg/liverpool-app:latest"
        env {
          name = "FIRESTORE_DB_NAME"
          value_from {
            secret_key_ref {
              name = "firestore_name"
              key  = "latest"
            }
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
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

# アプリケーションコード
`Dockerfile`
```
# Use the official Python image.
FROM python:3.11

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

# Copy application dependency manifests to the container image.
COPY ./src/requirements.txt ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./src ./

# Run the message processing script on container startup.
CMD ["python", "main.py"]
```

`main.py`
```bash
import os
import google.cloud.firestore
import json

dbname = os.environ['FIRESTORE_DB_NAME']
db = google.cloud.firestore.Client(database=dbname)


def get_players():
    results = db.collection('players').stream()
    print(f"result: {results}")
    players = [doc.to_dict() for doc in results]

    players_dict = {}
    players_dict = players
    json.dumps(players_dict)

    print(players_dict)

if __name__ == '__main__':
    get_players()
```

`requirements.txt`
```txt
google-cloud-firestore
```


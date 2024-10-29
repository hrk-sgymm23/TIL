# Cloud Runに対しデプロイする

# まずFireStoreにデータを用意

https://zenn.dev/hrk_sgyumm23/articles/37a4b59ade305e

＃ CloudRunのデプロイ

## イメージ、ビルドプッシュ
```bash
$ cd liverpool_fansite_app/api/docker/run/prd
$ docker build --platform linux/amd64 -t asia-northeast1-docker.pkg.dev/liverpool-fansite/liverpool-fansite-stg/liverpool-app:latest -f Dockerfile ../../../
$ docker push asia-northeast1-docker.pkg.dev/liverpool-fansite/liverpool-fansite-stg/liverpool-app:latest
```

## 環境変数を措定したい
- FireStoreのDB情報

https://cloud.google.com/run/docs/configuring/secrets?hl=ja#command-line

### シークレットマネージャーにjsonを登録しPythonで取得
https://zenn.dev/ushknn/articles/aae542a72f2881

### FireStoreとの接続を修正
https://gakogako.com/python_firestore/#%E8%AA%8D%E8%A8%BC%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89

<参考(抜粋)>
```python
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials


def main():
    # ===================== Firebase =====================================
    # このPythonファイルと同じ階層に認証ファイルを配置して、ファイル名を格納
    JSON_PATH = '〇〇.json'

    # Firebase初期化
    cred = credentials.Certificate(JSON_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
```

# CloudRunをデプロイした際にSecretManager周りで403エラーになったためGUIより修正

<img width="1440" alt="スクリーンショット 2024-10-29 21 16 49" src="https://github.com/user-attachments/assets/7ca58dc0-ce7f-4a31-9407-9dd33462bae2">

# CloudRunデプロイした際にクレデンシャルが読み込めないエラー

```hcl
env {
          name = "GOOGLE_APPLICATION_CREDENTIALS"
          value_from {
            secret_key_ref {
              name = "liverpool-fansite-key"
              key  = "latest"
            }
          }
        }
        env {
          name = "FIRESTORE_DB_NAME"
          value_from {
            secret_key_ref {
              name = "firestore_name"
              key  = "latest"
            }
          }
        }
```


## サービスアカウントにFireStoreの権限を付与しシークレットに格納するのはDB名だけにする
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
```

## https://liverpool-fansite-cloudrun-stg-348534837533.asia-northeast1.run.app/api/v1/playersにアクセスした際に403になる
以下で解決


# 別PJ間のRunとSTOREについて(GPT)

```
Cloud RunとFirestoreが別プロジェクトにある場合、Firestoreにアクセスするサービスアカウントには、Firestoreが存在するプロジェクトのIAM設定で適切な権限を与える必要があります。

手順
サービスアカウントを作成: まず、Cloud Runプロジェクトでサービスアカウントを作成します。これがFirestoreにアクセスするために使用されます。

Firestoreプロジェクトでの権限付与: Firestoreが存在するプロジェクトで、Cloud RunプロジェクトのサービスアカウントにFirestoreの権限を付与します。

以下はTerraformの例です：

Cloud Runプロジェクトでのサービスアカウント作成
hcl
コードをコピーする
resource "google_service_account" "liverpool_fansite_sa" {
  project      = var.cloud_run_project_id  # Cloud RunのプロジェクトID
  account_id   = "${var.cloud_run_project_id}-sa"
  display_name = "Liverpool Fansite Service Account"
}
Firestoreプロジェクトでの権限付与
Firestoreが存在するプロジェクトの設定を行います。この部分はFirestoreプロジェクトにデプロイするTerraform設定ファイル内で記述します。

hcl
コードをコピーする
# Firestore 管理者権限をサービスアカウントに付与
resource "google_project_iam_member" "firestore_admin_access" {
  project = var.firestore_project_id  # FirestoreのプロジェクトID
  role    = "roles/datastore.owner"
  member  = "serviceAccount:${google_service_account.liverpool_fansite_sa.email}"
}
注意点
プロジェクト間でのサービスアカウントのメールアドレスの使用: Firestoreプロジェクトに対して、Cloud Runプロジェクトのサービスアカウントのメールアドレスを指定して権限を付与します。このメールアドレスは、google_service_account.liverpool_fansite_sa.email で取得できます。

正しいプロジェクトIDを使用すること: 各リソースの作成やIAM権限付与において、正しいプロジェクトIDを使用することが重要です。誤ったプロジェクトIDを指定すると、権限が付与されないか、他のプロジェクトに影響を及ぼす可能性があります。

このように設定することで、Cloud RunからFirestoreへのアクセスが可能になります。
```









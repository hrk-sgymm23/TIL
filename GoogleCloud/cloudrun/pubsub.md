# 次は下記を試す

[Cloud Run で Pub/Sub を使用するチュートリアル](https://cloud.google.com/run/docs/tutorials/pubsub?hl=ja#run_pubsub_dockerfile-python)


## 必要なロール
```bash
Cloud Build 編集者（roles/cloudbuild.builds.editor）
Cloud Run 管理者（roles/run.admin）
サービス アカウントの作成（roles/iam.serviceAccountCreator）
プロジェクト IAM 管理者（roles/resourcemanager.projectIamAdmin）
Pub/Sub 編集者（roles/pubsub.editor）
サービス アカウント ユーザー（roles/iam.serviceAccountUser）
Service Usage ユーザー（roles/serviceusage.serviceUsageConsumer）
ストレージ管理者（roles/storage.admin）
```

## Artifactregistry作成

```bash
$ gcloud artifacts repositories create pyhon-cloudrun-20240915 \
    --repository-format=docker \
    --location=asia-northeast1
```

## PubsubTopic作成
```bash
$ gcloud pubsub topics create pyhon-cloudrun-topic-20240915
```

## サンプルのリポジトリを使う
```bash
$ git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
```

## コンテナビルド時エラー
```bash
$ gcloud builds submit --tag asia-northeast1-docker.pkg.dev/python-cloudrun-435707/pyhon-cloudrun-20240915/pubsub
```

```bash
Creating temporary tarball archive of 9 file(s) totalling 6.5 KiB before compression.
Uploading tarball of [.] to [gs://python-cloudrun-435707_cloudbuild/source/1726388557.290675-a4b42b5d311d47d8bd9cb1ca15066919.tgz]
API [cloudbuild.googleapis.com] not enabled on project [python-cloudrun-435707]. Would you like to enable and retry (this will take a few
minutes)? (y/N)?  y

Enabling service [cloudbuild.googleapis.com] on project [python-cloudrun-435707]...
Operation "operations/acf.p2-276838580752-41aef1ab-ad41-4c79-a787-0f2246987e1a" finished successfully.
ERROR: (gcloud.builds.submit) FAILED_PRECONDITION: invalid bucket "276838580752.cloudbuild-logs.googleusercontent.com"; service account 276838580752-compute@developer.gserviceaccount.com does not have access to the bucket
```

### CloudBuildのサービスアカウント`276838580752.cloudbuild-logs.googleusercontent.com`にGCSへ書き込む権限がない

```bash
$ gcloud projects add-iam-policy-binding python-cloudrun-435707 \
    --member="serviceAccount:276838580752-compute@developer.gserviceaccount.com" \
    --role="roles/storage.admin"
```
上記のようにGCSのadmin権限を付与しビルド再度実行

## デプロイ
```bash
$ gcloud run deploy pubsub-tutorial --image asia-northeast1-docker.pkg.dev/python-cloudrun-435707/pyhon-cloudrun-20240915/pubsub  --no-allow-unauthenticated
```

## PubSubと連携

### Pubsubサブスクリプション用のサービスアカウント作成`cloud-run-pubsub-invoker`

```bash
$ gcloud iam service-accounts create cloud-run-pubsub-invoker \
    --display-name "Cloud Run Pub/Sub Invoker"
```

### 上記で作成したサービスアカウントにcloudrunを呼び出す`invoke`する権限追加
```bash
$ gcloud run services add-iam-policy-binding pubsub-tutorial \
--member=serviceAccount:cloud-run-pubsub-invoker@python-cloudrun-435707.iam.gserviceaccount.com \
--role=roles/run.invoker
```


### Pub/Subが本プロジェクト`python-cloudrun-435707`で認証トークンを作成できるようにする

```bash
gcloud projects add-iam-policy-binding python-cloudrun-435707 \
   --member=serviceAccount:service-276838580752@gcp-sa-pubsub.iam.gserviceaccount.com \
   --role=roles/iam.serviceAccountTokenCreator
```

### `invoke`を許可したサービスアカウントでPubSubサブスクリプション作成
```bash
$ gcloud pubsub subscriptions create myRunSubscription --topic pyhon-cloudrun-topic-20240915 \
--ack-deadline=600 \
--push-endpoint=https://pubsub-tutorial-powbfkvb6a-an.a.run.app// \
--push-auth-service-account=cloud-run-pubsub-invoker@python-cloudrun-435707.iam.gserviceaccount.com
```

### PubSubトピックへメッセージパブリッシュ
```bash
$ gcloud pubsub topics publish pyhon-cloudrun-topic-20240915 --message "Runner"
```

### CloudRunのログを確認

```bash
$ 2024-09-15 17:56:45.810 JST
Hello Runner!
```

# Cloudrunjobsでpubsubを試す

## Artifactregistry作成

```bash
$ gcloud artifacts repositories create pyhon-cloudrun-jobs-20240915 \
    --repository-format=docker \
    --location=asia-northeast1
```

## コンテナイメージをビルドし、push

`pubsub-jobs:stg`...`stg`タグをつけ、push

```bash
$ gcloud builds submit --tag asia-northeast1-docker.pkg.dev/python-cloudrun-435707/pyhon-cloudrun-jobs-20240915/pubsub-jobs:stg
```

## CloudRun Jobsを起動

```bash
$ gcloud run jobs create pubsub-run-jobs \
    --image asia-northeast1-docker.pkg.dev/python-cloudrun-435707/pyhon-cloudrun-jobs-20240915/pubsub-jobs:stg \
    --region asia-northeast1 \
    --set-env-vars GOOGLE_CLOUD_PROJECT=python-cloudrun-435707,PUBSUB_SUBSCRIPTION=myRunSubscription
```



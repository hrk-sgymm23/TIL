# CloudRun Serviceにてメールやpush通知

## ローカルで実行する

### composeファイル用意

```yml
version: '3.8'

services:
  pubsub-app:
    build:
      context: .
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    tty: true
    volumes:
      - .:/app
```

`Dockerfile`
ローカルのファイルを変更した際にサーバーを再起動`--reload`
```dockerfile
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --reload main:app
```

### コンテナ起動

```bash
$ docker-compose up --build
```

### メッセージを送信

```bash
$ curl -X POST http://localhost:8080/ \
    -H "Content-Type: application/json" \
    -d '{"message": {"data": "SGVsbG8gd29ybGQ="}}'
```

`data`の値はエンコードした値にする必要がある
```bash
echo -n 'Hello World!' | base64
SGVsbG8gV29ybGQh

'{"message": {"data": "SGVsbG8gV29ybGQh}}'
```

python側でデコード
```python
if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
```

## CloudRun ServiceとFireStore接続

## FireStore作成
 name : `cloudrun-test`

## CloudRun Serviceのでデプロイ

### コンテナビルドとpush

```bash
$ cd service/
```

```bash
$ gcloud builds submit --tag asia-northeast1-docker.pkg.dev/python-cloudrun-435707/firebase-cloudrun-20240917/firebase-servise:stg
```

## デプロイ

```bash
gcloud run deploy firebase-cloudrun-20240917 --image asia-northeast1-docker.pkg.dev/python-cloudrun-435707/firebase-cloudrun-20240917/firebase-servise:stg  --no-allow-unauthenticated
Deploying container to Cloud Run service [firebase-cloudrun-20240917] in project [python-cloudrun-435707] region [asia-northeast1]
✓ Deploying new service... Done.
  ✓ Creating Revision...
  ✓ Routing traffic...
Done.
Service [firebase-cloudrun-20240917] revision [firebase-cloudrun-20240917-00001-jfk] has been deployed and is serving 100 percent of traffic.
Service URL: https://firebase-cloudrun-20240917-powbfkvb6a-an.a.run.app
```

## pubsub作る

### Topic作る
```bash
$ gcloud pubsub topics create firebase-cloudrun-topic-20240917
```

### Subscriptionu作る

pubsubサービスカウント作成と認証トークン作成許可が別途必要

#### cloudrungを外部から呼び出し可能にする
```bash
$ gcloud run services add-iam-policy-binding firebase-cloudrun-20240917 \
--member=serviceAccount:cloud-run-pubsub-invoker@python-cloudrun-435707.iam.gserviceaccount.com \
--role=roles/run.invoker
```

#### Subscription作成
```bash
$ gcloud pubsub subscriptions create firebase-cloudrun-subscription-20240917 --topic firebase-cloudrun-topic-20240917 \
--ack-deadline=600 \
--push-endpoint=https://firebase-cloudrun-20240917-powbfkvb6a-an.a.run.app \
--push-auth-service-account=cloud-run-pubsub-invoker@python-cloudrun-435707.iam.gserviceaccount.com
```

## データ送信

```bash
$ gcloud pubsub topics publish firebase-cloudrun-topic-20240917 --message "Runner"
```

# FireStoreと統合していく

## "統合"の作成

下記エラー

```bash
$ gcloud beta run integrations create \
--type=firestore \
--service=firebase-cloudrun-20240917 \
--region asia-northeast1
The following APIs are not enabled on project [python-cloudrun-435707]:
        runapps.googleapis.com

Do you want to enable these APIs to continue (this will take a few minutes)? (y/N)?  y

Enabling APIs on project [python-cloudrun-435707]...
Operation "operations/acat.p2-276838580752-67fa97dd-fbe9-48ab-90ee-76e1564cde82" finished successfully.
X Creating new Integration... Deployment started. This process will continue even if your terminal session is interrupted.
  ✓ Saving Configuration for Integration... You can check the status with `gcloud beta run integrations describe firestore-a281`
  X Configuring Integration... This might take up to 5 minutes.
  ✓ Configuring Firestore...
  . Configuring Cloud Run Service...
Failed to create new integration.
  To retry the deployment, use update command `gcloud beta run integrations update firestore-a281`
ERROR: (gcloud.beta.run.integrations.create) Configuration failed with error:
  build "projects/276838580752/locations/asia-northeast1/builds/386a5e59-56b7-44d3-b646-f7133b5f05db" failed: Resource [firestore-a281] failed with error: Error creating Database: googleapi: Error 403: The caller does not have permission
Logs are available at https://console.cloud.google.com/cloud-build/builds;region=asia-northeast1/386a5e59-56b7-44d3-b646-f7133b5f05db?project=276838580752
```

CloudRunコンソール　 Integrations確認

```bash
 Failed: Latest deployment failed: Error creating Database: googleapi: Error 403: The caller does not have permission
```

以下権限追加
<img width="801" alt="スクリーンショット 2024-09-18 0 04 32" src="https://github.com/user-attachments/assets/55868b08-961a-4cc3-ad2c-c565d38186b5">


```bash
Failed to create new integration.
ERROR: (gcloud.beta.run.integrations.create) INVALID_ARGUMENT: The request was invalid: Invalid Config: service allows 1 binding(s), not 2
```

失敗した統合削除後

`gcloud beta run integrations create`にて完了


## warning `"The request was not authenticated. Either allow unauthenticated invocations or set the proper Authorization header. Read more at https://cloud.google.com/run/docs/securing/authenticating Additional troubleshooting documentation can be found at: https://cloud.google.com/run/docs/troubleshooting#unauthorized-client"`

CloudRun作成毎に書きコマンドの実行が必要

```bash
$ gcloud run services add-iam-policy-binding {CloudRun名} \
--member=serviceAccount:cloud-run-pubsub-invoker@python-cloudrun-435707.iam.gserviceaccount.com \
--role=roles/run.invoker
```


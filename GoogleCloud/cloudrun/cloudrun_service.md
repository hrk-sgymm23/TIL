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

## FireStoreとの接続
新しいcloudRunで統合を作成の際エラー

```bash
gcloud beta run integrations create \
--type=firestore \
--service=firebase-cloudrun-20240918 \
--region asia-northeast1 \
--service-account=276838580752-compute@developer.gserviceaccount.com
X Creating new Integration... Deployment started. This process will continue even if your terminal session is interrupted.
  ✓ Saving Configuration for Integration... You can check the status with `gcloud beta run integrations describe firestore-b104`
  X Configuring Integration... This might take up to 5 minutes.
  ✓ Configuring Cloud Run Service...
  ✓ Configuring Firestore...
Failed to create new integration.
  To retry the deployment, use update command `gcloud beta run integrations update firestore-b104`
ERROR: (gcloud.beta.run.integrations.create) Configuration failed with error:
  build "projects/276838580752/locations/asia-northeast1/builds/f81f341a-5e24-401d-916e-0a100985a4e5" failed: Resource [firebase-cloudrun-20240918] failed with error: Request `Create IAM Members roles/datastore.user serviceAccount:276838580752-compute@developer.gserviceaccount.com for project "python-cloudrun-435707"` returned error: Error retrieving IAM policy for project "python-cloudrun-435707": googleapi: Error 403: Cloud Resource Manager API has not been used in project 276838580752 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=276838580752 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.
Logs are available at https://console.cloud.google.com/cloud-build/builds;region=asia-northeast1/f81f341a-5e24-401d-916e-0a100985a4e5?project=276838580752
```

`oogleapi: Error 403: Cloud Resource Manager API has not been used in project 276838580752 before or it is disabled.`
ResourceManagerAPIを有効化して再度実行

```bash
gcloud beta run integrations create \
--type=firestore \
--service=firebase-cloudrun-20240918 \
--region asia-northeast1 \
--service-account=276838580752-compute@developer.gserviceaccount.com
✓ Creating new Integration... Done.
  ✓ Saving Configuration for Integration... You can check the status with `gcloud beta run integrations describe firestore-e1aa`
  ✓ Configuring Integration...
  - Configuring Cloud Run Service...
  ✓ Configuring Firestore...
Done.

[firestore] integration [firestore-e1aa] has been created successfully.

To connect to the Firestore Database utilize the environment variables FIRESTORE_DB_NAME. These have been added to the Cloud Run service for you.
You can check the status with `gcloud beta run integrations describe firestore-e1aa`
```

## 追加コード
```python

import os
import google.cloud.firestore

dbname = os.environ['FIRESTORE_DB_NAME']
db = google.cloud.firestore.Client(database=dbname)
~
results = db.collection('human').stream()
data_list = [doc.to_dict() for doc in results]

print(data_list)

```

## PubSub Publishして確認
```bash
$ gcloud pubsub topics publish firebase-cloudrun-topic-20240917 --message "Runner"
```

```bash
[{'age': 88, 'name': 'Hiroshi'}]
```

## FireStoreの開発環境を考える

[Firebase Local Emulator Suiteの環境をDockerで用意する](https://zenn.dev/cbcloud_blog/articles/6256f1a3d05a18)

下記コマンドにて、ローカルの認証を通す。
```bash
$ docker-compose run --rm firebase firebase login --no-localhost
```

コンテナを実行した下際に以下エラー
```bash
$ Error: Extensions Emulator is running but Functions emulator is not. This should never happen.
```

GoogleCloudのプロジェクトとFirebaseを連携することでエラー回避

以下を実行し、fireStoreのDB名を作成したものを選択
```bash
$ docker compose run --rm firebase firebase init
```

```bash
$ docker-compose up

~
service-firebase-1    | i  firestore: Firestore Emulator logging to firestore-debug.log
service-firebase-1    | ✔  firestore: Firestore Emulator UI websocket is running on 9150.
service-firebase-1    | i  ui: Emulator UI logging to ui-debug.log
service-firebase-1    |
service-firebase-1    | ┌─────────────────────────────────────────────────────────────┐
service-firebase-1    | │ ✔  All emulators ready! It is now safe to connect your app. │
service-firebase-1    | │ i  View Emulator UI at http://127.0.0.1:4000/               │
service-firebase-1    | └─────────────────────────────────────────────────────────────┘
service-firebase-1    |
service-firebase-1    | ┌───────────┬──────────────┬─────────────────────────────────┐
service-firebase-1    | │ Emulator  │ Host:Port    │ View in Emulator UI             │
service-firebase-1    | ├───────────┼──────────────┼─────────────────────────────────┤
service-firebase-1    | │ Firestore │ 0.0.0.0:8181 │ http://127.0.0.1:4000/firestore │
service-firebase-1    | └───────────┴──────────────┴─────────────────────────────────┘
service-firebase-1    |   Emulator Hub running at 127.0.0.1:4400
service-firebase-1    |   Other reserved ports: 4500, 9150
service-firebase-1    |
service-firebase-1    | Issues? Report them at https://github.com/firebase/firebase-tools/issues and attach the *-debug.log files.
```

`http://127.0.0.1:4000/firestore/`にアクセス

## Pythonからエミュレーターにアクセス

```python
# 環境変数を設定

emulator_host = os.getenv('FIRESTORE_EMULATOR_HOST')
project = os.getenv('GCLOUD_PROJECT')

db = google.cloud.firestore.Client()
```

## コレクションを永続化したい


## サービス同士で接続できていない
`サービス名:port`で解決
```bash
services:
  pubsub-app:
    environment:
      - FIRESTORE_EMULATOR_HOST=firebase:8181
```

## 新しいディレクトリ構成で`run deploy`するとエラー

## ローカルとGCPでDockerfileを分ける
gcp用ビルド
```bash
$ gcloud auth login
$ gcloud config set project python-cloudrun-435707
$ docker build  -f ./docker/run/Dockerfile -t asia-northeast1-docker.pkg.dev/python-cloudrun-435707/firebase-cloudrun-20240917/firebase-servise:stg .
$ docker push asia-northeast1-docker.pkg.dev/python-cloudrun-435707/firebase-cloudrun-20240917/firebase-servise:stg
```

下記を参考にデプロイみなおし

https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/run/pubsub

## シン　prdビルド
```bash
$ cd service/run/prd
$ docker build --platform linux/amd64 -t asia-northeast1-docker.pkg.dev/python-cloudrun-435707/firebase-cloudrun-20240917/firebase-servise:latest -f Dockerfile ../../../
$ docker push asia-northeast1-docker.pkg.dev/python-cloudrun-435707/firebase-cloudrun-20240917/firebase-servise:latest
$ gcloud run deploy firebase-cloudrun-20240918 --image asia-northeast1-docker.pkg.dev/python-cloudrun-435707/firebase-cloudrun-20240917/firebase-servise:latest  --no-allow-unauthenticated
# テスト
$ gcloud pubsub topics publish firebase-cloudrun-topic-20240917 --message "Runner"
```

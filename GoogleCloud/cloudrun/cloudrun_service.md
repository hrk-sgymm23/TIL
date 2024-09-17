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



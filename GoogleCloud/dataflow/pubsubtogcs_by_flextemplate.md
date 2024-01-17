# 通常のテンプレーを試す
- [クイックスタート](https://cloud.google.com/pubsub/docs/stream-messages-dataflow?hl=ja#python_1)
- [公式リポジトリ](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/pubsub/streaming-analytics/PubSubToGCS.py)
- [作業リポジトリ]()
## dataflow実行
- 環境変数設定
```bash
BUCKET_NAME=pub_to_gcs_20240117
PROJECT_ID=$(gcloud config get-value project)
TOPIC_ID=pub_to_gcs_20240117
REGION=us-central1
SERVICE_ACCOUNT=775779819731-compute@developer.gserviceaccount.com
```

- 関連リソース作成
```bash
$ gsutil mb gs://$BUCKET_NAME
$ gcloud pubsub topics create $TOPIC_ID
```

### ローカルから実行できるようコンテナを用意
```bash
$ docker-compose build
$ docker-compose exec -it dataflow /bin/bash
```
↑gcloud認証をコンテナ内で通す必要があり一旦保留

### python仮想環境の作成
```bash
$ python3 -m venv env
$ source env/bin/activate
# 仮想環境内にapache-beam インストール
$ pip install apache-beam
# 仮想環境から抜ける
$ deactivate
```

- dataflow job実行
```bash

```


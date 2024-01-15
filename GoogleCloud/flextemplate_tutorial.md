## FlexTemplate　Tutorial

### プロジェクト設定
```bash
$ gcloud projects create data-process-sample
$ gcloud config set project data-process-sample
```

### ローカル認証情報の設定
```bash
$ gcloud auth application-default login
```
### アカウントにロール付与
```bash
$ gcloud projects add-iam-policy-binding data-process-sample \
  --member="user:sandboxgcloud208@gmail.com" \
  --role=roles/iam.serviceAccountUser

Updated IAM policy for project [data-process-test].
bindings:
- members:
  - user:sandboxgcloud208@gmail.com
  role: roles/iam.serviceAccountUser
- members:
  - user:sandboxgcloud208@gmail.com
  role: roles/owner
etag: BwYO_JWKpDA=
version: 1
```

## トラブルシュート
- なぜかAPIを有効化できなかった→支払い情報を確認　https://cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=ja#console

### 必要なロール`roles/dataflow.admin、roles/dataflow.worker、roles/bigquery.dataEditor、roles/pubsub.editor、roles/storage.objectAdmin、roles/artifactregistry.reade`をアタッチ
```bash
$ gcloud projects add-iam-policy-binding resolute-winter-411303 --member="serviceAccount:775779819731-compute@developer.gserviceaccount.com" --role={ロール名}
```
## 関連リソース作成
###　バケット作成
```bash
$ gsutil mb gs://dataflow-sample-20230116
Creating gs://dataflow-sample-20230116/...
```
### pubsub作成
```
$ gcloud pubsub topics create topic-sample
$ gcloud pubsub subscriptions create --topic topic-sample subscription-sample
```
## BQ作成
### データセット
```bash
$ bq --location=asia-northeast1 mk \
  data-process-sample:data-set-sample-20240116
```
### テーブル
```bash
  bq mk \
      --table \
      data-process-sample:data_set_sample_20240116.teable_sample \
      url:STRING,review:STRING,last_date:TIMESTAMP,score:FLOAT,first_date:TIMESTAMP,num_reviews:INTEGER
```


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

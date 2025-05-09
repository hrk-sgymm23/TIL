# クイックスタートで作った向き先がEFSのものをS3へ変更する

## 改修が必要なもの
- yamlファイル
  - pvc
  - ジョブ
  - ジョブキュー
- IAMロール
  - EKSのサービスアカウント用

 ## yamlファイル
 
- `k8s/update-batch-job.yaml`
  - pvcマウント削除、環境変数追加

```
apiVersion: batch/v1
kind: Job
metadata:
  name: new-batch-job
  namespace: default
spec:
  template:
    spec:
      serviceAccountName: ecr-sa
      containers:
      - name: batch-processor
        image: xxx
      env:
        - name: AWS_REGION
          value: ap-northeast-1
```

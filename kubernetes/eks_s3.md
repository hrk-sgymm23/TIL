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

## やること

### クラスター作成

- 以下実行
```
$ eksctl create cluster -f cluster-config.yaml
```

### ポッド作成
- 以下実行

```
$ kubectl apply -f update-batch-job.yaml
$ kubectl apply -f update-batch-job-queue.yaml
```

### ジョブyaml修正

- `cronJob`作成
- https://kubernetes.io/ja/docs/concepts/workloads/controllers/cron-jobs/

```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: new-batch-job
  namespace: default
spec:
  schedule: "9 * * * *"
  jobTemplate:
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

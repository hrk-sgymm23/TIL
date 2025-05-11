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


### 設定したクロンジョブを確認
```
$ kubectl get cronjob new-batch-job

NAME            SCHEDULE     SUSPEND   ACTIVE   LAST SCHEDULE   AGE
new-batch-job   10 1 * * *   False     0        <none>          9m42s
```

### 実行ログの確認

```
$ kubectl create job --from=cronjob/new-batch-job test-job-now
job.batch/test-job-now created
$ kubectl get pods
NAME                 READY   STATUS   RESTARTS     AGE
test-job-now-hv87k   0/1     Error    1 (6s ago)   6s
$ kubectl logs test-job-now-hv87k
```

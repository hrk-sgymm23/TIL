# Amazon EKS の SQS と EFS 永続ストレージを使用した非同期タスクの管理

- クラスター構築
  - https://community.aws/content/2fK7oHTJNmSetxGPYg8FZQUCNME/navigating-amazon-eks-eks-cluster-batch-processing
- バッチアプリケーションのデプロイ
  - https://community.aws/content/2eBfaGM7T9C8M1dzoZBuRUfyMpr/navigating-amazon-eks-managing-high-volume-batch-sqs-eks
- 備考
  - EFSアクセスのロール作成
    - https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html#efs-create-iam-resources?sc_channel=el&sc_campaign=appswave&sc_geo=mult&sc_country=mult&sc_outcome=acq&sc_content=managing-high-volume-batch-sqs-eks
  - OIDCプロバイダ作成
    - https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html?sc_channel=el&sc_campaign=appswave&sc_geo=mult&sc_country=mult&sc_outcome=acq&sc_content=managing-high-volume-batch-sqs-eks

## クラスターの作成

- `k8s/cluster-config.yaml`作成
- 以下実行
```
$ eksctl create cluster -f cluster-config.yaml
```






## クリーンアップ

```
$ eksctl delete cluster -f ./cluster-config.yaml
```

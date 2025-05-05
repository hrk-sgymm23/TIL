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

- nodeを確認
```
$ kubectl get nodes
```

- eksのアドオンを確認
```
$ eksctl get addon --cluster async-batch-quickstart --region ap-northeast-1
```

- サービスアカウント確認
```
$ kubectl get sa -A
```

## アプリケーションデプロイ

- 環境変数確認
```
$ kubectl config current-context
$ eksctl get cluster --region ap-northeast-1 // クラスタ名確認

$ export CLUSTER_NAME=$(aws eks describe-cluster --region ap-northeast-1 --name async-batch-quickstart --query "cluster.name" --output text)
$ export CLUSTER_REGION=$(aws eks describe-cluster --name ${CLUSTER_NAME} --region ap-northeast-1 --query "cluster.arn" --output text | cut -d: -f4)
$ export ACCOUNT_ID=$(aws eks describe-cluster --name ${CLUSTER_NAME} --region ${CLUSTER_REGION} --query "cluster.arn" --output text | cut -d':' -f5)
```

- サービスアカウントまわり
```
$ kubectl get sa -A

// 下記が確認できる
default           ecr-sa                               0         31m
kube-system       efs-csi-controller-sa                0         30m
```

## EFS CSIドライバーアドオンの確認

```
$ eksctl get addon --cluster ${CLUSTER_NAME} --region ${CLUSTER_REGION}

# 下記が確認できる
aws-efs-csi-driver      v1.5.8-eksbuild.1       ACTIVE  0
```

## アプリケーションコードの実装

- `batch_processing.py`,`input.csv`を用意する

### コンテナイメージ作成
- ECR作成
- Makefile作成
```
IMAGE_NAME=batch-processing-repo
TAG=latest
REGION=ap-northeast-1
ECR_REPO_NAME=batch-processing-repo

build:
	docker build -f docker/Dockerfile -t $(IMAGE_NAME):$(TAG) .

run:
	docker run --rm -v $(PWD)/app/src:/batch $(IMAGE_NAME):$(TAG)

push:
	@ACCOUNT_ID=$$(aws sts get-caller-identity --query Account --output text); \
	docker tag $(ECR_REPO_NAME):latest $$ACCOUNT_ID.dkr.ecr.$(REGION).amazonaws.com/$(ECR_REPO_NAME):latest; \
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $$ACCOUNT_ID.dkr.ecr.$(REGION).amazonaws.com; \
	docker push $$ACCOUNT_ID.dkr.ecr.$(REGION).amazonaws.com/$(ECR_REPO_NAME):latest
```


## クリーンアップ

```
$ eksctl delete cluster -f ./cluster-config.yaml

# クラスタ起動
$ eksctl create cluster -f cluster-config.yaml
```

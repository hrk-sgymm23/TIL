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

## マルチアーキテクチャイメージ作成

- マルチアーキテクチャとは
  - > M1/M2 Mac でビルドした Docker イメージが、x86_64 環境（EC2, ECR, CIなど）で動かない問題を防ぐ
- ビルダーインスタンス作成
```
$ docker buildx create --name batchBuilder
$ docker buildx use batchBuilder
$ docker buildx inspect --bootstrap
```

## kubernetesジョブをデプロイする

- ECR URLを取得
```
$ echo ${ACCOUNT_ID}.dkr.ecr.${CLUSTER_REGION}.amazonaws.com/batch-processing-repo:latest
```
- `batch-job.yaml`を改修
  - 上記で得たURLを指定
- ジョブマニフェストを適用
```
$ kubectl apply -f batch-job.yaml
```
- ジョブの実行を確認
```
$ kubectl get jobs

NAME                      COMPLETIONS   DURATION   AGE
my-batch-processing-job   0/1           13s        13s
```

## SQS準備

- SQS作成
```
$ aws sqs create-queue --queue-name eks-batch-job-queue
}
    "QueueUrl": "https://sqs.ap-northeast-1.amazonaws.com/321699386584/eks-batch-job-queue"
}
```

- EKSのサービスアカウントへ権限付
```
$ eksctl create iamserviceaccount \
  --region ${CLUSTER_REGION} \
  --cluster async-batch-quickstart \
  --namespace default \
  --name ecr-sa \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess \
  --override-existing-serviceaccounts \
  --approve

Assume Role MFA token code: 
2025-05-06 18:45:40 [ℹ]  3 existing iamserviceaccount(s) (default/ecr-sa,kube-system/cluster-autoscaler,kube-system/efs-csi-controller-sa) will be excluded
2025-05-06 18:45:40 [ℹ]  1 iamserviceaccount (default/ecr-sa) was excluded (based on the include/exclude rules)
2025-05-06 18:45:40 [!]  metadata of serviceaccounts that exist in Kubernetes will be updated, as --override-existing-serviceaccounts was set
2025-05-06 18:45:40 [ℹ]  no tasks
```

## kubernetesシークレットの作成

- kubernetesクrスターがプライベートECRリポジトリから必要なコンテナイメージをぷるできるようにするためのもの

```
$ ECR_TOKEN=$(aws ecr get-login-password --region ${CLUSTER_REGION})
$ kubectl create secret docker-registry regcred \
  --docker-server=${ACCOUNT_ID}.dkr.ecr.${CLUSTER_REGION}.amazonaws.com \
  --docker-username=AWS \
  --docker-password="${ECR_TOKEN}" \
  -n default
```

## キュー統合を利用しkubernetesジョブをデプロイする

- `batch-job-queue.yaml`作成
- 上記適用
```
$ kubectl apply -f batch-job-queue.yaml
```

## EFSを作成する

https://community.aws/content/2iCiQb70sP9wWcOLgG67jLVqK53/navigating-amazon-eks-eks-with-efs-add-on

### EFSファイルシステムを作成する

- CIDR範囲を環境変数へ
```
$ export CIDR_RANGE=$(aws ec2 describe-vpcs \
    --vpc-ids $CLUSTER_VPC \
    --query "Vpcs[].CidrBlock" \
    --output text \
    --region $CLUSTER_REGION)
```

- クラスターを配置するVPCを環境変数へ設定
```
$ export CLUSTER_VPC=$(aws eks describe-cluster --name ${CLUSTER_NAME} --region ${CLUSTER_REGION} --query "cluster.resourcesVpcConfig.vpcId" --output text)
```

- セキュリティグループ作成

```
$ export SECURITY_GROUP_ID=$(aws ec2 create-security-group \
    --group-name MyEfsSecurityGroup \
    --description "My EFS security group" \
    --vpc-id $CLUSTER_VPC \
    --region $CLUSTER_REGION \
    --output text)
```

```
# CIDR範囲が正しくなかったため修正
$ export CIDR_RANGE="192.168.0.0/16"
$ aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 2049 \
    --cidr $CIDR_RANGE \
    --region $CLUSTER_REGION
```

- EKS自体を作成

```
export FILE_SYSTEM_ID=$(aws efs create-file-system \
--region $CLUSTER_REGION \
--performance-mode generalPurpose \
--query 'FileSystemId' \
--output text)
```

## EFSファイルシステムのマウントターゲットを構成する


- サブネットが所属するVPCの特定

```
$ aws ec2 describe-subnets \ 
    --filters "Name=vpc-id,Values=$CLUSTER_VPC" \ 
    --region $CLUSTER_REGION \ 
    --query 'Subnets[*].{SubnetId: SubnetId,AvailabilityZone: AvailabilityZone,CidrBlock: CidrBlock}' \ 
    --output table

|                          DescribeSubnets                          |
+------------------+-------------------+----------------------------+
| AvailabilityZone |     CidrBlock     |         SubnetId           |
+------------------+-------------------+----------------------------+
|  ap-northeast-1c |  192.168.32.0/19  |  subnet-07b2e35aba1068ca0  |
|  ap-northeast-1a |  192.168.0.0/19   |  subnet-0f5e821d4cbc9c100  |
|  ap-northeast-1a |  192.168.64.0/19  |  subnet-08e79bcb3ec95bbf5  |
|  ap-northeast-1c |  192.168.96.0/19  |  subnet-052ef1403c24b9472  |
+------------------+-------------------+----------------------------+
```

### ノードをホストするマウントターゲットを追加

- 上記サブネット分実行

```
$ aws efs create-mount-target \
    --file-system-id $FILE_SYSTEM_ID \
    --subnet-id subnet-xxx \
    --security-groups $SECURITY_GROUP_ID \
    --region $CLUSTER_REGION
```


## EFSのPersistentVolumeとPersistentVolumeClaimを作成する

- EFS URLを取得
```
$ echo $FILE_SYSTEM_ID.efs.$CLUSTER_REGION.amazonaws.com
```

- `batch-pv-pvc.yaml`作成
- 上記適用
```
$ kubectl apply -f batch-pv-pvc.yaml
persistentvolume/efs-pv created
persistentvolumeclaim/efs-claim created
```

## EFSでストレージを永続化する

- `update-batch-job.yaml`作成
- 上記適用
```
$ kubectl apply -f update-batch-job.yaml

job.batch/new-batch-job created
```

- `update-batch-job-queue.yaml`作成
- 上記適用
```
$ kubectl apply -f update-batch-job-queue.yaml

job.batch/new-batch-processing-job-queue created
```

- 上記ログ確認の際EFSのパスがおかしくpv,pvcを作成し直す必要があったその際に実行したコマンドが以下

```
$ kubectl patch pv efs-pv --type=json -p='[{"op": "remove", "path": "/spec/claimRef"}]'
$ kubectl patch pvc efs-claim -p '{"metadata":{"finalizers":null}}'
```

- さいどpv, pvc作成

```
$ kubectl apply -f batch-pv-pvc.yaml
```

### 実行結果確認

- ポッド名取得

```
$ kubectl get pods --selector=job-name=new-batch-job -o wide
```

- ポッドの実行詳細確認

```
$ kubectl describe pod new-batch-job-94bfc
$ kubectl logs new-batch-job-94bfc -c batch-processor

Starting batch task...
Batch task completed.
```

## クリーンアップ

- EKSクラスター削除
```
$ eksctl delete cluster -f ./cluster-config.yaml

# クラスタ起動
$ eksctl create cluster -f cluster-config.yaml
```

- ECR, SQS削除
```
$ aws sqs delete-queue --queue-url YOUR_SQS_QUEUE_URL
$ aws ecr delete-repository --repository-name YOUR_ECR_REPO_NAME --force
```

## 必要なリソース群

- VPC
- subnet
  - for ECS
  - for ALB
  - for RDS
- SecurityGroup
  - for ECS
  - for ALB
  - for RDS


## パブリックサブネットとプライベートサブネット間の通信について

https://qiita.com/hatsu/items/8b30e68ba7252a749fe7#modulessubnet

上記記事ではNATGateWayを使っているがコスト面で懸念→vpcエンドポイントを使う

https://dev.classmethod.jp/articles/privatesubnet_ecs/

# ECS作成

## `aws_caller_identity`について
[*.tf 内で AWS アカウント ID を自動参照(取得)する aws_caller_identity Data Source](https://qiita.com/gongo/items/a2b83d7402b97ef43574)

> ハードコーディングで構わないと思いつつも、どうにかいい感じに Terraform が AWS アカウント ID を取得してくれないかなーという願いを叶えるために、 Terraform version 0.7.1 から aws_caller_identity が実装されました。

# `CloudWatch Container Insights`について
- [Container Insights を使用して Amazon ECS コンテナをモニタリングする](https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/cloudwatch-container-insights.html)
- [Amazon ECS Container Insights メトリクス](https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/monitoring/Container-Insights-metrics-ECS.html)
- [ECS で Container Insights を使ってみた](https://qiita.com/sugimount-a/items/7c62582972a80deccd7d)

> Container Insights では、コンテナ化されたバージョンの CloudWatch エージェントを使用してクラスターで実行中のすべてのコンテナを検出し、パフォーマンススタックのすべてのレイヤーでパフォーマンスデータを収集します。運用データは、パフォーマンスログイベントとして収集されます。これらは、高濃度データを大規模に取り込み、保存できる、構造化された JSON スキーマを使用するエントリです。CloudWatch はこのデータから、クラスター、サービスおよびサービスレベルで、高レベルの集約されたメトリクスを CloudWatch メトリクスとして作成します。このメトリクスには、CPU、メモリ、ディスク、ネットワークなどのリソース使用率が含まれます。メトリクスは、CloudWatch 自動ダッシュボードで使用できます。

# ECSのネットワークモードについて
[https://zenn.dev/fdnsy/articles/43b7f4d745ed1f](https://zenn.dev/fdnsy/articles/43b7f4d745ed1f)

> ECSの起動タイプは2つの選択肢があります。
サーバレス型の「Fargate」
ホスト型の「EC2」

Fargateのネットワークモードはawsvpcのみなので、今回はあまり関係ありません。
EC2を選択した場合に複数の選択肢があるため、今回はこちらのネットワークモードが中心です。
<img width="891" alt="スクリーンショット 2024-05-17 14 55 58" src="https://github.com/hrk-sgymm23/TIL/assets/78539910/a02b68f1-fcf7-43a3-b0f3-f0f4aa472ec3">

# `PassRole`について
[IAMのPassRoleとセキュリティの話](https://qiita.com/koheiawa/items/044a1ccf08482287da16)
> IAMのPassRoleは、IAMポリシーの記述の中で iam:PassRole と表現するアクセス許可です。これは ポリシーがアタッチされているプリンシパル(IAMユーザとIAMロール) が、 AWSのサービス(EC2やLambdaなど) にロールを渡すことを意味しています。これにより、例えばEC2がS3のファイルを読み取れたり、LambdaがDynamoDBにデータを格納することができるようになります。

# 次作業
- ECSモジュールよりタスク実行ロールとしてIAMモジュールを参照
- ECSモジュール作成

# タスク定義を書く
[ECSタスク定義をコンソールから作って後悔した後、コード管理するため最速でJSON登録可能にする超愚直な方法](https://dev.classmethod.jp/articles/ecs-task-definition-to-json/)

> ECSタスク定義で利用できるJSONを作る方法
> 元ネタのJSONを取得する
> 最初に編集するための元ネタとなるJSONを取得します。今回のJSONはマネジメントコンソールにのみ表示されているので、ものすごい愚直な方法でとってきますYO
> マネジメントコンソールのECSタスク定義メニューから該当のタスク定義を開きます。ここで[Create new revision]をクリック。

## `apply`の際のエラー解決
```bash
│ Error: Unsupported attribute
│
│   on ecs.tf line 7, in module "ecs_stg":
│    7:   target_group_arn          = module.alb_stg.target_group_arn
│     ├────────────────
│     │ module.alb_stg is a object
│
│ This object does not have an attribute named "target_group_arn".
```

↑ALBのモジュールのoutputが空だった。

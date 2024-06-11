# RDSの無料利用枠について
[RDS 公式　Q&A](https://aws.amazon.com/jp/rds/faqs/#:~:text=%E7%84%A1%E6%96%99%E5%88%A9%E7%94%A8%E6%9E%A0%E3%81%AF%E3%80%811,%E3%81%A7%E3%81%94%E5%88%A9%E7%94%A8%E3%81%84%E3%81%9F%E3%81%A0%E3%81%91%E3%81%BE%E3%81%99%E3%80%82)

## 無料利用可能なエンジン
- MySQL
- Posgrate
- MariaDB

## 無料利用可能な時間
- 月間750インスタンス時間の使用
  - つまり、2インスタンスで400時間稼働させると400*2=800
  - 800-750=50時間の料金が請求される

## インスタンスタイプ
- `db.t2.micro`または`db.t3.micro`

## ストレージ
- 20GB

## バックアップストレージ
- 20GB

# ASSのRDSのTerraformの設定を見てゆく
```terraform
resource "aws_db_instance" "main" {
  identifier                      = "${var.common_name}-${var.enviroment}"
  db_name                         = replace(var.db_name, "-", "_")
  instance_class                  = var.db_instance_class
  engine                          = var.engine
  engine_version                  = var.engine_version
  allocated_storage               = 20
  max_allocated_storage           = 20
  storage_type                    = "gp2"
  storage_encrypted               = true
  username                        = replace(var.db_user_name, "-", "_")
  password                        = random_password.rds.result
  multi_az                        = var.multi_az
  publicly_accessible             = false
  backup_window                   = "09:10-09:40"
  backup_retention_period         = 7
  maintenance_window              = "mon:10:10-mon:10:40"
  auto_minor_version_upgrade      = true
  deletion_protection             = false
  skip_final_snapshot             = false
  final_snapshot_identifier       = "${var.common_name}-snapshot-${var.enviroment}"
  port                            = var.port
  apply_immediately               = false
  vpc_security_group_ids          = [module.rds_security_group.security_group_id]
  parameter_group_name            = aws_db_parameter_group.main.name
  option_group_name               = aws_db_option_group.main.name
  db_subnet_group_name            = aws_db_subnet_group.main.name
  enabled_cloudwatch_logs_exports = var.enabled_cloudwatch_logs_exports
  lifecycle {
    ignore_changes = [password]
  }
  # monitoring_interval = 60
  # monitoring_role_arn = 
}
```

## ASSの設定において、、、
- 今回はインスタンスをマルチAZにする関係でインスタンスは2個立ち上がることになる。
- 2インスタンスで月間の起動時間が750時間に収まるようにする

1インスタンスあたり月間375時間→375時間を31日(月)で割る→12.096...
12時間起動だと少しオーバーする可能性があるため、11時間起動とする。その場合11*31=341*2=６８２時間に収まる

### 11:00AM~10:00PMの起動時間は有用か、、、

##EventBridgeSchedulerで実装する
- https://envader.plus/article/250
- https://dev.classmethod.jp/articles/amazon-eventbridge-scheduler-rds-stop/

#　スケジューラーが機能していない問題

## SDKを正しいものを選んでいなかった
下記のように
`arn:aws:scheduler:::aws-sdk:rds:stopDBInstance`の`stopDBInstance`が`stopDBCluster`になっていた
下記のようにコンソールから対象のリソースの設定名を確認する
<img width="1440" alt="スクリーンショット 2024-06-12 0 02 36" src="https://github.com/hrk-sgymm23/TIL/assets/78539910/c5edd7d7-d7a5-4018-afbb-eca75e154301">


```terraform
resource "aws_scheduler_schedule" "rds_stop_stg" {
  name                = "${var.common_name}-stop-scheduler-${var.enviroment}"
  schedule_expression = local.stop_rds_schedule
  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:rds:stopDBInstance"
    role_arn = aws_iam_role.rds_scheduler_stg.arn
    input = jsonencode({
      DbInstanceIdentifier = aws_db_instance.main.identifier
    })
  }
}
```

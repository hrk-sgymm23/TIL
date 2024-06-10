# RDS作成

# `aws_db_instance`作成

## `replace`関数について
[replace Function](https://developer.hashicorp.com/terraform/language/functions/replace)

### 第二引数で指定した値を第３引数に変更する
```bash
> replace("1 + 2 + 3", "+", "-")
1 - 2 - 3

> replace("hello world", "/w.*d/", "everybody")
hello everybody
```

# `terraform plan`の際にwarning
```bash
User
│ Warning: Deprecated attribute
│
│   on ../../../modules/rds/main.tf line 113, in resource "aws_ssm_parameter" "db_name":
│  113:   value       = aws_db_instance.main.name
│
│ The attribute "name" is deprecated. Refer to the provider documentation for details.
```

> この警告は、aws_db_instance.main.name属性が非推奨であることを示しています。代わりに、新しい属性を使用する必要があります。おそらく、DBインスタンスの識別子（identifier）を参照することが意図されています。

```terraform
resource "aws_ssm_parameter" "db_name" {
  name        = "/${var.common_name}-${var.enviroment}/db/name"
  type        = "SecureString"
  # nameは非推奨のためidentifierを参照するように変更
  value       = aws_db_instance.main.identifier
  description = "DBName"
  lifecycle {
    ignore_changes = [value]
  }
}
```

# EventBridgeSchedulerの実装

[TerraformとEventBridge Schedulerを活用したEC2インスタンスの時限起動によるコスト削減](https://envader.plus/article/250)
[AWS EventBridgeスケジューラで圧倒的コスト削減に成功した話](https://qiita.com/Nightley_dev/items/54ce272509f2a9a48b30#rds)

上記を参考に実装

```terraform
locals {
  stop_rds_schedule  = "cron(0 13 * * ? *)" // 22:00 JST
  start_rds_schedule = "cron(0 2 * * ? *)"  // 08:00 JST
}

# Stop RDS
resource "aws_scheduler_schedule" "rds_stop_stg" {
  name                = "${var.common_name}-stop-scheduler-${var.enviroment}"
  schedule_expression = local.stop_rds_schedule
  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:rds:stopDBCluster"
    role_arn = aws_iam_role.rds_scheduler_stg.arn
    input = jsonencode({
      DbClusterIdentifier = aws_db_instance.main.identifier
    })
  }
}
```


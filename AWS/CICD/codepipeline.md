# Codepipeline作成

# やること
- GithubActionsにて作成したコンテナイメージがECRに格納されることを起点にCodepipelineを起動し、DBマイグレーション、ECSサービスの更新まで行う。

# 参考
- [ECS用のCDパイプラインに対する考察](https://zenn.dev/reireias/articles/8e987af2762eaa#%E8%B6%A3%E6%97%A8)
  - 様々な種類の構成のパイプラインが載っている
  - 「3. Image BuildのみGitHub Actionsでやる」がやりたいイメージ

#　各Code~の仕組みについて理解する

# CodeBuild

## アーティファクトについて理解する

# CodePipelineの流れ

1. GithubActionsよりECRへコンテナイメージがpushされる
2. 前項にてpushされたイメージを検知し、CodeBuildが発火
3. CodeBuildにてECRからpushされたイメージをもとに
  - DBマイグレーション
  - S3からappspecとタスク定義を取得しアーティファクト化(後続の処理へ渡すための処理)
  - CodeDeployにてECSサービスを更新


# CodeBuild作成時の課題

## S3から取得するタスク定義にてタスク定義のリビジョンを動的にしたい
- [【ECS Blue/Greenデプロイ】１タスクで複数コンテナ稼働している場合のCI/CDパイプライン構築](https://qiita.com/tarian/items/5043abe44345d448e7dc)

タスク定義.json
```json
{
    "taskDefinitionArn": "arn:aws:ecs:ap-northeast-1:730335441282:task-definition/ass-task-def-staging:52",
    "containerDefinitions": [
        {
            "name": "rails",
            "image": "730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/ass-rails-ecr-staging:stg",
            "cpu": 0,
            "memoryReservation": 512,
            "portMappings": [
                {
                    "containerPort": 3000,
                    "hostPort": 3000,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "entryPoint": [
                "/usr/bin/entrypoint.sh"
            ],
            "command": [
                "sh",
                "-c",
                "bundle exec puma -C config/puma.rb"
            ],
            "environment": [
                {
                    "name": "RAILS_LOG_TO_STDOUT",
                    "value": "true"
                },
                {
                    "name": "RAILS_ENV",
                    "value": "staging"
                },
                {
                    "name": "RAILS_SERVE_STATIC_FILES",
                    "value": "true"
                }
            ],
            "mountPoints": [
                {
                    "sourceVolume": "sockets",
                    "containerPath": "/app/tmp/sockets"
                }
            ],
            "volumesFrom": [],
            "secrets": [
                {
                    "name": "DB_HOST",
                    "valueFrom": "/ass-staging/db/host"
                },
                {
                    "name": "DB_PASSWORD",
                    "valueFrom": "/ass-staging/db/password"
                },
                {
                    "name": "DB_USERNAME",
                    "valueFrom": "/ass-staging/db/username"
                },
                {
                    "name": "RAILS_MASTER_KEY",
                    "valueFrom": "/ass-staging/rails-master-key"
                },
                {
                    "name": "DB_ENDPOINT",
                    "valueFrom": "/ass-staging/db/endpoint"
                },
                {
                    "name": "DB_NAME",
                    "valueFrom": "/ass-staging/db/name"
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/ass-staging",
                    "awslogs-create-group": "true",
                    "awslogs-region": "ap-northeast-1",
                    "awslogs-stream-prefix": "ecs/ass-staging"
                }
            },
            "healthCheck": {
                "command": [
                    "CMD-SHELL",
                    "curl localhost:3000/api/v1/health_check",
                    "\"|| exit 1\""
                ],
                "interval": 300,
                "timeout": 60,
                "retries": 10,
                "startPeriod": 300
            },
            "systemControls": []
        },
        {
            "name": "nginx",
            "image": "730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/ass-nginx-ecr-staging:stg",
            "cpu": 0,
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 80,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "environment": [],
            "mountPoints": [
                {
                    "sourceVolume": "sockets",
                    "containerPath": "/app/tmp/sockets"
                }
            ],
            "volumesFrom": [],
            "dependsOn": [
                {
                    "containerName": "rails",
                    "condition": "HEALTHY"
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/ass-staging",
                    "awslogs-region": "ap-northeast-1",
                    "awslogs-stream-prefix": "ecs/ass-staging"
                }
            },
            "healthCheck": {
                "command": [
                    "CMD-SHELL",
                    "curl localhost:3000/api/v1/health_check",
                    "\"|| exit 1\""
                ],
                "interval": 300,
                "timeout": 60,
                "retries": 10,
                "startPeriod": 300
            },
            "systemControls": []
        }
    ],
    "family": "ass-task-def-staging",
    "taskRoleArn": "arn:aws:iam::730335441282:role/ass-ecs-task-execution",
    "executionRoleArn": "arn:aws:iam::730335441282:role/ass-ecs-task-execution",
    "networkMode": "awsvpc",
    "revision": 52,
    "volumes": [
        {
            "name": "sockets",
            "host": {}
        }
    ],
    "status": "ACTIVE",
    "requiresAttributes": [
        {
            "name": "ecs.capability.execution-role-awslogs"
        },
        {
            "name": "com.amazonaws.ecs.capability.ecr-auth"
        },
        {
            "name": "com.amazonaws.ecs.capability.docker-remote-api.1.21"
        },
        {
            "name": "com.amazonaws.ecs.capability.task-iam-role"
        },
        {
            "name": "ecs.capability.container-health-check"
        },
        {
            "name": "ecs.capability.execution-role-ecr-pull"
        },
        {
            "name": "ecs.capability.secrets.ssm.environment-variables"
        },
        {
            "name": "com.amazonaws.ecs.capability.docker-remote-api.1.18"
        },
        {
            "name": "ecs.capability.task-eni"
        },
        {
            "name": "com.amazonaws.ecs.capability.docker-remote-api.1.29"
        },
        {
            "name": "com.amazonaws.ecs.capability.logging-driver.awslogs"
        },
        {
            "name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"
        },
        {
            "name": "ecs.capability.container-ordering"
        }
    ],
    "placementConstraints": [],
    "compatibilities": [
        "EC2",
        "FARGATE"
    ],
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "256",
    "memory": "512",
    "registeredAt": "2024-08-18T12:50:14.296Z",
    "registeredBy": "arn:aws:iam::730335441282:root",
    "tags": []
}
```

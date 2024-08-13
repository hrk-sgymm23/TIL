# S3へのアップロード、ECRへのコンテナイメージpush

## 参考

https://zenn.dev/kou_pg_0131/articles/gh-actions-oidc-aws

## ロールの作成

- 信頼されたエンティティ...`カスタム信頼ポリシー`

`カスタム信頼ポリシー`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::730335441282:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                    "token.actions.githubusercontent.com:sub": "repo:hrk-sgymm23/AwsomeStudySpaces:ref:refs/heads/main"
                }
            }
        }
    ]
}
```


## ロールにポリシーを追加

- `AmazonEC2ContainerRegistryPowerUser`
- `AmazonS3FullAccess`

## GithubActionsを作成
`s3`
```yml

name: Deploy React App

on:
  push:
    branches:
      - main

jobs:
    deploy:
        runs-on: ubuntu-latest
        permissions:
            id-token: write
            contents: read
        steps:
            - name: Checkout
              uses: actions/checkout@v3
            
            - uses: aws-actions/configure-aws-credentials@v1
              with:
                aws-region: ap-northeast-1
                role-to-assume: 'arn:aws:iam::730335441282:role/GithubActionsRoleforASS'

            - name: Set up Node.js
              uses: actions/setup-node@v3
              with:
                  node-version: '16.15.1'
            
            - name: Install modules
              run: npm ci
              working-directory: ./frontend/app
            
            - name: Build application
              run: npm run build
              working-directory: ./frontend/app
            
            - name: Deploy to S3
              run: aws s3 sync --delete ./build/ s3://${{ secrets.BUCKET_ID }} --region ap-northeast-1
              working-directory: ./frontend/app
     

```

`ecr`
```yml

name: Push ECR for Rails and Nginx

on:
  push:
    branches:
      - main

jobs:
    PushRailstoECR:
        runs-on: ubuntu-latest
        permissions:
            id-token: write
            contents: read

        steps:
            - name: Checkout
              uses: actions/checkout@v3 
            
            - uses: aws-actions/configure-aws-credentials@v1
              with:
                aws-region: ap-northeast-1
                role-to-assume: 'arn:aws:iam::730335441282:role/GithubActionsRoleforASS'

            - name: Login ECR
              run: |
                aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${{ secrets.AWS_ECR_ENDPOINT }}

            - name: Image Build & Push to Rails ECR
              env:
                RAILS_REPOSITORY: "ass-rails-ecr-staging"
                IMAGE_TAG: stg
              run: |
                docker build --no-cache -f ./docker/staging/Dockerfile --platform linux/amd64  -t ${{ env.RAILS_REPOSITORY }} .
                docker tag ${{ env.RAILS_REPOSITORY }}:latest 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/${{ env.RAILS_REPOSITORY }}:${{ env.IMAGE_TAG }}
                docker push 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/${{ env.RAILS_REPOSITORY }}:${{ env.IMAGE_TAG }}
              working-directory: ./backend

            - name: Image Build & Push to Nginx ECR
              env:
                NGINX_REPOSITORY: "ass-nginx-ecr-staging"
                IMAGE_TAG: stg
              run: |
                docker build --no-cache --platform linux/amd64 -t ${{ env.NGINX_REPOSITORY }} .
                docker tag ${{ env.NGINX_REPOSITORY }}:latest 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/${{ env.NGINX_REPOSITORY }}:${{ env.IMAGE_TAG }}
                docker push 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/${{ env.NGINX_REPOSITORY }}:${{ env.IMAGE_TAG }}
              working-directory: ./nginx

```

## `Error: Credentials could not be loaded, please check your action inputs: Could not load credentials from any providers`

`permittion`を追加することで解決

```yml
jobs:
    deploy:
        runs-on: ubuntu-latest
        permissions:
            id-token: write
            contents: read
```

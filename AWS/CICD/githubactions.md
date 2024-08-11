# ASSのCICDを作る

## イメージ

![image](https://github.com/user-attachments/assets/8db729ac-cb74-4979-a6c6-4becb06c8237)


## GithubActionsとCodePipelineの使いわけ

### GithubActions

#### `main`へのマージ時
- Reactのビルドと生成されたファイルのアップロード
- Railsのコンテナイメージのビルド、タグ付け、ECRへのpush

#### リモートへのpush時
- `npm ci`により依存関係の整理
- `npm run format:check`によるフォーマット

#### 参考
- [【GitHub Actions】ReactプロジェクトのCI/CDパイプラインを構築してみた](https://qiita.com/suzuki0430/items/de0cc70f0b9d2b1ad00b)
  - feature -> develop, develop -> mainへのワークフローが記載されてる

### CodePipeline

- ECRへのイメージのpushをトリガーとしてパイプラインを実行

## まずやること

コードフォーマットを実現するため`pretter`をインストールする

```bash
$ npm i -D  prettier
```

`.prettierrc`
```
.prettierrc
node_modules
```

```bash
$ npx prettier . --write
```

`package.json/scripts`追加
```json
"format": "npx prettier . --write"
```

## 次やること
(RailsプロジェクトにGitHub Actionsを導入する方法（Rspec, Rubocop）)[https://qiita.com/JZ8xNeXY/items/fef7efb5eb9495b62faf]
- Railsのフォーマットとテスト追加
- リモートpush時のgithub actions作成

## RubyCopo導入

`Gemfile`
```
development do
~
  gem 'rubocop', require: false
  gem 'rubocop-performance', require: false
  gem 'rubocop-rails', require: false
  gem 'rubocop-rspec', require: false
~
end
```

```bash
$ bundle install
```

`.rubocop_todo.yml.`作成
```bash
$ bundle exec rubocop --auto-gen-config
```

違反箇所確認
```bash
$ bundle exec rubocop
```

違反箇所修正
```bash
$ bundle exec rubocop --auto-correct
```

## GithhubActios WorkFlow追加

`.github/workflows/static_analytics`

```yml
name: Static Analytics

on:
    push:

jobs:
    rspec:
        runs-on: ubuntu-latest
        defaults:
            run:
                working-directory: .
        services:
            mysql:
                image: mysql:latest
                ports:
                    - 3306:3306
                env:
                    MYSQL_ALLOW_EMPTY_PASSWORD: yes

        steps:
            - name: Checkout Code
              uses: actions/checkout@v2

            - name: SetUp Ruby
              uses: ruby/setup-ruby@v1
              with:
                ruby-version: 3.2.2
                bundler-cache: true

            - name: Cache NodeModules
              uses: actions/cache@v3
              with:
                path: ./frontend/app/node_modules
                key: ${{ runner.os }}-node-${{ hashFiles('**/yarn.lock') }} # キャッシュのキーを指定します。
                restore-keys: |
                    ${{ runner.os }}-node-

            - name: Bundler and Gem install
              run: |
                gem install bundler
                bundle install
              working-directory: ./backend/app

            - name: Database craete and Migration
              run: |
                bundle exec rails db:create RAILS_ENV=test
                bundle exec rails db:migrate RAILS_ENV=test
              working-directory: ./backend/app

            - name: Exec RSpec
              run: bundle exec rspec
              working-directory: ./backend/app

    rubocop:
        runs-on: ubuntu-latest
        defaults:
            run:
              working-directory: .
        steps:
            - name: Checkout code
              uses: actions/checkout@v3
      
            - name: Set up Ruby
              uses: ruby/setup-ruby@v1
              with:
                ruby-version: 3.2.2
                bundler-cache: true
            
            - name: Bundler and Gem install
              run: |
                  gem install bundler
                  bundle install
              working-directory: ./backend/app

            - name: Run rubocop
              run: bundle exec rubocop
              working-directory: ./backend/app

```


## PrettierをGithubActionsを導入
`prettier`をgithubactionsに追加

```yml
    prettier:
        runs-on: ubuntu-latest
        defaults:
            run:
              working-directory: .
        steps:
            - name: Checkout code
              uses: actions/checkout@v3

            - name: Set up Node.js
              uses: actions/setup-node@v3
              with:
                node-version: '16.15.1'

            - name: Install npm
              run: npm ci
              working-directory: ./frontend/app

            - name: run Prettier
              run: npm run format
              working-directory: ./frontend/app

            - name: Check diff exits
              run: |
                git add -N .
                git diff
                line=`git diff | wc -l`
                if [ $line -gt 0 ]; then
                  echo "You need to format before commit"
                  git diff
                  exit -1
                fi
              working-directory: ./frontend/app
```







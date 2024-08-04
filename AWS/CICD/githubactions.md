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




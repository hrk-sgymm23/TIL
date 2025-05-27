# Dify x Bedrock

## Difyをローカル環境で起動させる

### 参考

- https://zenn.dev/tuzuminami/articles/9c8a814859af58
- https://github.com/langgenius/dify


### 以下実行

```
$ cd dify
$ cd docker
$ cp .env.example .env
$ docker compose up -d
```

http://localhost/installにアクセス

### Difyの使い方調査


## Dify on ECS

### 参考

- https://github.com/aws-samples/dify-self-hosted-on-aws
- https://dev.classmethod.jp/articles/dify-self-hosting-aws/

### clone

```
$ git clone git@github.com:aws-samples/dify-self-hosted-on-aws.git
```

### リージョンとコスト削減の設定

`cdk.ts`
```
export const props: EnvironmentProps = {
  awsRegion: 'ap-northeast-1',
  awsAccount: process.env.CDK_DEFAULT_ACCOUNT!,
  // Set Dify version
  difyImageTag: '1.3.1',
  // Set plugin-daemon version to stable release
  difyPluginDaemonImageTag: '0.0.9-local',

  // uncomment the below options for less expensive configuration:
  isRedisMultiAz: false,
  useNatInstance: true,
  enableAuroraScalesToZero: true,
  useFargateSpot: true,

  // Please see EnvironmentProps in lib/environment-props.ts for all the available properties
};

### 諸々コマンド実行

```
$ npm ci
# CDKを利用する際に一度だけ実行するコマンド
$ npx cdk bootstrap
# デプロイ 時間かかりそうなので後で実行
$ npx cdk deploy
```



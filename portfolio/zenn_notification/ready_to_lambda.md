# Lambdaの用意

### 参考
https://zenn.dev/tokatu/articles/f9092ce8128bab#%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA

### カスタムランタイムのGoを使いたい

- [LambdaでGoランタイムが使えなくなるのでカスタムランタイムに移行する（Terraform）](https://zenn.dev/ikarin0825/articles/30627c72d43494)

# 作業順序

## Slack API操作

- token払い出し
  - [Slackでアプリケーションを作成し、OAuth Tokenを発行するまで](https://qiita.com/kobayashi_ryo/items/a194e620b49edad27364)

```bash
$ go get -u github.com/slack-go/slack
$ cd work/zenn_notify_app/
$ make run
```

## Lambdaをローカルで実行できるようにする

## AWSアカウント用意

## tfコード作成&apply

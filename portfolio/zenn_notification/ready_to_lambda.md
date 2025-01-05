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

自分のアカウントを用いてメッセージ送信はできたが、botから送信できなかった。
以下を参考にbotを追加

https://zenn.dev/kou_pg_0131/articles/slack-api-post-message

## zenn dev apiとやりとり

```go
package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"time"

	"github.com/slack-go/slack"
)

// Article represents the structure of a single article.
type Article struct {
	ID          interface{} `json:"id"`
	Title       string `json:"title"`
	Path        string `json:"path"`
	PublishedAt string `json:"published_at"`
}

// Response represents the structure of the API response.
type Response struct {
	Articles []Article `json:"articles"`
}

func main() {
	// 1. Zenn API から記事情報を取得
	url := "https://zenn.dev/api/articles?topicname=aws&order=trend"
	resp, err := http.Get(url)
	if err != nil {
		panic(fmt.Sprintf("Error making GET request: %v", err))
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		panic(fmt.Sprintf("Unexpected status code: %d", resp.StatusCode))
	}

	var response Response
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		panic(fmt.Sprintf("Error parsing JSON: %v", err))
	}

	// 2. 記事情報を配列に格納
	articles := response.Articles

	// 3. 配列からランダムに1件を選択
	rand.Seed(time.Now().UnixNano())
	randomArticle := articles[rand.Intn(len(articles))]

	// 4. Slack に投稿
	tkn := "xxxxxx"
	c := slack.New(tkn)

	message := fmt.Sprintf("*おすすめの記事*\nTitle: %s\nPath: https://zenn.dev%s\nPublishedAt: %s",
		randomArticle.Title, randomArticle.Path, randomArticle.PublishedAt)

	_, _, err = c.PostMessage(
		"#zenn-ariticles-recommend", // 投稿先チャンネル
		slack.MsgOptionText(message, false),
	)
	if err != nil {
		panic(fmt.Sprintf("Error posting to Slack: %v", err))
	}

	fmt.Println("Message posted successfully!")
}
```


## Lambdaをローカルで実行できるようにする

## AWSアカウント用意
- spotify appのものを利用する


## tfコード作成&apply

### backendとtfstate準備



- https://qiita.com/_akira19/items/d929cae158be4110996d

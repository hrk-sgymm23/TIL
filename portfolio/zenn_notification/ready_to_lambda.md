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
	"io/ioutil"
	"net/http"
)

// Article represents the structure of an article in the response
type Article struct {
	ID       interface{} `json:"id"`
	Title    string `json:"title"`
	Path     string `json:"path"`
	PublishedAt string `json:"published_at"`
}

// Response represents the structure of the API response
type Response struct {
	Articles []Article `json:"articles"`
}

func main() {
	// API endpoint
	url := "https://zenn.dev/api/articles?topicname=aws&order=trend"

	// Create HTTP client and request
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("Error making GET request:", err)
		return
	}
	defer resp.Body.Close()

	// Check HTTP status code
	if resp.StatusCode != http.StatusOK {
		fmt.Printf("HTTP request failed with status: %d\n", resp.StatusCode)
		return
	}

	// Read response body
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		return
	}

	// Parse JSON response
	var response Response
	err = json.Unmarshal(body, &response)
	if err != nil {
		fmt.Println("Error parsing JSON:", err)
		return
	}

	// Print articles
	fmt.Println("Articles:")
	for _, article := range response.Articles {
		fmt.Printf("- Title: %s\n  Path: %s\n  PublishedAt: %s\n", article.Title, article.Path, article.PublishedAt)
	}
}
```


## Lambdaをローカルで実行できるようにする

## AWSアカウント用意

## tfコード作成&apply

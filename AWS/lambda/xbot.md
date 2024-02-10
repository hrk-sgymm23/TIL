# lamabdaを使ってXのBotを作る

## 参考
- [お役立ち Twitter Bot を作りながら学ぶ AWS ドリル](https://aws.amazon.com/jp/builders-flash/202201/aws-drill-twitter-bot-1/?awsf.filter-name=*all)
- [【X(Twitter) Bot】Ｘの運用がめんどくさい全ての人へ](https://zenn.dev/enterrocken/articles/e6ae6ddcc121d8)

## 記事の実装について知る
```tweet_module.py
API_ENDPOINT = "https://zenn.dev/api/articles?&order=liked_count"

load_dotenv(verbose=True)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# デフォルトの取得件数を20件とする
def get_popular_article(top_n: int = 20) -> list[dict[str, str]]:
    # 取得した記事をリストにする
    response_articles = requests.get(API_ENDPOINT).json()["articles"]
    # 
    popular_artilces = sorted(
        response_articles, key=lambda x: x["liked_count"], reverse=True
    )[:top_n]

    return popular_artilces
```

## エンドポイント
```
https://zenn.dev/api/articles?topicname=rails&order=liked_count
```
- devtoolより入手

## moduleについて
### 構造
- `get_popular_article`
　　- zenn apiに対してコールし記事のリストを得る
- `choose_ai_article`
  - 

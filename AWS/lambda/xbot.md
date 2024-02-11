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

## 衣装予報botを作る
### 必要なもの
- xアカウント
- APIキー
  - openai
  　　- https://openai.com/blog/openai-api
  - twitter
  　　- https://developer.twitter.com/en/products/twitter-api
- エンドポイント
 　-　livedoor互換のもの
    - https://weather.tsukumijima.net/api/forecast/city/130010 #地点は東京
 
## 手順
- 各アカウント作成
  - gameil
  - openapi
- コードの用意(リポジトリの作成)
  - `lambda_handler.py`
  - `module.py`
  - 仮想環境の作成
- テスト
- デプロイ
  - レイヤーの作成
  - コードの反映

  

  

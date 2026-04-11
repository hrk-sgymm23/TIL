# FastAPI Cloudを触る

- https://zenn.dev/shundeveloper/articles/93417d82f02dd5
- https://fastapicloud.com/docs/getting-started/

## はじめに

FastAPI CloudとはVercelなどのような開発体験をFastAPIでも得られる様にしたサービスとのことです(以下参照)
https://fastapicloud.com/blog/why-fastapi-labs-why-fastapi-cloud/

## 注意事項
FastAPICloudは現在(2026/04/11時点)ベータ版での公開となっており、以下リンクよりウェイティングリストに登録しJOINのメールが届き次第アカウントを作成することが可能になります
https://fastapicloud.com/

## 早速触ってみる

### FastAPIをローカルで作成

uvを使って準備
```bash
$ uv init fast_api_sandbox
$ cd fast_api_sandbox
$ uv venv .venv
$ source .venv/bin/activate
$ uv add "fastapi[standard]"
```

デプロイ
```bash
$ fastapi deploy
Installed 11 packages in 9ms

   FastAPI   Creating a new project 🚀
 
       env   Setting up environment with uv
 
      deps   Installing dependencies...
 
  template   Writing template files...
 
   success   ✨ Success! Created FastAPI project: myapp
 
             Next steps:
               $ cd myapp
               $ uv run fastapi dev
 
             Visit http://localhost:8000
 
             Deploy to FastAPI Cloud:
               $ uv run fastapi deploy
 
             💡 Tip: Use 'uv run' to automatically use the project's environment
```

### 動作確認
```bash
$ curl https://fast-api-sandbox-97a55331.fastapicloud.dev/
{"message":"Hello World"}%  
```

## FastAPI Cloudの各機能

FastAPIのダッシュボードを眺めていると色々な機能が搭載されていることが確認できます。

### ログ機能
curlしたリクエストを200で返していることが確認できます。
<img width="1470" height="830" alt="スクリーンショット 2026-04-11 20 50 28" src="https://github.com/user-attachments/assets/a9743f13-285f-4c94-af8c-5a8c640a7c6e" />


### DB接続機能
SupaBaseなどとの接続をネイティブでサポートしている様です。

<img width="1470" height="830" alt="スクリーンショット 2026-04-11 20 55 37" src="https://github.com/user-attachments/assets/b75863a7-9e52-4463-823a-05c6d7bdc940" />


### CICDサービスとの接続(トークン発行)
GitHub ActionsなどのCICDサービスからFastAPICloudへのデプロイを行うためのトークンの払い出しを行えます。
<img width="1470" height="829" alt="スクリーンショット 2026-04-11 21 05 52" src="https://github.com/user-attachments/assets/df47728a-b557-40d3-91bb-900d976f7a76" />


### AIサービスとの統合?

2026/04/11時点ではCommingSoonとなっていますが将来AIとの統合するサービスがローンチされるとのことで楽しみです

<img width="541" height="129" alt="スクリーンショット 2026-04-11 21 08 39" src="https://github.com/user-attachments/assets/7665bbd5-992f-4e80-b1fa-1bf8652e7c7e" />


## FastAPICloudを触れて見ての所感
- 触れてみてのまずの感想はデプロイの作業がかなりシンプルである点です。インフラ面を一つも気にしない点は冒頭でも触れた開発チームの思いを感じました。
- pythonの強みである仮想環境の充実を生かしコンテナを使わず、uvで簡潔し別途デプロイする際にコンテナを必要としない点もかなり魅力的です。
- まだベータ版であるため発展途上に感じますが今後AIとの統合や新機能サービスも含め期待できるサービスであると感じました










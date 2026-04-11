# FastAPI Cloudを触る

- https://zenn.dev/shundeveloper/articles/93417d82f02dd5
- https://fastapicloud.com/docs/getting-started/

## はじめに

FastAPI CloudとはVercelなどのような開発体験をFastAPIでも得られる様にしたサービスとのことです(以下参照)
https://fastapicloud.com/blog/why-fastapi-labs-why-fastapi-cloud/

## 早速触ってみる

### FastAPIをローカルで作成

```bash
$ uvx fastapi-new myapp
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

FastAPIのダッシュボードを眺めていると色々な機能が搭載されていることが確認できます

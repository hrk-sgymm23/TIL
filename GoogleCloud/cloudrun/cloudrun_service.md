# CloudRun Serviceにてメールやpush通知

## ローカルで実行する

### composeファイル用意

```yml
version: '3.8'

services:
  pubsub-app:
    build:
      context: .
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    tty: true
    volumes:
      - .:/app
```

`Dockerfile`
ローカルのファイルを変更した際にサーバーを再起動`--reload`
```dockerfile
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --reload main:app
```

### コンテナ起動

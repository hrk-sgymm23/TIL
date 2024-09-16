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

```bash
$ docker-compose up --build
```

### メッセージを送信

```bash
$ curl -X POST http://localhost:8080/ \
    -H "Content-Type: application/json" \
    -d '{"message": {"data": "SGVsbG8gd29ybGQ="}}'
```

`data`の値はエンコードした値にする必要がある
```bash
echo -n 'Hello World!' | base64
SGVsbG8gV29ybGQh

'{"message": {"data": "SGVsbG8gV29ybGQh}}'
```

python側でデコード
```python
if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
```

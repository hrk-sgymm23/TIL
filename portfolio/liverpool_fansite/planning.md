# Liverpool FanSite 構築順序

## リスト
- ローカル環境準備
- FireStore作成/FireStore環境構築
- CloudRun作成


# FireStore作成

## FireStore API 有効化

## FireStore開発環境構築

以下ファイルを用意
- .firebaserc
- firebase.json
- firestore.indexes.json
- firestore.rules

Firebaseの認証を通す
```bash
$ docker-compose run --rm firebase firebase login --no-localhost
```

Firebase初期化
```bash
$ docker compose run --rm firebase firebase init
```

以下エラー
```bash
Error: Failed to get Firebase project liverpool-fansite. Please make sure the project exists and your account has permission to access it.
```

https://console.firebase.google.com/?hl=ja

上記にてGoogle CloudとFireBaseのプロジェクトを紐付ける

以下が出ればOK
```bash
Firebase initialization complete!
```

# 開発環境を立ち上げる
```bash
$ docker compose build
$ docker compose up
```



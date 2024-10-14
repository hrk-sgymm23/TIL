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

## FireStore データ永続化
https://katashin.info/posts/firebase-emulator/#:~:text=Firebase%20%E3%82%A8%E3%83%9F%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%BF%E3%83%BC%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92,%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E3%81%9D%E3%81%AE%E3%81%BE%E3%81%BE%E8%AA%AD%E3%81%BF%E8%BE%BC%E3%81%BF%E3%81%BE%E3%81%99%E3%80%82

上記リンクを参考に

# まず開発環境で選手一覧のAPIを作成する

## まず開発環境にてコレクション格納を行う

https://qiita.com/soiSource/items/53990fca06fb9ba1d8a7

上記参考にjson読み込みから行う

https://zenn.dev/google_cloud_jp/articles/a0a6b5f855fe90#%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E4%BD%9C%E6%88%90%E3%83%BB%E5%8F%96%E5%BE%97

上記よりコレクション作成を行う

コレクションとドキュメントの関係性
```bash
players (コレクション)
  ├─ playerID1 (ドキュメント)
  ├─ playerID2 (ドキュメント)
  └─ playerID3 (ドキュメント)
```

firestore自体のデータ永続化ではなく、pythonのスクリプトをコンテナ起動時に実行することによって解決


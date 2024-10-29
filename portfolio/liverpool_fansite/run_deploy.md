# Cloud Runに対しデプロイする

# まずFireStoreにデータを用意

https://zenn.dev/hrk_sgyumm23/articles/37a4b59ade305e

＃ CloudRunのデプロイ

## イメージ、ビルドプッシュ
```bash
$ cd liverpool_fansite_app/api/docker/run/prd
$ docker build --platform linux/amd64 -t asia-northeast1-docker.pkg.dev/liverpool-fansite/liverpool-fansite-stg/liverpool-app:latest -f Dockerfile ../../../
$ docker push asia-northeast1-docker.pkg.dev/liverpool-fansite/liverpool-fansite-stg/liverpool-app:latest
```

## 環境変数を措定したい
- FireStoreのDB情報

https://cloud.google.com/run/docs/configuring/secrets?hl=ja#command-line

### シークレットマネージャーにjsonを登録しPythonで取得
https://zenn.dev/ushknn/articles/aae542a72f2881

### FireStoreとの接続を修正
https://gakogako.com/python_firestore/#%E8%AA%8D%E8%A8%BC%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89

<参考(抜粋)>
```python
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials


def main():
    # ===================== Firebase =====================================
    # このPythonファイルと同じ階層に認証ファイルを配置して、ファイル名を格納
    JSON_PATH = '〇〇.json'

    # Firebase初期化
    cred = credentials.Certificate(JSON_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
```




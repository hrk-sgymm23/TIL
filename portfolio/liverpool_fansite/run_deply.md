# Cloud Runに対しデプロイする

# まずFireStoreにデータを用意

## FireStore Emulatorからエキスポート

https://qiita.com/tanabee/items/2ce4d50e5ea320beb0cf

上記を参考にエクスポート

```bash
$ docker compose exec firebase /bin/sh
$ firebase emulators:export ./export_data/
```

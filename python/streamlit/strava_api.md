# Strava APIとの連携

## APIよりCSVを入手する

以下よりログイン
https://www.strava.com/settings/api

ユーザーデータを入手
```
$ curl -X GET \
https://www.strava.com/api/v3/athlete \
-H 'Authorization: Bearer {token}'
```

https://qiita.com/tatsuki-tsuchiyama/items/fb15145029e5e7318bec
上記よりtoken.py実行

実行時に502になるがURLのcodeに続く部分がトークンであるため問題なし

上記で入手したトークンを環境変数へ格納しactivity.pyを実行
以下のようなデータが得られる
```
[
    {
        "id": 15977030560,
        "name": "\u591c\u306e\u30e9\u30f3\u30cb\u30f3\u30b0",
        "distance": 5354.0,
        "moving_time": 2705,
        "elapsed_time": 2773,
        "total_elevation_gain": 17.0,
        "type": "Run",
        "start_date": "2025-09-29T15:30:41Z",
        "start_date_local": "2025-09-30T00:30:41Z",
        "timezone": "(GMT+09:00) Asia/Tokyo",
        "utc_offset": 32400.0,
        "average_speed": 1.979,
        "max_speed": 5.8,
        "average_cadence": 72.8,
        "average_temp": 24,
        "average_heartrate": 133.2,
        "max_heartrate": 201.0
    },
...
```


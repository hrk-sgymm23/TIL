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

## 取得したJSONをCSVへ変換
`convert.py`
```
import json
import csv
import os

data = [
  {
   ...
  }
]

# ファイルの位置は調整必須
csv_filename = "tmp_csv/activities.csv"

os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

# CSVに書き出す
with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
    # ヘッダーを自動で取得
    fieldnames = data[0].keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(data)

print(f"CSVファイル '{csv_filename}' を作成しました。")
```

以下のようなCSVを得る
```
id,name,distance,moving_time,elapsed_time,total_elevation_gain,type,start_date,start_date_local,timezone,utc_offset,average_speed,max_speed,average_cadence,average_temp,average_heartrate,max_heartrate
15977030560,夜のランニング,5354.0,2705,2773,17.0,Run,2025-09-29T15:30:41Z,2025-09-30T00:30:41Z,(GMT+09:00) Asia/Tokyo,32400.0,1.979,5.8,72.8,24,133.2,201.0
15960258117,Afternoon Trail Run,26934.7,11557,19264,1168.6,Run,2025-09-28T01:17:29Z,2025-09-28T10:17:29Z,(GMT+09:00) Asia/Tokyo,32400.0,2.331,9.8,,,,
```

## CSVを読み込んで表を作成


## 表グラフの表示をMVCっぽく切り分けてみる


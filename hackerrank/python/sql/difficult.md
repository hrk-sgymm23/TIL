# https://www.hackerrank.com/challenges/weather-observation-station-5/problem?isFullScreen=true

```sql
(
    select
        city, char_length(city) as nl
    from
        station
    order by 
        nl asc, city asc
    limit 1
)
union all
(
    select
        city, char_length(city) as nl
    from
        station
    order by 
        nl desc, city desc
    limit 1
)

```

## `union all`について
- クエリの結果を統合する(重複を削除しない)


# https://www.hackerrank.com/challenges/weather-observation-station-6/problem?isFullScreen=true

```sql
SELECT DISTINCT CITY 
FROM STATION
WHERE CITY REGEXP '^[aeiouAEIOU]';
```

以下でも代替可能
```sql
SELECT DISTINCT CITY 
FROM STATION
WHERE CITY LIKE 'A%' 
   OR CITY LIKE 'E%' 
   OR CITY LIKE 'I%' 
   OR CITY LIKE 'O%' 
   OR CITY LIKE 'U%';
```

## `DISTINCT`について

> DISTINCTはSQLのSELECT文とともに使用され、 データベースから取得した結果の中で重複しているデータを取り除き、ユニークなデータだけを返すためのコマンド

## `REGEXP`について

https://dev.mysql.com/doc/refman/8.0/ja/regexp.html

正規表現を実装できる

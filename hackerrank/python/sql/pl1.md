# 1

https://www.hackerrank.com/challenges/revising-the-select-query/problem?isFullScreen=true

```sql
SELECT
    *
FROM
    CITY
WHERE
    COUNTRYCODE = 'USA'
AND
    POPULATION > 100000;
```

# 2

https://www.hackerrank.com/challenges/revising-the-select-query-2/problem?isFullScreen=true

```SQL
SELECT
    NAME
FROM
    CITY
WHERE
    POPULATION > 120000
AND
    COUNTRYCODE = 'USA';
```

# 4

https://calendar.google.com/calendar/u/0/r/week

```SQL
SELECT
    *
FROM
    CITY
WHERE
    ID = '1661';
```

# https://www.hackerrank.com/challenges/weather-observation-station-3/problem?isFullScreen=true

```sql
SELECT
DISTINCT
    CITY
FROM
    STATION
WHERE
    MOD(ID, 2) = 0;
```

# https://www.hackerrank.com/challenges/weather-observation-station-4/problem?isFullScreen=true

```sql
SELECT COUNT(CITY) - COUNT(DISTINCT CITY) FROM STATION;
```







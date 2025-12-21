# 【22日間で学ぶ】SQL文、分析関数、テーブル設計、SQLチューニングまでMySQLで覚えるSQL実践講座

## RDBMSについて

- リレーショナルデータベースマネジメントシステム
- データベースの種類の一つでテーブル感の関係性を表形式のデータ構造で定義する
- RDBMS以外のDBをNoSQLという

## テーブル操作

### `RENAME TO`
- テーブル名の変更

```sql
ALTER TABLE users RENAME TO users_table;
``` 

### `DROP COLUMN`
- カラム列の削除
```sql
ALTER TABLE users DROP COLUMN class_no;
```

### `ADD`
- カラムの追加
```sql
ALTER TABLE table_name
ADD
  new_cloulmn_name new_cloulmn_defnition
  [FIRST | AFTER cloumn_name]
```

`FISRT`...テーブルの一番最初の列に追加
`AFTER`...一番最後の列に追加

### `MODIFY`
カラム定義の変更

### `CHANGE COULMN`
カラムの名前、場所定義の変更

### `DROP PRIMARY KEY`
主キーの削除

## `CHAR`固定長文字列(CHAR)と可変長文字列(VARCHAR)の違い

### CHAR型
- DBに格納する際にあらかじめ格納するデータの領域が確保される
- 指定した長さより短くても、空白の領域も確保される

- DB操作のパフォーマンスがいい
- データの長さがある程度固定されていて変化が少ない場合に用いる
  - 電話番号、銀行コード

### VARCHAR型
- DBにデータを格納する際にデータに応じて確保されるデータ領域を調整する

- DB操作のパフォーマンスが悪い
- データの長さが格納するデータに応じて大きく変わる場合に用いられる
  - 住所、テキストメッセージ

### `DISNTICT`
重複の削除
ex)
```sql
SELECT
	DISTINCT birth_date
FROM
	people
ORDER BY
	birth_date DESC;
```

### `TRUNCATE`
- 特定のテーブルを空にするSQL
- 一部削除...`DELETE`
- 全削除...`TRUNCATE`

- `DELETE`
  - データをロールバックすることができる
  - 処理速度は遅い
  - 使用しているディスク領域は解放されない
- `TRUNCATE`
  - データを完全削除することによりロールバックできない
  - DELETEよりも高速
  - 使用しているディスク領域が解放される

### NULLのデータを取り出す
- NULLは直接=では取り出せない
- NULLのものを取り出すには`IS NULL`, `IS NOT NULL`を使う

### `BETWEEN`
- 範囲指定
```sql
SELECT
	*
FROM
	users
WHERE	
	age 
BETWEEN
	5 AND 10;
```

### `LIKE`
- 部分一致
```sql
SELECT
	*
FROM
	users
WHERE	
	name
LIKE "%郎";
```

### `IN`,`NOT IN`
- 引数に該当する値を持つレコードを抽出
  - `NOT IN`は該当外
```sql
SELECT
	*
FROM
	users
WHERE	
	age IN (12, 24, 36);
```


### `ANY`
- 下記ではageが取り出されたもののどれかと等しいものだけ取り出せる

```sql
SELECT
	*
FROM
	users
WHERE
	age = ANY(SELECT age FROM employees WHERE salary > 5000000);
```

### `ALL`
- 単独では意味を持たず、比較演算子と合わせて使う
- 下記SQLは取り出したageの一番大きいもので比較を行う
```sql
SELECT
	*
FROM
	users
WHERE
	age > ALL(SELECT age FROM employees WHERE salary > 5000000);
```

### 算術演算子
- 文字の結合はCONCATを使う
```sql
SELECT
	department,
	`name`,
	salary*1.1
FROM
	employees;
```

## 数学関数

### `ROUND`

桁数指定なしは第一位切り捨て
```sql
SELECT ROUND(3.14);

3
```

整数指定は小数点第xi位で切り捨て
```sql
SELECT ROUND(3.14, 1);

3.1
```

負の数指定は整数第xi位で切り捨て
```sql
SELECT ROUND(987, -1);

990
```

### `FLOOR`

### `CEILING`






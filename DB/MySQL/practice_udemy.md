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

切り捨て
```sql
SELECT FLOOR(3.14);

3
```

### `CEILING`

切り上げ
```sql
SELECT CEILING(3.14);

4
```

### `POWER`
累乗
```sql
SELECT POWER(3,4);

81
```

### `COALESCE`
-　最初に登場するNULLではない値を返す
```sql
COALESCE(列1, 列2, ...)
```

```sql
SELECT COALESCE('A','B','C') # A
SELECT COALESCE(NULL,'B','C') # B
SELECT COALESCE(カラム１,カラム2,カラム3) FROM users # usersテーブルから取得してカラム１,カラム2,カラム3のうちNULLではない最初の文字を取得する
```

### `IF`
条件をチェックして真と偽の場合で表示内容を変える
```sql
SELECT IF(100 < 200, "真"、"偽") # 真
```

```sql
SELECT *,IF(birth_place="日本","日本人","その他") AS "国籍" FROM users;
```

```sql
SELECT name, age, IF(age < 20, "未成年", "成人") FROM users;
```

```sql
SELECT *, IF(class_no=6 AND height > 170, "6組の170cm以上の人", "その他") FROM students;
```


### `CASE`

複数の条件式をチェックして条件に応じて表示する値を変える(IFの上位互換)
```sql
CASE式1
CASE 評価する列
	WHEN 値1 THEN 値１の時に返す
	WHEN 値2 THEN 値２の時に返す
	ELSE デフォルト値
END
```

```sql
SELECT
	*,
	CASE birth_place
	WHEN "日本" THEN "日本人"
	WHEN "Iraq" THEN "イラク人"
	ELSE "外国人"
	END AS "国籍"
FROM
	users;
```

```sql
SELECT
	name,
	CASE
		WHEN name IN("香川県","愛媛県","徳島県","高知県") THEN "四国"
		ELSE "その他"
	END AS "地域名"
FROM
	prefectures;
```

-　閏年計算
  - 閏年は4で割り切れるかつ100で割り切れない値
```sql
SELECT
	name,
	birth_day,
	CASE
		WHEN DATE_FORMAT(birth_day, "%Y") % 4 = 0 AND DATE_FORMAT(birth_day, "%Y")% 100 <> 0 THEN "閏年"
		ELSE "閏年でない"
	END AS "閏年か"
FROM
	users;
```

### `ORDER BY`で`CASE`

```sql
ORDER BY CASE  ...END ASC(DESC)
```

### `UPDATE`で`CASE`
- 香川を四国という名前へ更新
```sql
UPDATE
  prefectures
SET
  name = CASE
    WHEN name IN ("愛媛", "香川", "高知", "徳島") THEN "四国"
    ELSE "その他"
  END
WHERE
  name = "香川";
```

### `CASE`で`NULL`
```sql
	SELECT
		CASE
			WHEN country="Japan" THEN "日本人"
			WHEN country IS NULL THEN "不明"
	FROM
		users;
```

## 43 演習問題
1
```sql
SELECT
	name,
	age
FROM
	customers
WHERE
	age BETWEEN 28 AND 40
	AND name LIKE "%子%"
ORDER BY
	age ASC
LIMIT 5;
```

5
```sql
UPDATE customers
	SET age = age + 1
WHERE
	id BETWEEN 20 AND 50;
```

7
```sql
SELECT 
	*
FROM
	students
WHERE
	class_no = 1
	AND height < ALL(
		SELECT height + 10
		FROM students
		WHERE class_no IN (3,4)
	)
```

８
```sql
UPDATE employees SET department = TRIM(department); 
```

### `TRIM`
空白削除
```sql
TRIM(文字列)
```

特定の文字を削除

```sql
SELECT TRIM(BOTH '-' FROM '----abc----')

abc
```

9
https://qiita.com/rickeysan95/items/554079d4dc543b2dd062
```sql
UPDATE 
	employees 
SET
	salary =  
	CASE
		WHEN salary >= 5000000 THEN salary*0.9
		WHEN salary < 5000000 THEN salary*1.1
	END;
```

10
```sql
INSERT INTO customers
    (id, name, age, birth_day)
VALUES
    (101,'名無し権平', 0, NOW());
```

11
```
ALTER TABLE customers ADD name_length INT AFTER birth_day;

UPDATE customers SET name_length = LENGTH(name)
```

12

```sql
ALTER TABLE tests_score ADD score INT AFTER test_score_3;
UPDATE 
	tests_score
SET score =
		CASE
			WHEN COALESCE(test_score_1, test_score_2, test_score_3) IS NULL THEN NULL
			WHEN COALESCE(test_score_1, test_score_2, test_score_3) >= 900 
				THEN FLOOR(COALESCE(test_score_1, test_score_2, test_score_3)*1.2)
			WHEN COALESCE(test_score_1, test_score_2, test_score_3) <= 600
				THEN CEIL(COALESCE(test_score_1, test_score_2, test_score_3)*0.8)
		END
```

13
```sql
SELECT *
FROM employees
ORDER BY FIELD(
  department,
  'マーケティング部',
  '研究部',
  '開発部',
  '総務部',
  '営業部',
  '経理部'
);
```

### `ORDER BY FIELD`

(列, 値1, 値2...)となり値1,2,3...の順番で出力がソートされる

https://note.com/nhsykym/n/n30d6fd3b3198


## トランザクションとは
- 複数のSQLを一塊にして、扱うようにDBに指示する
- 実行に成功したら、結果を反映し（コミット）、失敗したら元に戻す(ロールバック)

## 原始性について
- トランザクションに含まれる複数のSQLの不可分のものであり必ず「全て実行される」か「一つも実行されていない」状態に制御しなければならないとするDBの性質

### COMMIT
トランザクションを完了して実行結果をDBに反映させるSQLコマンド
```sql
START TRANSACTION;
INSERT...
DELETE...
COMMIT;
```

### ROLLBACK
トランザクションを無効にしてDBを前の状態戻すこと
```sql
START TRANSACTION;
INSERT...
DELETE...
ROLLBACK;
```

## 自動コミットモードについて
- 多くのDBMSでは明示的にトランザクションを実行しない限りSQLを実行すると自動的にコミットされる
- これを自動コミットという

## ロックとは
- DBのテーブルや行を固定し別のトランザクションからテーブルや行の参照を更新できない

## 共有ロック、排他(占有)ロックとは
- ロックには2つの方法がある
  - 共有ロック...他のトランザクション(ユーザー)から参照はできるが更新はできなくするロック
  - 排他ロック...他のトランザクションから参照も更新もできなくする

## 複数のトランザクションがロックをかけた場合
- 共有ロックは複数のトランザクションをかけられる
- 排他ロックをかけると別のユーザーからは排他ロック、共有ロックはかけれれない





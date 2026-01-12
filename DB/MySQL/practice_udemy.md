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

## 行ロックとテーブルロック
- ロックする対象に主に行とテーブルがある(DBにロックすることも可能)
```sql
START TRANSACTION;
UPDATE table SET name = "xx" WHERE id = 12　# id12だけがロックがかかる(行ロック)
```

## トランザクションとロック
トランザクションを開始して、テーブルの更新、削除、ロックに関連する処理が実行されるとトランザクションが終了するまでテーブルレコードがロックされる

## SQLとロック(SELECT)
テーブルロック
```sql
# 共有ロック
SELECT * FROM users FOR SHARE;
# 排他ロック
SELECT * FROM users FOR UPDATE(NOWAIT)
```

行ロック
```sql
# 共有ロック
SELECT * FROM users WHERE id = 1 FOR SHARE;
# 排他ロック
SELECT * FROM users WHERE id = 1 FOR UPDATE
```

## SQLとロック(UPDATE,DELETE,INSERT)
UPDATE,DELETE,INSERTを実行した場合自動的に排他ロックされる

## 明示的なテーブルのロック、デッドロック

##　明示的にテーブルをロックする
- DBにはトランザクション以外にもテーブルをロックするコマンドが存在する

- 実行したセッションはテーブルは読みことはできるが書き込むことはできない
- 他のセッションもテーブルは読み込むことができるが書き込むことはできない
```sql
LOCK TABLE {テーブル名} READ
```

- 実行したセッションはテーブルは読みことも書き込むこともできる
- 他のテーブルは読み込むことも書き込むこともできない
```sql
LOCK TABLE {テーブル名} WRITE
```

- 元セッションの保有するテーブルロックを全て解除する
```sql
UNLOCK TABLES
```

## デッドロック
- 2つのセッションが互いの更新対象のテーブルをロックしていて、処理が進まない状態のこと

## アプリケーションとロックとトランザクション

## アプリケーションでのトランザクション処理
- アプリケーションでトランザクションの処理を記述することでトランザクションを実行することができる

## 集合演算子
- 構造のよく似た複数のテーブルに対してSELECTでレコードを取得して取得結果を組み合わせるSQL
<img width="893" height="353" alt="スクリーンショット 2025-12-29 16 38 37" src="https://github.com/user-attachments/assets/267fa05b-d7ac-4a8b-84d0-2f6cbb277889" />


### `UNION`
- 検索結果の和集合を求めるSQL分
- UNIONは重複する行はひとつにまとめ、UNION ALLは重複する行は重複したまま表示する

### `EXPECT`(MINUS)
- ある集合と別の集合の輪を求めるSQL
- SQL1とSQL2を比較してSQL1の結果のうちSQL2の結果に存在するものを差し引く
  - 2つの結果の差を表示

### `INTERSECT`
- ある集合と別の集合の積集合を求めるSQL
- SQL1とSQL2の結果を比較して2つの結果に共通する行を表示する

## 各SQL

### `UNION`
```sql
SELECT * FROM table1
UNION
SELECT * FROM table2
```
- 集合演算子を使う際の注意点
  - 各SQLの取得するカラム数を合わせること
  - ORDERBYを利用する場合はひとつめのSQLのカラム名を用いいること

## `INTERSECT`, `EXPECT`
- 重複の削除
```sql
SELECT * FROM new_students
INTERSECT
SELECT * FROM students;
```
- new_studentsに存在してstudentsに存在しない
```sql
SELECT * FROM new_students
EXPECT
SELECT * FROM students;
```


## 集計関数
- `SUM`,`AVG`,`MIN`,`MAX`,`COUNT`

- 何行データが入っているか
```sql
SELECT COUNT(*) FROM customers;
```
- 列指定（この列に何行入っているかNULLはカウントしない）
```sql
SELECT COUNT(name) FROM customers;
```

## グループに分ける(`GROUPBY`)
- `GROUPBY`を使うと要素ごとにグループ分けして集計できる

```sql
SELECT カラム名 FROM テーブル名 GROUP BY カラム1
```

年齢別で集計を行う
```sql
SELECT age, COUNT(*), MAX(birth_day), MIN(birth_day) FROM users
WHERE birth_place="日本"
GROUP BY age;
```

- GROUP BY xx...xxごとに集計する
- 複数のGROUP BY...xxとyyの組み合わせごとの集計

## `HAVING`
- グループ化した集計に対して絞り込みをする場合に利用するSQL

```sql
SELECT
	department,
	AVG(salary)
FROM
	employees
GROUP BY
	department
HAVING AVG(salary) > 3980000;
```
- HAVINGは実行結果に対するWHERE
- 集計した後の結果に条件をかけるための句

```sql
SELECT
	department,
	AVG(salary)
FROM
	employees
GROUP BY
	department
HAVING
	AVG(salary) > 3980000;
```

```sql
SELECT birth_place, age, COUNT(*) FROM users
GROUP BY birth_place, age
HAVING COUNT(*)>2;
```

# SQLの評価される順番に関して

```
FROM
 → WHERE      （行を削る）
 → GROUP BY   （まとめる）
 → HAVING     （グループを削る）
 → SELECT
```

## 副問い合わせの構文1(INで使う)
INの後に()で囲いその中にSELECTを記述するとSELECTの結果に含まれるレコードだけを取り出すことができる
```sql
SELECT 
	last_name, first_name
FROM
	employees
WHERE
	office_code IN(SELECT 
		office_code
	FROM
		offices
	WHERE
		country = 'USA'
	);
```

## 副問い合わせの構文2(INで複数のカラムを使う)
INの後に()で囲いその中にSELECTを記述し複数のカラムを取得する
```sql
SELECT 
	last_name, first_name
FROM
	employees
WHERE
	(office_code, office_name) IN(SELECT 
		office_code, office_name
	FROM
		offices
	WHERE
		country = 'USA'
	);  
```

## 副問い合わせの構文3(集計関数と使う)
WHERE句の比較式に()で囲ったSELECT文を記述し副問い合わせで集計した値と比較する

```sql
SELECT
	customerNumber,
	checkNumber,
	amount
FROM
	payments
WHERE
	amount = (SELECT MAX(amount) FROM payments);
```

## 副問い合わせの構文4(FROMの取得先に用いる)
FROMの取得対象のテーブルの代わりに()でSELECTを記述

```sql
SELECT
	MAX(lineItems.items),
	MIN(lineItems.items),
	FLOOR(AVG((lineItems.items))
FROM
	(SELECT
		order_number, COUNT(order_number) AS items
	 FROM
		order_details
	GROUP BY
		orderNumber) AS lineitems
	)
```

## 副問い合わせの構文5(SELECTの行に用いる)
SELECTで取得する対象の行に含める
```sql
SELECT
	p1.site_name,
	(
	 SELECT
		MAX(file_zize)
	 FROM
		page2 AS p2
	 WHERE
		p2.site_id = p1.site_id
	) AS max_file_size
FROM
	pages1 AS p1;
```

```sql
SELECT
	cs.first_name,
	cs.last_name,
	(SELECT
		MAX(order_date) FROM orders AS order_max WHERE cs.id = order_max.customer_id
	) AS "最新注文日",
	(SELECT
		SUM(order_amount * order_price) FROM orders AS order_temp WHERE cs.id = order_temp.customer_id
	) AS "全支払い金額"
FROM
	customers AS cs
WHERE
	cs.id < 10;
```

## 副問い合わせの構文6(CASEとともに使う)
SELECTで対象の行に含める

```sql
SELECT
	employee_id,
	last_name,
	(
	 CASE
	 	WHEN department_id = (
			SELECT
				department_id
			FROM
			 	departments
			WHERE
				location_id = 2500
		) THEN 'Canada'
		ELSE 'USA'
	 END
	) location
FROM
	employees;
```


## `INSERT INTO SELECT`
- SELECTの処理結果をテーブルに挿入する

## `CREATE TABLE SELECT`
- 別のテーブルを作成して、SELECTの結果を挿入する

# `EXITS`
- 他のテ－ブルに値の存在する行のみを抽出するSQL
- サブクエリ内でメインクエリの表や列を利用する副問い合わせ

```sql
SELECT
	*
FROM
	a_table
WHERE
	[NOT] EXISTS(sunquery);
```

## EXISTSの構文
- EXISTSのEXISTSの後ではサブクエリが何らかの値を返すレコードだけ取り出す(NO EXISTSの場合は値を返さないレコードだけ取り出す)
```sql
SELECT
	*
FROM
	customers AS ct
WHERE
	EXISTS(
		SELECT
			*
		FROM
			order AS or
		WHERE
			ct.cusomer_id = or.customer_id
);
```

```sql
SELECT
	*
FROM
	employees AS em
WHERE
	EXISTS(
		SELECT * FROM departments AS dt WHERE em.department_id = dt.id
	);
```

INと組み合わせ
```sql
SELECT
	*
FROM
	employees AS em
WHERE
	EXISTS(
		SELECT
			*
		FROM
			departments AS dt
		WHERE
			dt.name IN ("営業部","開発部")
			AND em.department_id = dt.id
	);
```

- EXISTSにおける`SELECT 1`
  - 値を取りたいわけではない
  - 行が存在するか知りたい
  - 1は値は使わないという意思表示

## NULLとEXISTS
- EXISTS句ではサブクエリで値が返されるレコードのみを取得する
  - NULLにものは変えされない

## INTERSECTとEXEPCTをEXISTSで実現する

### EXPECTを実現

```sql
SELECT * FROM b_table WHERE
NOT EXISTS(
SELECT * FROM a_table
WHERE
	a_table.columm_1 = b_table.columm_1 AND
	a_table.columm_2 = b_table.columm_2 AND
	:
)
```

### INTERSECTを実現
- customers と customers_2 に「完全一致する顧客」がいるかどうかをチェックする
- phone_numberだけ書き方が特殊
  - 両方NULLの場合に一致と反映されないため
```sql
SELECT * FROM customers AS c1 
	WHERE EXISTS(
		SELECT * FROM customers_2 AS c2
		WHERE
			c1.id = c2.id AND
			c1.first_name = c2.first_name AND
			c1.last_name = c2.last_name AND
			(c1.phone_number = c2.phone_number OR (c1.phone_number IS NULL AND c2.phone_number IS NULL )) AND
			c1.age = c2.age
	);
```


# テーブルの結合について
- RDBMSでは特定のカラム(列)を用いて同じ値のレコード同士をひもづけることができる。これをテーブルの結合という。

 ## 1対1の結合
 - 複数のテーブルが1レコードにつき1レコードが紐づく結合を1対1(One to One)結合し合う
 - 国に対し首都が1対1

## 1対多の結合
 - 複数のテーブルが一方のテーブルの1レコードにつき片方のテーブルの複数テーブルに紐づく結合
 - 注文に対し複数の注文詳細が紐づく

## 多対多の結合
- 複数のテーブルで各テーブルが互いのテーブルに対して複数のレコードに紐づく結合を多対多という
- 本に対して本_著書が1対多で著者に対して本_著書が多対1で紐づく
- 本_著書は中間テーブル

## JOINとは
- 特定のカラム同士が等しいレコード同士をテーブル間で結合するSQL
- `INNER JOIN`...条件が一致する行のみ表示
```sql
INNER JOIN 接続するテーブル名 ON 接続する条件
```

## 内部結合
```sql
SELECT
	*
FROM
	employees AS emp
INNER JOIN
	departments as dep
ON
	emp.department_id = dep.id;
```

- `=`以外で紐付ける
```sql
SELECT
	*
FROM
	employees AS emp
INNER JOIN
	students as std
ON
	emp.id < std.id;
```

## 外部結合`LEFT(OUTER) JOIN`
- 複数のテーブルを結合して左のテーブルは全てのレコードを取得して、右のテーブルからは紐付けできたレコードのみを取り出す、それ以外はNULL

```sql
SELECT
	emp.id, emp.first_name, emp.last_name, dt.id, dt.name AS department_name
FROM
	employees AS emp
LEFT JOIN
	departments as dt
ON
	emp.department_id = dt.id;
```

`COALESCE`で該当なし表示
```sql
SELECT
	emp.id, emp.first_name, emp.last_name, COALESCE(dt.id, "該当なし") AS department_id,  dt.name AS department_name
FROM
	employees AS emp
LEFT JOIN
	departments as dt
ON
	emp.department_id = dt.id;
```

































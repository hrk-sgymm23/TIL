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

###

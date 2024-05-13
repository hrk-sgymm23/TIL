# RDS作成

# `aws_db_instance`作成

## `replace`関数について
[replace Function](https://developer.hashicorp.com/terraform/language/functions/replace)

### 第二引数で指定した値を第３引数に変更する
```bash
> replace("1 + 2 + 3", "+", "-")
1 - 2 - 3

> replace("hello world", "/w.*d/", "everybody")
hello everybody
```

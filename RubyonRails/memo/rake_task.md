# rakeタスクでDB操作

[【Rails 】Rakeタスクとは](https://qiita.com/mmaumtjgj/items/8384b6a26c97965bf047#:~:text=Rake%20%E3%81%A8%E3%81%AF%E3%80%81%20Ruby%20%E3%81%A7,%E5%A0%B4%E6%89%80%E3%82%92%20Rakefile%20%E3%81%A8%E5%91%BC%E3%81%B6%E3%80%82)

上記を参考に簡単なのからやってみる

## rakeタスク作成

### `generate`
```bash
$rails g task ファイル名
$rails g task greet
```

### タスク記述
```ruby
namespace :greet do
desc "say Hello"
    task say_hello: :environment do
        puts "Hello"
    end
end
```

### タスクが存在するか確認
```bash
$ rake -T

~
rake greet:say_hello                    # say Hello
~
```

### タスク実行
```bash
$ rake greet:say_hello

root@ef4695459bb5:/api# rake greet:say_hello
Hello
```

## `development.log`のログ削除
[logディレクトリ以下にあるすべてのlogファイルを0バイトに切り詰める](https://railsdoc.com/page/rails_log_clear)
```bash
$ rails log:clear
```

## トランザクションについて深掘り
[ActiveRecordのトランザクションを理解する](https://qiita.com/mtoyopet/items/67d1cff3df00aa651cb7)
> トランザクションとは、複数のSQL文によるデータの更新を「1つの処理」とし、全てのSQLの実行が成功した時にデータベースに更新分を反映させることです。データベースの整合性を保つ目的があります。
> 基本的に、複数のSQLを同時に実行する際はトランザクションを使う必要があります。


## ユーザーを作成し、そのユーザーに紐づく投稿を作成するrakeファイルを作成する。
```bash
root@ef4695459bb5:/api# rails g task create_sample_data
      create  lib/tasks/create_sample_data.rake
```
```ruby

```









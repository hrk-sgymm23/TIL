# リソースを復活させる

## NATgatewayが必ず差分として出てきてしまう。。

### `ignore_changes`を使うとリソースの変更を無視できる？
https://dev.classmethod.jp/articles/note-about-terraform-ignore-changes/

#### ignore_changesのユースケース
> : 実体を正としたい
例えば、以下のように「この値は常にTerraformコードの設定を保つ必要がなく、実体を正としたい」といった場合が最も適したユースケースと言えそうです。
> AutoScalingGroupのEC2の起動数
運用開始後は自由にスケールしてほしい
リソースへのタグ付け
他要因によって付けられたタグをTerraformで削除してほしくない

### リソースの属性の変更を無視するものでリソース自体を無視することはできない、、
結局コメントアウトに。。。

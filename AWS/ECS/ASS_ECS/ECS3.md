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

## ALBに関して(料金)
- https://aws.amazon.com/jp/elasticloadbalancing/pricing/
- https://qiita.com/T_unity/items/f1be3704072f439dc807
- https://qiita.com/himorishuhei/items/1066c5c579be6de0441c

### 料金の体系
- 時間
- LCU(Load Balancer Capacity Units)

### 料金計算
- 時間
  - USD 0.0243/1h *  24 * 30 = 17.496$ *2 = 35$

## 必要なリソース群

- VPC
- subnet
  - for ECS
  - for ALB
  - for RDS
- SecurityGroup
  - for ECS
  - for ALB
  - for RDS


## パブリックサブネットとプライベートサブネット間の通信について

https://qiita.com/hatsu/items/8b30e68ba7252a749fe7#modulessubnet

上記記事ではNATGateWayを使っているがコスト面で懸念→vpcエンドポイントを使う

https://dev.classmethod.jp/articles/privatesubnet_ecs/

## VPC(VPCとサブネットでモジュールを分ける)

## Terraform`toset`について

### [Terraformの型とループ処理 for_each = { for } について理解する](https://zenn.dev/kasa/articles/8fe998e04cb916)

### [便利な Terraform 関数集](https://zenn.dev/cloud_ace/articles/terraform_functions#toset-%E9%96%A2%E6%95%B0)

> toset() は引数の型を変換する関数です。for_each 文は、map 型または、 string の集合( Set )型でしか使えません。そこで、toset() で list(string) 型を string の集合型に変換さて、for_each を実行させるのに使います。

```terraform
locals {
  toset_sample = [
    "a",
    "b"
  ]
}

resource "terraform_data" "main" {
  for_each = toset(local.toset_sample)

  provisioner "local-exec" {
    command = format("echo %s", each.value)
  }
}
```

## `cidrsubnets`関数について

### [[Terraform/AWS]複数のサブネットを一度に作る](https://zenn.dev/shonansurvivors/articles/5424c50f5fd13d#cidrsubnet%E9%96%A2%E6%95%B0%E3%81%A8length%E9%96%A2%E6%95%B0)
> 第一引数のCIDRを分割して返してくれます。

```bash
$ terrafform console
> cidrsubnet("172.31.0.0/16", 8, 0)
"172.31.0.0/24"

> cidrsubnet("172.31.0.0/16", 8, 1)
"172.31.1.0/24"
```

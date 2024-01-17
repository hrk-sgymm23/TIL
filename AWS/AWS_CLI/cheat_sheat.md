# AWS CLI 環境変数&リージョンチートシート
※引用　https://qiita.com/notakaos/items/4a7774ee6e1d11bb55d2

## AWS CLI 環境変数
```bash
export AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxx     # アクセスキー
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxx  # シークレットアクセスキー
export AWS_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxx  # セッショントークン

export AWS_DEFAULT_REGION=ap-northeast-1      # デフォルトリージョン   
export AWS_DEFAULT_OUTPUT=json                # 出力形式 (json|text|table)
export AWS_PROFILE=default                    # プロファイル名

export AWS_CONFIG_FILE=~/.aws/config          # コンフィグファイルパス
export AWS_SHARED_CREDENTIALS_FILE=~/.aws/credentials # クレデンシャルファイルパス
export AWS_CA_BUNDLE=<AWS_CA_BUNDLE_PATH>     # 証明書バンドルへのパス
```
[Configuring the AWS Command Line Interface - AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
{Environment Variables - AWS Command Line Interface](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-envvars.html)

## リージョン
### 東京リージョン
```bash
 アジアパシフィック（東京）
ap-northeast-1
```

### 利用可能なリージョン
```bash
us-east-1      # 米国東部（バージニア北部）
us-east-2      # 米国東部（オハイオ）
us-west-1      # 米国西部（北カリフォルニア）
us-west-2      # 米国西部（オレゴン）
ca-central-1   # カナダ (中部)
eu-central-1   # 欧州（フランクフルト）
eu-west-1      # 欧州（アイルランド）
eu-west-2      # 欧州（ロンドン）
eu-west-3      # 欧州（パリ）
eu-north-1     # 欧州（ストックホルム）
eu-south-1     # ヨーロッパ（ミラノ）
af-south-1     # アフリカ（ケープタウン）※要オプトイン
ap-east-1      # アジアパシフィック（香港）※要オプトイン
ap-northeast-1 # アジアパシフィック（東京）
ap-northeast-2 # アジアパシフィック（ソウル）
ap-northeast-3 # アジアパシフィック（大阪: ローカル）
ap-southeast-1 # アジアパシフィック（シンガポール）
ap-southeast-2 # アジアパシフィック（シドニー）
ap-south-1     # アジアパシフィック (ムンバイ)
me-south-1     # 中東（バーレーン）※要オプトイン
sa-east-1      # 南米（サンパウロ）
```
https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/using-regions-availability-zones.html

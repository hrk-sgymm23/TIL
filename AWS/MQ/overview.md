# Amazon MQについて調べる

## 参考
- [Amazon MQとAmazon SQSの違いと選定基](https://zenn.dev/iwamasa/articles/b5fd0c120ce57a)
- [AWS Black Belt Online Seminar Amazon MQ](https://pages.awscloud.com/rs/112-TZM-766/images/20210317_AWS-BlackBelt_AmazonMQ%20210317a.pdf)

## 概要
- オープンオースメッセージブローカー向け完全マネージド型サービス
- Apache Active MQ, Rabbit MQをサポート
- 運用負荷の軽減
- 豊富なメッセージング機能
- 低遅延と高耐久
- 業界標準のプロトコルとAPIに対応

## 特徴
- Apache Active MQ, Rabbit MQの完全マネージドサービス
- 垂直及び水平スケール(SQSは自動でスケール)

## メッセージブローカー
- ソフトウェア、コンポーネント間での情報の伝達を容易に
- 各コンポーネントを疎結合化し、相手に依存性を最小化
- 投入データのバッファリングし、バルク処理を容易に
- それぞれが最も効率的に処理を行えるようにスケール、バルク処理などを適用

## Apache ActiveMQ 概要
- Javaで実装され、JMS、REST、WebSocketのインターフェースを提供
- AMQP、MQTT、OpenWire、STOMPに対応
- Java, C, C++, C#, Ruby, Perl, Python, PHP を始め、多様な言語から接続可能

## 基本的な構成要素

### キュー
- point to pointで信頼性のあるメッセージングを実現
- 各メッセージは単一のコンシューマが取得
- FIFOとonce and only onceをサポート

<img width="504" alt="スクリーンショット 2025-03-04 21 47 44" src="https://github.com/user-attachments/assets/759d6fb3-8564-40f1-8241-b68d1b0245d5" />

### トピック
- 同一メッセージを複数の送信先へ送達
- Pub/Sub型
- メッセージはアクティブなサブスクリプションを持つ全てのコンシューマへ送信される
- 永続サブスクリプションを使用すると切断中のメッセージを再接続時に取得可能

### ブローカー
- 複数のブローカーエンジン
- 単一のブローカーまたはマルチアクティブAZアクティブ/スタンバイブローカー
- パブリック接続可能またはパブリック接続不可
- SGやユーザー、認可にマップによるアクセス制御

#### 単一インスタンスブローカー
- 1AZ、1ブローカーのシンプルな構成
- 開発やテストに向く
- SLAは定義されない
- `mq.m5`インスタンスファミリーの場合、ストレージを選択可能
  - EFS,EBS
 
#### アクティブ/スタンバイブローカー
**2つのアベイラビリティーゾーンに分散配置されるこうかよう性対応構成**
- 各プロトコルやActiveMQウェブコンソールのエンドポイントはアクティブインスタンスポイント側の利用が可能
- 障害発生時にはテイクオーバー
- アプリケーションはフェイルオーバートランスポートを定義することで稼働中のエンドポイントへ接続
- SLAの対象

## RabbitMQ
- 企業規模を問わず支持を集める軽量なメッセージブローカー
- プロトコルとしてAMQPに標準対応

### RabbitMQの主なメッセージング要素
- Exchanges
  - メッセージを0以上のQueueへルーティング
  - ExchangesType
  　　- Direct,Topic,Fanout,Headers
- Bidings
  - メッセージをキューへルーティングするためにexchangeに利用される
- Queues
  - アプリケーションが利用するメッセージを保持する

## 基本的な構成要素/ブローカー
- 単一ブローカーまたはクラスターブローカー
- パブリック接続可能またはプライベート

## 単一ブローカー(パブリックアクセス)

<img width="873" alt="スクリーンショット 2025-03-08 17 10 25" src="https://github.com/user-attachments/assets/2a63ce4b-ac08-4495-a8fa-0df4d9e9d2a2" />

## 単一ブローカー(プライベートアクセス)

<img width="746" alt="スクリーンショット 2025-03-08 17 19 55" src="https://github.com/user-attachments/assets/483f4b85-75ff-4b14-aed1-4fa5933b7d7d" />

## クラスターブローカー
- 3つのノードを異なるAZに配置

### クラスターブローカーの耐久性
- プロデューサー及びコンシューマー向けの単一エンドポイントを提供
- AmazonMQが`ha-mode=all`及び`ha-sync-mode=automatic`を全てのrabbitMQポリシーに設定することでmirroed queue構成を実現する
- ノードの交換時には
  - AmazonMQは自動的にリプレースされる
  - コンシューマは切断されるため、再接続が必要
  - 新たなMirrorが接続されるとキューは自動的に同期される
 
## AmazonMQ for RabbitMQの管理
- rabbitmqadmin
  - コマンドラインから利用可能なrabbitMQ REST API client
  - ブローカー作成後よりRabbitMQのバージョンに即したものを取得する
  - `-p 443` Amazon MQ Rabbit Webコンソールのポートを指定

## AmazonMQの主な制限
- ブローカー
  - ブローカー数: 20
  - ブローカー設定履歴の深さ: 10
  - ブローカーあたりのセキュリティグループ数: 5
  - CloudWatchでモニタリングされる送信先
    - RabbitMQ: コンシューマ数の上位500(キュー) 
- データストレージ
  - ブローカあたりのストレージ容量: 200GB

## 料金
- ブローカーインスタンスの料金
  - メッセージブローカの使用量に基づいた時間単位で課金(1秒ごと)
  - 料金はメッセージブローカーインスタンスのサイズ、選択する構成(単一,アクティブ/スタンバイ、クラスター)による
- ブローカーストレージの料金
  - 月単位での平均ストレージ使用量に基づいた課金
  - EFSの場合: GB-Monthあたり0.36USD
  - EBSの場合: GB-Monthあたり0.12USD
- データ転送料金
  - AmazonMQで送受信されたデータに対して通常のAWSのデータ転送料金が






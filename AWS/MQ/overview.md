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
- 


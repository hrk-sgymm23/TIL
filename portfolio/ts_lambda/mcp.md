# MCPについて

## そもそもMCPとは

出典: https://zenn.dev/cloud_ace/articles/model-context-protocol

- MCPはAIとデータソースや外部ツールを標準化された方法で接続する
- AIアシスタントに10個のサービスを連携したいとする。10個のサービスに対し各APIへの接続コードを書く必要があった
- しかしMCPクライアントを実装するだけでMCPに対応した全てのサービスと連携できるようになる

### MCPホスト
- MCPホストは生成AIモデルを搭載したアプリケーション
- Claude, Cursorなど

### MCPクライアント
- MCPクライアントはMCPホスト内に組み込まれたコンポーネントでMCPサーバーとの通信を担当する
- クライアントはサーバーとの接続を確立しリソースやツール、プロンプトなどの機能を利用するためのリクエストを送信する

### MCPサーバー
- MCPサーバーは特定のデータソースやツールアクセスを提供する軽量サーバ例えばファイルシステム、データベース、APIなどのアクセスを提供するサーバー
- サーバーはクライアントからのリクエストを処理し、必要なデータや機能を提供する

## MCPの主要な機能

### リソース
- リソースはAIモデルが参照できるデータやコンテンツを提供する
- ファイルシステム、DB、ドキュメントなど

### ツール
- ツールはAIモデルが実行できる関数やアクションを提供する
- 単純なテキスト生成では不十分な場合に外部システムと対話するための機能を提供する

### プロンプト
- プロンプトはAIモデルの応答の方を作るテンプレート。適切なプロンプトは汎用的なテキストではなく、正確で有用な結果を得るために重要

# MCPを触ってみる

- [[https://zenn.dev/nozomi_cobo/articles/start-genkit-mcp#%E3%81%82%E3%82%8F%E3%81%9B%E3%81%A6%E8%AA%AD%E3%81%BF%E3%81%9F%E3%81%84-(genkit-%E3%81%AB%E8%88%88%E5%91%B3%E3%82%92%E6%8C%81%E3%81%A3%E3%81%9F%E6%96%B9%E5%90%91%E3%81%91)](https://zenn.dev/nozomi_cobo/articles/start-genkit-mcp)](https://zenn.dev/nozomi_cobo/articles/start-genkit-mcp)


## genkit cliのインストール

```bash
$ npm install -D genkit-cli
```

## 実行
```
$ npx genkit start -o -- tsx --watch src/index.ts
```

## gemini aiモデルリスト
- https://ai.google.dev/gemini-api/docs/models?hl=ja

## 上の記事が動かなかったため公式チュートリアルを試す
- https://firebase.google.com/docs/genkit/get-started?hl=ja















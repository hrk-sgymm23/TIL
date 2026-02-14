# 自然言語からMCPでmermaidにてフローチャート作成

## 利用しているnodeのバージョン
```
v24.10.0
```

## そもそもMCPとは
- AIがほかツールを安全に呼び出すための共通規格

## mcp インストール
```bash
$ npm install -g mermaid-mcp-server
```

## Cline（VSCode拡張)の準備

<img width="1024" height="806" alt="スクリーンショット 2026-02-14 21 39 56" src="https://github.com/user-attachments/assets/f65360e6-fbf1-456f-ace8-7c419d8766ca" />

## cline_mcp_setting.json

<img width="1470" height="956" alt="スクリーンショット 2026-02-14 21 14 29" src="https://github.com/user-attachments/assets/fe10ec34-aaed-4419-80c0-b65da87271b5" />

```json
{
  "mcpServers": {
    "mermaid-mcp-server": {
      "command": "mermaid-mcp-server",
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## とりあえず使ってみる
プロンプト
```
以下の文章を Mermaid の flowchart で表現して

・「分岐は菱形、開始/終了は丸、例外は点線」
・「日本語ラベルは必ずダブルクォートで囲む」
・「生成後に validate_mermaid を実行し、通らなければ修正して」
・「最後に render_mermaid_svg でSVG化して」

下記内容で作成して
ユーザーが申請 → 入力チェック → OKなら承認依頼 → 承認なら完了、否認なら差し戻し → 入力チェックへ戻る
```

## とりあえずの結果
```mermaid
flowchart TD
    A["ユーザーが申請"] --> B{"入力チェック"}
    B -->|"OK"| C["承認依頼"]
    B -->|"NG"| D["差し戻し"]
    C -->|"承認"| E["完了"]
    C -->|"否認"| D
    D -.->|"再入力"| B
```

<img width="1470" height="828" alt="スクリーンショット 2026-02-14 21 33 19" src="https://github.com/user-attachments/assets/de3cf37c-b582-4c5b-83a9-b1982f3e07a0" />


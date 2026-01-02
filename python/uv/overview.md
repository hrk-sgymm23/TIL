# uvについて学ぶ

- インストール
```bash
$ brew install uv
```

- 初期設定
```bash
$ uv init uv_practice
$ cd uv_practice/
```

- 仮想環境作成、有効化
```
$ uv venv
$ source .venv/bin/activate
```

仮想環境を意識せずとも`uv run`で自動的に仮想環境内でコマンドやスクリプトを実行できる

# `uv run`使い方

```bash
uv run main.py

Hello from uv-practice!
```

- `uv run`の便利な特徴
  - 依存関係が書かれたスクリプトを実行すると自動で必要なパッケージを一時環境にインストールしてから実行する

## パッケージの追加、削除

```bash
$ uv add numpy pandas
$ uv remove numpy
```

## パッケージのインストール、同期、ロック
同期
```bash
$ uv sync
```
依存関係のロックファイルを更新
```bash
$ uv lock
```
依存関係のツリー表示
```bash
$ uv tree
```

## pythonのバージョン管理
インストール
```bash
$ uv python install 3.10 3.11
```

インストールずみのバージョン確認
```bash
$ uv python list
```

プロジェクトで使うバージョンの固定
```bash
$ uv python pin 3.13
```

CLIツールのインストール
```bash
$ uv tool install ruff
$ uv tool list
```

## `uvx`コマンドの使い方
`uvx`はCLIツールやパッケージを一時的な環境で素早く実行できるコマンド

cowsayを実行
```bash
uvx cowsay -t "Hello, uv!"
  _________
| Hello, uv |
  =========
         \
          \
            ^__^
            (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

pytestを実行
```sql
uvx pytest
```

### `uvx`の主なオプション
`--from`...指定パッケージのコマンドを使用
`--with`...追加パッケージも同時にインストールして実行
`--isolated`...完全に新しい一時環境で実行(既存ツール無視)













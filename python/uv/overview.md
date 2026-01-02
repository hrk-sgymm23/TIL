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

また既存のrewuirements.txtからもインストール可能
```bash
$ uv add -r requirements.txt 
```

`--dev`で開発環境のパッケージとして追加も可能
```bash
$ uv add numpy --dev
```

`pyproject.toml`には以下形式で追加されている
```toml
[dependency-groups]
dev = [
    "jupyterlab>=4.5.1",
    "numpy>=2.4.0",
]
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
```bash
$ uvx pytest
```

ruffを実行
```
$ uvx ruff check .
All checks passed!
```

### `uvx`の主なオプション
`--from`...指定パッケージのコマンドを使用
`--with`...追加パッケージも同時にインストールして実行
`--isolated`...完全に新しい一時環境で実行(既存ツール無視)

## `pip互換コマンド`
`uv pip install`...パッケージのインストール
`uv pip uninstall`...パッケージのアンインストール
`uv pip list`...インストールずみのパッケージ一覧
`uv pip freeze`...バージョン固定用リスト出力
`uv pip check`...依存関係の整合性チェック

## 依存関係のエクスポート
```
$ uv export --format=requirements.txt
```

既存のpip/venvから移行する際も簡単


## 他のツールとの統合
GitHubActionsやDocker統合は以下を参照
https://docs.astral.sh/uv/guides/integration/


# まとめ
- uvは仮想環境、パッケージ、Pythonバージョン、CLIツール管理を一元化
  - uvが高速なのはRust製である点、並列処理が得意でありpip(製)と差異がでる
- `uv run`で仮想環境を意識せず安全/高速にスクリプトやコマンドを実行
- `uvx`で一時的なCLIツール実行も可能
- 他ツールとの統合の容易にできる







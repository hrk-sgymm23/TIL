# 12. 仮想環境とパッケージ

# 12.1. はじめに

> Pythonアプリケーションは特定のライブラリやそのバージョンを必要とすることが多く、異なるアプリケーション間でライブラリのバージョン要求が衝突することがあります。この問題を解決するために 仮想環境 を使用します。
> 仮想環境は、特定のPythonバージョンと追加パッケージを含む独立した環境を提供し、各アプリケーションがそれぞれの環境で必要なライブラリを自由に管理できます。これにより、ライブラリのバージョン変更が他のアプリケーションに影響を与えることを防ぎます。


# 12.2. 仮想環境の作成

以下のようにして仮想環境を作成可能
```bash
$ python -m venv tutorial-env{仮想環境名}
```

これは tutorial-env ディレクトリがなければ作成して、その中に Python インタプリタ、その他関連するファイルのコピーを含むサブディレクトリを作る

仮想環境を作成後、有効か
```bash
$ source tutorial-env/bin/activate
```

有効化し、Pythonを実行するとその仮想環境のPythonを実行化するようになる。

```python
$ source ~/envs/tutorial-env/bin/activate
(tutorial-env) $ python
Python 3.5.1 (default, May  6 2016, 10:59:36)
  ...
>>> import sys
>>> sys.path
['', '/usr/local/lib/python35.zip', ...,
'~/envs/tutorial-env/lib/python3.5/site-packages']
```

仮想環境を無効化は以下
```python
$ deactivate
```

# 12.3. pip を使ったパッケージ管理

> pip と呼ばれるプログラムでパッケージをインストール、アップグレード、削除することができます。デフォルトでは pip は Python Package Index からパッケージをインストールします。
> ブラウザを使って Python Package Index を閲覧することができます。

```python
(tutorial-env) $ python -m pip install novas
Collecting novas
  Downloading novas-3.1.1.3.tar.gz (136kB)
Installing collected packages: novas
  Running setup.py install for novas
Successfully installed novas-3.1.1.3
```

バージョンの指定
パッケージ名のあとに == とバージョン番号を付けることで、特定のバージョンのパッケージをインストールすることもできる
```python
(tutorial-env) $ python -m pip install requests==2.6.0
Collecting requests==2.6.0
  Using cached requests-2.6.0-py2.py3-none-any.whl
Installing collected packages: requests
Successfully installed requests-2.6.0
```

`python -m pip show`...指定されたパッケージの情報を表示

```python
(tutorial-env) $ python -m pip show requests
---
Metadata-Version: 2.0
Name: requests
Version: 2.7.0
Summary: Python HTTP for Humans.
Home-page: http://python-requests.org
Author: Kenneth Reitz
Author-email: me@kennethreitz.com
License: Apache 2.0
Location: /Users/akuchling/envs/tutorial-env/lib/python3.4/site-packages
Requires:
```

`python -m pip list`...仮想環境にインストールされた全てのパッケージを表示
```python
(tutorial-env) $ python -m pip list
novas (3.1.1.3)
numpy (1.9.2)
pip (7.0.3)
requests (2.7.0)
setuptools (16.0)
```

`requirements.txt`...バージョン管理システムにコミットして、アプリケーションの一部として配布することができます。ユーザーは必要なパッケージを`pip install -r`でインストールできる

```python
(tutorial-env) $ python -m pip install -r requirements.txt
Collecting novas==3.1.1.3 (from -r requirements.txt (line 1))
  ...
Collecting numpy==1.9.2 (from -r requirements.txt (line 2))
  ...
Collecting requests==2.7.0 (from -r requirements.txt (line 3))
  ...
Installing collected packages: novas, numpy, requests
  Running setup.py install for novas
Successfully installed novas-3.1.1.3 numpy-1.9.2 requests-2.7.0
```


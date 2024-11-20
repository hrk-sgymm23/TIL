# 10. 標準ライブラリミニツアー

https://docs.python.org/ja/3/tutorial/stdlib.html

# 10.3. コマンドライン引数

## `sys`

```python
# File demo.py
import sys
print(sys.argv)
```

上記を以下のように実行
```bash
$ python demo.py one two three
```
出力結果
```bash
$ ['demo.py', 'one', 'two', 'three']
```

## `argparse`

コマンドライン引数を処理するための機能
```python
import argparse

parser = argparse.ArgumentParser(
    prog='top',
    description='Show top lines from each file')
parser.add_argument('filenames', nargs='+')
parser.add_argument('-l', '--lines', type=int, default=10)
args = parser.parse_args()
print(args)
```

上記を以下のように実行
```bash
$ python top.py --lines=5 alpha.txt beta.txt
```

結果は以下
`args.lines`を`5`、`args.filenames`を `['alpha.txt', 'beta.txt']`に設定。

# 10.5. 文字列のパターンマッチング

```python
import re
re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
# ['foot', 'fell', 'fastest']
re.sub(r'(\b[a-z]+) \1', r'\1', 'cat in the the hat')
# 'cat in the hat'
```

上記解説
- `re.findall`...指定された式表現に一致する部分文字列をリストとして返す。
  - `r'\bf[a-z]*'`
    - `\b`単語の境界を表す
    - `f`...`f`にマッチするか
    - `[a-z]*`小文字のアルファベット全体にマッチするか(`f`)で始まる文字列全体
- `re.sub`...指定された正規表現に一致する文字列を指定された文字列に置き換えます
  - `r'(\b[a-z]'`...一文字以上からなる単語を認識
  - `+) \1`...最初に正規表現にて認識した単語の同じ文字列をマッチさせる。
  - `r'\1'`...第二引数の置き換え文字列最初に認識した単語へ置き換え

つまり上記場合、全単語を調べる上で`the the`を認識し、1個目に認識した`the`へ置き換える。

# 10.7. インターネットへのアクセス

> インターネットにアクセスしたりインターネットプロトコルを処理したりするための多くのモジュールがあります。最も単純な2つのモジュールは、 URL からデータを取得するための urllib.request と、メールを送るための smtplib です

`urllib.request`
```python
from urllib.request import urlopen
with urlopen('http://worldtimeapi.org/api/timezone/etc/UTC.txt') as response:
    for line in response:
        line = line.decode()             # Convert bytes to a str
        if line.startswith('datetime'):
            print(line.rstrip())         # Remove trailing newline
```

`smtplib`
```python
import smtplib
server = smtplib.SMTP('localhost')
server.sendmail('soothsayer@example.org', 'jcaesar@example.org',
"""To: jcaesar@example.org
From: soothsayer@example.org

Beware the Ides of March.
""")
server.quit()
```

# 10.9. データ圧縮

```python
import zlib
s = b'witch which has which witches wrist watch'
len(s)
41
```

# 11.4. マルチスレッディング

> スレッド処理 (threading) とは、順序的な依存関係にない複数のタスクを分割するテクニックです。スレッドは、ユーザの入力を受け付けつつ、背後で別のタスクを動かすようなアプリケーションの応答性を高めます。同じような使用例として、I/O を別のスレッドの計算処理と並列して動作させるというものがあります。

```python
import threading, zipfile

class AsyncZip(threading.Thread):
    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile
        self.outfile = outfile

    def run(self):
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print('Finished background zip of:', self.infile)

background = AsyncZip('mydata.txt', 'myarchive.zip')
background.start()
print('The main program continues to run in foreground.')

background.join()    # Wait for the background task to finish
print('Main program waited until background was done.')
```

- `class AsyncZip(threading.Thread):`を継承して`AsyncZip`クラスを作成
- `__init__`...入出力ファイルを設定、`threading.Thread.`スーパークラスのコンストラクタを作成
- `def run(self):`にてzipファイル作成と作成完了のログを出す設定
- `background = AsyncZip('mydata.txt', 'myarchive.zip') background.start()`にてインスタンス作成とスレッド作成
  - `background.start()`にて`run()`が走る
- `background.join() print('Main program waited until background was done.')` にてメインスレッドの処理待ちその後ログ出力

# リスト操作のためのツール

`array`

```python
from array import array
a = array('H', [4000, 10, 700, 22222])
sum(a)
26932
a[1:3]
array('H', [10, 700])
```

- `arrray(typecode, いてれーた)`
  - `typecode`...配列内のデータ型を指定する1文字のコード。
    - `H`...符号なし2バイト
  - いてれーた...配列の初期値となるリストやタプルなどのシーケンス。


`collections.deque`
> collections モジュールでは、 deque オブジェクトを提供しています。リスト型に似ていますが、データの追加と左端からの取り出しが速く、その一方で中間にある値の参照は遅くなります。こうしたオブジェクトはキューや木構造の幅優先探索の実装に向いています
```python
from collections import deque
d = deque(["task1", "task2", "task3"])
d.append("task4")
print("Handling", d.popleft())
Handling task1
```


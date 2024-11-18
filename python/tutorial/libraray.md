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





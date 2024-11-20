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





# 6. モジュール

https://docs.python.org/ja/3/tutorial/modules.html

# この章で使うファイル

`fibo.py`

```python
ef fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

def fib2(n):   # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a+b
    return result
```


# 6.1　モジュールについてもう少し
`as`または`from`を使うことでモジュールを任意の名前で扱えるようになる

`as`

```python
import fibo as fib
fib.fib(500)
0 1 1 2 3 5 8 13 21 34 55 89 144 233 377
```

`from`

```python
from fibo import fib as fibonacci
fibonacci(500)
0 1 1 2 3 5 8 13 21 34 55 89 144 233 377
```

6.11 モジュールをスクリプトとして実行する
モジュールを以下実行するとモジュール内のコードが実行できる

```python
$ python fibo.py <arguments>
```

モジュールの末尾に以下を追加することで、同時にスクリプトとして実行できるようになる

```python
if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))
```

```bash
$ python fibo.py 50
0 1 1 2 3 5 8 13 21 34
```

モジュールが import された場合は、そのコードは実行されない
```python
import fibo
```

6.4 パッケージ

パッケージはドット付きモジュールを使って構造化する手段

```bash
sound/                          Top-level package
      __init__.py               Initialize the sound package
      formats/                  Subpackage for file format conversions
              __init__.py
              wavread.py
              wavwrite.py
              aiffread.py
              aiffwrite.py
              auread.py
              auwrite.py
              ...
      effects/                  Subpackage for sound effects
              __init__.py
              echo.py
              surround.py
              reverse.py
              ...
      filters/                  Subpackage for filters
              __init__.py
              equalizer.py
              vocoder.py
              karaoke.py
              ...
```

> パッケージを import する際、 Python は sys.path 上のディレクトリを検索して、トップレベルのパッケージの入ったサブディレクトリを探します。

ファイルを含むパッケージをpythonに扱わせるには`_init_.py`が必要
`_init_.py`は空のファイルで良いが、パッケージの初期化のコードを書いたり`_all_`変数を使ったりする



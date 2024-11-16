# 8. エラーと例外

# 8.3. 例外を処理する

```python
while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")

```

以下tryの説明を抜粋

> もしも except 節 で指定された例外と一致しない例外が発生すると、その例外は try 文の外側に渡されます。例外に対するハンドラ (handler、処理部) がどこにもなければ、 処理されない例外 (unhandled exception) となり、エラーメッセージを出して実行を停止します。

`try..expect`はオプションとして`else`を設けることができる。`else`を設ける場合、全ての`ecpect`より後ろに記述しなくてはならない
`else`は`try`にて全く例外が送出されなかったおきに実行できるコードとして役立つ

```python
for arg in sys.argv[1:]:
    try:
        f = open(arg, 'r')
    except OSError:
        print('cannot open', arg)
    else:
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()
```

> 例外ハンドラは、try 節 の直接内側で発生した例外を処理するだけではなくその try 節 から (たとえ間接的にでも) 呼び出された関数の内部で発生した例外も処理します。例えば:

```python
def this_fails():
    x = 1/0

try:
    this_fails()
except ZeroDivisionError as err:
    print('Handling run-time error:', err)

Handling run-time error: division by zero
```

# 8.4. 例外を送出する

`raise`文を使って例外を発生させることが可能。

```python
raise NameError('HiThere')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    raise NameError('HiThere')
NameError: HiThere
```

`raise`の唯一の引数は創出される例外を示す。
これは例外インスタンスや例外クラス(BaseException を継承したクラス、たとえば Exception やそのサブクラス)でなければならない。

8.5 例外の連鎖

ある例外から直接影響されていることを示すために`raise`のオプションの`from`を指定する

```python
raise RuntimeError from exc
```

```python
def func():
    raise ConnectionError

try:
    func()
except ConnectionError as exc:
    raise RuntimeError('Failed to open database') from exc

Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
    func()
    ~~~~^^
  File "<stdin>", line 2, in func
ConnectionError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
    raise RuntimeError('Failed to open database') from exc
RuntimeError: Failed to open database
```

# 8.7. クリーンアップ動作を定義する`finally`

`try`文にはクリーンアップ動作がある。どんな状況でも必ず実行される

```python
>>> try:
...     raise KeyboardInterrupt
... finally:
...     print('Goodbye, world!')
...
Goodbye, world!
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
KeyboardInterrupt
>>>
```

もし`finally`がある場合、`try`文が終わる前の最後の処理を`finally`が実行する。
`try`が例外を発生させるかに問わず`finally`実行される。

## 複雑なケース
- もし`try`の実行中に例外が発生したら`expect`によって処理される。もし例外が`expect`により処理されなければ`finally`が実行された後にその例外が再送出される。
- `expect`または`else`にて例外が発生したとする。その場合は`finally`が実行された後に例外が再送出される。
- `finally`内で`break`,`continue`,`return`が実行された場合、例外は再創出されない。
- もし`try`文が`break`,`continue`または`return`のいずれかに達するとその`break`,`continue`または`return`の直前に`finally`が実行される。
- もし`finally`が`return`を含む場合、返される値は`try`の`return`ではなく`finally`の`return`になる


例
```python
def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        print("division by zero!")
    else:
        print("result is", result)
    finally:
        print("executing finally clause")

divide(2, 1)
result is 2.0
executing finally clause
divide(2, 0)
division by zero!
executing finally clause
divide("2", "1")
executing finally clause
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    divide("2", "1")
    ~~~~~~^^^^^^^^^^
  File "<stdin>", line 3, in divide
    result = x / y
             ~~^~~
TypeError: unsupported operand type(s) for /: 'str' and 'str'
```

上記より`finally`はどの場合でも実行される。
一番最後の文字列の割り算で`TypeError`は`expect`で処理されないため、先に`finally`が実行されたのちに例外が再創出される。

> 実世界のアプリケーションでは、 finally 節は(ファイルやネットワーク接続などの)外部リソースを、利用が成功したかどうかにかかわらず解放するために便利です。

# 8.9. 複数の関連しない例外の送出と処理

いくつか発生した例外の報告が必要なケースがある。

`ExceptionGroup`は例外インスタンスのリストをまとめ、同時に創出できるようにする。
 ExceptionGroupも例外のため他の例外と同じように捕捉できる。

```python
def f():
    excs = [OSError('error 1'), SystemError('error 2')]
    raise ExceptionGroup('there were problems', excs)

f()
  + Exception Group Traceback (most recent call last):
  |   File "<stdin>", line 1, in <module>
  |     f()
  |     ~^^
  |   File "<stdin>", line 3, in f
  |     raise ExceptionGroup('there were problems', excs)
  | ExceptionGroup: there were problems (2 sub-exceptions)
  +-+---------------- 1 ----------------
    | OSError: error 1
    +---------------- 2 ----------------
    | SystemError: error 2
    +------------------------------------
try:
    f()
except Exception as e:
    print(f'caught {type(e)}: e')

caught <class 'ExceptionGroup'>: e

```

##  ExceptionGroupの例外の処理

https://atmarkit.itmedia.co.jp/ait/articles/2211/11/news021.html

### パターン１  ExceptionGroupでまとめられている個々の例外を`expesct*`節で処理する方法
```python
try:
    # ExceptionGroup例外を送出するコード
except* TypeError as e:
    # ExceptionGroup例外に格納されているTypeError例外を処理
except* ValueError as e:
    # ExceptionGroup例外に格納されているValueError例外を処理
```

### パターン２　ExceptionGroup全体をまとめて処理する方法

```python
ry:
    # ExceptionGroup例外を送出するコード
except ExceptionGroup as eg:
    # ExceptionGroup例外に格納されている例外を個別に取り出して処理する
```

# 8.10. ノートによって例外を充実させる

例外を受け取った後に情報を追加できる。
例外は`add_note(note)`メソッドを持ちます。

例えば複数の例外を一つにまとめたいとき各エラーのコンテキスト情報を追加したい場合がある。


```python
def f():
    raise OSError('operation failed')

excs = []
for i in range(3):
    try:
        f()
    except Exception as e:
        e.add_note(f'Happened in Iteration {i+1}')
        excs.append(e)

raise ExceptionGroup('We have some problems', excs)
  + Exception Group Traceback (most recent call last):
  |   File "<stdin>", line 1, in <module>
  |     raise ExceptionGroup('We have some problems', excs)
  | ExceptionGroup: We have some problems (3 sub-exceptions)
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "<stdin>", line 3, in <module>
    |     f()
    |     ~^^
    |   File "<stdin>", line 2, in f
    |     raise OSError('operation failed')
    | OSError: operation failed
    | Happened in Iteration 1
    +---------------- 2 ----------------
    | Traceback (most recent call last):
    |   File "<stdin>", line 3, in <module>
    |     f()
    |     ~^^
    |   File "<stdin>", line 2, in f
    |     raise OSError('operation failed')
    | OSError: operation failed
    | Happened in Iteration 2
    +---------------- 3 ----------------
    | Traceback (most recent call last):
    |   File "<stdin>", line 3, in <module>
    |     f()
    |     ~^^
    |   File "<stdin>", line 2, in f
    |     raise OSError('operation failed')
    | OSError: operation failed
    | Happened in Iteration 3
    +------------------------------------
```


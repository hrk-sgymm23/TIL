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




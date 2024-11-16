# 9 クラス

# 9.2. Python のスコープと名前空間

名前空間(ネームスペース)とは名前からオブジェクトへの対応づけのことを指す。
属性という言葉は`.`に続く名前全てに対して使っている。
例えば式`z.real`で`real`はオブジェクト`z`の属性。

名前空間はさまざまな時点で作成され、寿命もさまざま。

# 9.2.1. スコープと名前空間の例

```python
def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

scope_test()
print("In global scope:", spam)
```

出力結果
```python
After local assignment: test spam
After nonlocal assignment: nonlocal spam
After global assignment: nonlocal spam
In global scope: global spam
```

`do_local()`...スコープ:`do_local`関数内
`do_nonlocal()`...スコープ:`do_nonlocal` scope_test`関数内
`do_global()`...スコープ:モジュールレベル

# 9.3. クラス初見

# 9.3.1. クラス定義の構文

クラス定義の単純な形式
```python
class ClassName:
    <statement-1>
    .
    .
    .
    <statement-N>
```

# 9.3.2. クラスオブジェクト

クラスオブジェクトは2種類の演算、属性参照とインスタンス生成をサポートしている。

属性参照には`obj.name`を使う

```python
class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'
```

クラスのインスタンス化には関数記法を使う。クラスオブジェクトのことをクラスの新しいインスタンスを返す引数のない関数のように扱う

```python
x = MyClass()
```
上記はクラスの新しいインスタンスを作成し、そのオブジェクトをローカル変数xへ格納する。


インスタンス化操作ではからのオブジェクトが作成される。多くのクラスは特定の初期状態でカスタマイズされたオブジェクトを作成したい。
そのためクラスには`_init_()`という特殊メソッドが定義されている。新しくインスタンス化された際に自動的に`_init_()`を呼び出す。

```python
def __init__(self):
    self.data = []
```

```python
class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

x = Complex(3.0, -4.5)
x.r, x.i
(3.0, -4.5)
```




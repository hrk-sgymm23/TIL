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

# 9.3.3. インスタンスオブジェクト

インスタンオブジェクトでできる操作は**属性の参照**。有効な属性名はデータ属性とメソッドの2種類がある。

## データ属性
```python
x.counter = 1
while x.counter < 10:
    x.counter = x.counter * 2
print(x.counter)
del x.counter
```

# 9.3.4. メソッドオブジェクト
メソッドとはオブジェクトの属するメソッドのこと


```python
x.f()
```

```python
xf = x.f
while True:
    print(xf())
```

### メソッドが呼び出された時、実際には何が起きているか？

`f()`の関数定義では引数を一つ指定していたにも関わらず上記では`x.f()`にて引数なしで呼び出されている。
**なぜ呼び出せるかというと引数にインスタンスオブジェクトが渡されるため**

**`x.f()`という呼び出しは`MyClass.f(x)`と等価である。**

# 9.3.5. クラスとインスタンス変数

```python
class Dog:

    kind = 'canine'         # 全インスタンスで共有されるクラス変数

    def __init__(self, name):
        self.name = name    # インスタンスごとに固有のインスタンス変数

>>> d = Dog('Fido')
>>> e = Dog('Buddy')
>>> d.kind                  # すべての犬で共有
'canine'
>>> e.kind                  # すべての犬で共有
'canine'
>>> d.name                  # d 固有
'Fido'
>>> e.name                  # e 固有
'Buddy'
```

以下コードは間違い

`tricks`がクラス変数として扱われ、別の犬間で同じ`tricks`が共有されてしまうため。
```python
class Dog:

    tricks = []             # クラス変数の間違った使用

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)

>>> d = Dog('Fido')
>>> e = Dog('Buddy')
>>> d.add_trick('roll over')
>>> e.add_trick('play dead')
>>> d.tricks                # 意図せず すべての犬で共有
['roll over', 'play dead']

```

以下正しい例

```python
class Dog:

    def __init__(self, name):
        self.name = name
        self.tricks = []    # 犬ごとに新しい空リストを作る

    def add_trick(self, trick):
        self.tricks.append(trick)

>>> d = Dog('Fido')
>>> e = Dog('Buddy')
>>> d.add_trick('roll over')
>>> e.add_trick('play dead')
>>> d.tricks
['roll over']
>>> e.tricks
['play dead']
```

# 9.4. いろいろな注意点

以下では`f`,`g`,`h`は全て`C`の属性であり,関数オブジェクトを参照している。
全て`C`のインスタンスメソッドである。

```python
# クラス外で定義された関数
def f1(self, x, y):
    return min(x, x+y)

class C:
    f = f1

    def g(self):
        return 'hello world'

    h = g
```

メソッドは`self`引数のメソッド属性を使って他のメソッドを呼び出すことができる

```python
class Bag:
    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)
```

# 9.5. 継承

Python には継承に関係する 2 つの組み込み関数がある

- `isinstance()`を使うとインスタンスの型が調べられる。
   - isinstance(obj, int) は `obj.__class__`が`int`や`int`の派生クラスの場合に限り`True`になります。
- `issubclass()`を使うと継承関係が調べられる。
  - bool は int のサブクラスなので `issubclass(bool, int)` は `True` です。しかし、 `float`は `int` のサブクラスではないので `issubclass(float, int)` は False です。


# 9.6. プライベート変数

> オブジェクトの中からしかアクセス出来ない "プライベート" インスタンス変数は、 Python にはありません。しかし、ほとんどの Python コードが従っている慣習があります

しかしアンダースコアで始まる名前は非publicなものとして扱う慣習がある。ex)`_spam`

名前マングリングは、サブクラスが内部のメソッド呼び出しを壊さずにオーバーライドするのに便利。

```python
class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update   # 元の update() メソッドのプライベートコピー

class MappingSubclass(Mapping):

    def update(self, keys, values):
        # update() への新シグネチャ導入
        # しかし __init__() は壊さない
        for item in zip(keys, values):
            self.items_list.append(item)
```

上記ではもし`MappingSubClass`に`__update`識別子を導入しても機能する。
`Mapping`クラスでは`_Mapping__update`となり`_MappingSubclass__update`にそれぞれ置き換えるからである。

# 9.7. 残りのはしばし

名前つきのデータ要素を一まとめにするデータ方`dataclasses`

```python
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    dept: str
    salary: int
```

```python
john = Employee('john', 'computer lab', 1000)
john.dept
'computer lab'
john.salary
1000
```

# 9.8. イテレータ (iterator)

イテラブルとイテレータに関して
https://yumarublog.com/python/iter/

## イテラブルとは
for文で要素を一つずつ取り出せるような反復可能なオブジェクトのこと

- シーケンス型(リスト、タプル、range)
- マッピング型(辞書)
- テキストシーケンス型(文字列)
- バイナリシーケンス型(bytes、bytearray、memoryview)

## イテレータに関して
型の一つで順番に要素を取得できるオブジェクトのこと

# 9.9 ジェネレータ

ジェネレータはイテレータを作成するためのツール

ジェネレータは通常の関数のように書かれるが何らかのデータを返す際には`yield`を使う

以下例
```python
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]
```

```pyhton
for char in reverse('golf'):
    print(char)

f
l
o
g
```

# 9.10. ジェネレータ式
リスト内包表記のように書くが`[]`ではなく`()`で囲むのが特徴

```python
sum(i*i for i in range(10))                 # 平方和
285

xvec = [10, 20, 30]
yvec = [7, 5, 3]
sum(x*y for x,y in zip(xvec, yvec))         # ドット積
260
```

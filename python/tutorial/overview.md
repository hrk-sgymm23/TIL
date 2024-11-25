# Python Tutorialの実施
https://docs.python.org/ja/3/tutorial/

# 3. 形式ばらない Python の紹介¶

> スライスの使い方をおぼえる良い方法は、インデックスが文字と文字の あいだ (between) を指しており、最初の文字の左端が 0 になっていると考えることです。
> そうすると、 n 文字からなる文字列中の最後の文字の右端はインデックス n となります。例えばこうです:
```bash
 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
 0   1   2   3   4   5   6
-6  -5  -4  -3  -2  -1
```

## **上記配列に対して直接アクセスすると**
```bash
word[42]  # the word only has 6 characters
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: string index out of range
```

## **スライス`[:]`でアクセスすると範囲外でもエラーにならない**
```bash
word[4:42]
'on'
word[42:]
''
```

# 4.2. for 文
> コレクションオブジェクトの値を反復処理をしているときに、そのコレクションオブジェクトを変更するコードは理解するのが面倒になり得ます。
> そうするよりも、コレクションオブジェクトのコピーに対して反復処理をするか、新しいコレクションオブジェクトを作成する方が通常は理解しやすいです:

```python
# コレクション作成
users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

# 方針:  コピーを反復
for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]

# 方針:  新コレクション作成
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status
```

# 4.9.3.4 関数の例

```python
def standard_arg(arg):
    print(arg)

def pos_only_arg(arg, /):
    print(arg)

def kwd_only_arg(*, arg):
    print(arg)

def combined_example(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)
```

## `standard_arg`はどちらでも指定可能

```python
standard_arg(2)
2

standard_arg(arg=2)
2
```

## pos_only_arg は、 / が関数定義にあるので、引数は位置専用になります:

```python
>>> pos_only_arg(1)
1
>>> pos_only_arg(arg=1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: pos_only_arg() got some positional-only arguments passed as keyword arguments: 'arg'
```

## kwd_only_argはキーワード引数のみ受け付ける

```python
>>> kwd_only_arg(3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: kwd_only_arg() takes 0 positional arguments but 1 was given
>>> kwd_only_arg(arg=3)
3
```

## 最後の関数は3つの引数の種類を一つの関数定義の中で使用しています

```python
>>> combined_example(1, 2, kwd_only=3)
1 2 3
>>> combined_example(1, standard=2, kwd_only=3)
1 2 3
>>> combined_example(pos_only=1, standard=2, kwd_only=3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: combined_example() got some positional-only arguments passed as keyword arguments: 'pos_only'
```

# 4.9.6 ラムダ式
```python
def make_incrementor(n):
    return lambda x: x + n

f = make_incrementor(42)

print(f(-1))
```

リスト各要素を2倍に
```python
>>> numbers = [1, 2, 3, 4, 5]
>>> doubled = list(map(lambda x: x * 2, numbers))
>>> print(doubled)
[2, 4, 6, 8, 10]
```

`make_incrementor`関数
make_incrementorは、引数nを取り、lambda x: x + nというラムダ関数を返します。
このラムダ関数は、引数xを取り、x + nの結果を返します。
つまり、make_incrementor(n)を呼び出すと、xにnを加える関数が生成され、それを返します。






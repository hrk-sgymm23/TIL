# データ構造

https://docs.python.org/ja/3/tutorial/datastructures.html

# `append`と`extend`の違い

```python
a = [1, 2, 3]
a.append([4, 5, 6])  # appendを使用
print(a)  # 出力: [1, 2, 3, [4, 5, 6]]

a = [1, 2, 3]
a.extend([4, 5, 6])  # extendを使用
print(a)  # 出力: [1, 2, 3, 4, 5, 6]
```

## 5.1.3 リスト内包表記

平方のリストを作成する

通常の書き方
```python
>>> squares = []
>>> for x in range(10):
...     squares.append(x**2)
...
>>> squares
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

リスト内包表記
```python
squares = [x**2 for x in range(10)]
```

リスト内包表記は括弧の中の式、for、そして0個以上のforかifで構成される

下記の式はどちらも等価である

```python
[(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
[(1, 3), (1, 4), (2, 3), (2, 1), (2, 4), (3, 1), (3, 4)]
```

```python
combs = []
for x in [1,2,3]:
    for y in [3,1,4]:
        if x != y:
            combs.append((x, y))

combs
[(1, 3), (1, 4), (2, 3), (2, 1), (2, 4), (3, 1), (3, 4)]
```

## 5.1.4. ネストしたリストの内包表記


長さ4のリスト3つからなる、3x4 の matrix について考える
```python
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]
```

下のリスト内包表記は、matrix の行と列を入れ替える
```python
[[row[i] for row in matrix] for i in range(4)]
[[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
```

下記コードと等価になる
```python
transposed = []
for i in range(4):
    # the following 3 lines implement the nested listcomp
    transposed_row = []
    for row in matrix:
        transposed_row.append(row[i])
    transposed.append(transposed_row)

transposed
```

備考`zip`関数
```python
>>> for item in zip([1, 2, 3], ['sugar', 'spice', 'everything nice']):
...     print(item)
...
(1, 'sugar')
(2, 'spice')
(3, 'everything nice')
```

```pyhon
>>> list(zip(range(3), ['fee', 'fi', 'fo', 'fum']))
[(0, 'fee'), (1, 'fi'), (2, 'fo')]
```

## 5.2 del

リストのインデックスを指定して値を削除する
返り値はない
```python

>>> a = [-1, 1, 66.25, 333, 333, 1234.5]
>>> del a[0]
>>> a
[1, 66.25, 333, 333, 1234.5]
>>>
>>> del a[2:4]
>>> a
[1, 66.25, 1234.5]
>>>
>>> del a[:]
>>> a
[]

```

# 5.5. 辞書型 (dictionary)

`dict()`コンストラクタ

```python
dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
{'sape': 4139, 'guido': 4127, 'jack': 4098}
```

リスト内包表記を使って辞書を作成可能

```python
{x: x**2 for x in (2, 4, 6)}
{2: 4, 4: 16, 6: 36}
```

キーワード引数
```python
dict(sape=4139, guido=4127, jack=4098)
{'sape': 4139, 'guido': 4127, 'jack': 4098}
```

# 5.6. ループのテクニック

辞書に対し`items()`メソッドを使うとキーとそれに対応するため値を取り出せる

```python
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print(k, v)

gallahad the pure
robin the brave
```

配列に対し`enumerate()`を使うと要素とインデックスを取り出せる
```python
for i, v in enumerate(['tic', 'tac', 'toe']):
    print(i, v)

0 tic
1 tac
2 toe
```

シーケンスを逆方向に渡ってループするには、まずシーケンスの範囲を順方向に指定し、`reversed()`を使う。

```python
for i in reversed(range(1, 10, 2)):
    print(i)

9
7
5
3
1
```

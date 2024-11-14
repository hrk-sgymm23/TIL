# 7. 入力と出力

# 7.1.2. 文字列の `format()` メソッド

`str.format()`

`{}`を引数の値に置き換えられる

```python
print('We are the {} who say "{}!"'.format('knights', 'Ni'))
We are the knights who say "Ni!"
```

```python
print('{0} and {1}'.format('spam', 'eggs'))
spam and eggs
print('{1} and {0}'.format('spam', 'eggs'))
eggs and spam
```

# `*`,`**`可変長引数の使い方(`*args`,`**kwsrgs`)

https://note.nkmk.me/python-args-kwargs-usage/

# `*`(`*args`)

引数を可変長にできる
```python
def my_sum2(*args):
    print('args: ', args)
    print('type: ', type(args))
    print('sum : ', sum(args))

my_sum2(1, 2, 3, 4)
# args:  (1, 2, 3, 4)
# type:  <class 'tuple'>
# sum :  10
```

## `**`(`**kwargs`)

複数のキーワード引数を辞書として受け取る

```python
def func_kwargs(**kwargs):
    print('kwargs: ', kwargs)
    print('type: ', type(kwargs))

func_kwargs(key1=1, key2=2, key3=3)
# kwargs:  {'key1': 1, 'key2': 2, 'key3': 3}
# type:  <class 'dict'>
```

# 7.2. ファイルを読み書きする

> open() は file object を返します。大抵、 open(filename, mode, encoding=None) のように2つの位置引数と1つのキーワード引数を伴って呼び出されます。

```python
f = open('workfile', 'w', encoding="utf-8")
```

> ファイルオブジェクトを扱うときに with キーワードを使うのは良い習慣です。 その利点は、処理中に例外が発生しても必ず最後にファイルをちゃんと閉じることです。 with を使うと、同じことを try-finally ブロックを使って書くよりずっと簡潔に書けます:
`with`を使うと自動で`close`が行われる
```python
with open('workfile', encoding="utf-8") as f:
    read_data = f.read()

# We can check that the file has been automatically closed.
f.closed
True
```

# 7.2.2. json による構造化されたデータの保存

> 文字列表現からデータを再構築することは、デシリアライズ (deserializing) と呼ばれます。シリアライズされてからデシリアライズされるまでの間に、オブジェクトの文字列表現はファイルやデータの形で保存したり、ネットワークを通じて離れたマシンに送ったりすることができます。

`json.dumps()`

```python
import json
x = [1, 'simple', 'list']
json.dumps(x)
'[1, "simple", "list"]'
```




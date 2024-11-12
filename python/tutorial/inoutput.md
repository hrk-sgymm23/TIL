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

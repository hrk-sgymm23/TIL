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

~match文まで





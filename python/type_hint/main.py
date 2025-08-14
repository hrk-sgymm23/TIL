# 参考: https://libroworks.co.jp/?p=5420

"""
関数
"""

num: int = 10

def cal_total(num: int) -> int:
    return num * 2

print('cal_total result:',cal_total(num))

"""
リスト,辞書,タプル
"""

num_list: list[int] = [1, 2, 3, 4, 5]

price_dict: dict[str, int] = {
    'apple': 100,
    'banana': 200,
    'orange': 300
}

price_tuple: tuple[int, str, bool] = (100, 'apple', True)

print('num_list:',num_list)
print('price_dict:',price_dict)
print('price_tuple:',price_tuple)

"""
クラス
"""

class User:
    def __init__(self, name: str, age: int):
        self.name = name

"""
mypy
"""

num: int
num = 'Hello'

"""
type_hint/main.py:45: error: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]
Found 2 errors in 1 file (checked 1 source file)
"""

print('cal_total result:',cal_total('みかん'))

"""
type_hint/main.py:52: error: Argument 1 to "cal_total" has incompatible type "str"; expected "int"  [arg-type]
"""

"""
mypyの設定

mypy.iniファイルを作成する
[mypy]
python_version = 3.10
disallow_untyped_defs = True

上記設定をすると型ヒントがない際にエラーが発生する
"""

def cal_total2(num):
    return 200 * num

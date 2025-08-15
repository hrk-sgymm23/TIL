# 参考: https://zenn.dev/yosemat/books/1e021f1745566f/viewer/50516a

"""
基本
"""

def add(a: int, b: int):
    return a + b

c = add(3, 4)


"""
いろいろなtypehint
"""
# from struct import unpack
from typing import TypedDict, Unpack

class MyKWArgs(TypedDict):
    x: int
    y: int

def do_something(
    a: int, 
    b: float = 1.1,
    *args: int,
    **kwargs: Unpack[MyKWArgs]
):
    print(a)
    print(b)
    print(args)
    print(kwargs)

b = do_something(1, 2.0, 3, 4, 5, x=1, y=2)


def something(a: int):
    return a


# 下記のように型ヒントのない関数に型を書いてあげる
def do_something2(a: int) -> int:
    return something(a)

d = do_something2(3) 

def do_something3(a: int) -> float:
    # x: int
    # x = something(a)
    x: int = something(a)
    return x * 0.5

e = do_something3(5)

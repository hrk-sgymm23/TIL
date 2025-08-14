from typing import Final

"""
Finalを使うと上書き防止が可能
"""

hello: Final[str] = "Hello World"
hello = "Over Written!" 

"""
Protocolを使うと型ヒントを定義できる
"""

from typing import Protocol

class MyProtocol(Protocol):
    def hello(self) -> str:
        ...

class MyClass:
    def hello(self) -> str:
        return "Hello World"

def my_func(obj: MyProtocol) -> None:
    print(obj.hello())

my_func(MyClass())

"""
"""
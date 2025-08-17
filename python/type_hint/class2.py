# 参考: https://zenn.dev/yosemat/books/1e021f1745566f/viewer/62e363

"""
静的なクラス
"""

class StaticClass:
    def __init__(self):
        self.x = 1


"""
動的なクラス
メンバー変数が動的
基本動的なクラスは使わない
型推論できなくなる
"""
class DynamicClass:
    def __init__(self, val: int):
        if val % 2 == 0:
            self.x = 1
        else:
            self.y = 1

"""
静的なクラスのベストプラクティス

サポートするライブラリ
- dataclass
- pydantic
"""

"""
dataclass
"""

from dataclasses import dataclass

@dataclass
class Myclass:
    x: int
    y: float

    def cry(self):
        print(f"x: {self.x}, y: {self.y}")

Valid = Myclass(1, 2.0)
Invalid = Myclass(1.0, 2.0)


"""
- __init__メソッドの役割
  - メンバー変数を定義し代入する役割にとどめておく
  - なぜならインスタンスの初期化方法は一つとは限らず今後も増える可能性があるため
  もし初期化ロジックを複雑にしたい場合、classmethodとし処理を外出しする 
"""
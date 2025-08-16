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
dataclasss
"""




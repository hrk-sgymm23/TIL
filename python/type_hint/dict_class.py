"""
クラス替わりのdict
dictをconfigの代わりに使うと、データ構造をprintをしていちいち確認しなくてはならない点
また静的解析でキー管理ができないのもデメリット

> dictを使うべきときはあります。dictのキーが実行時までわからないときです。
> しかし大抵の場合はソースコードにconfig["batch_size"], config["learning_rate"]などと固定のキーを直書きしてあってどんなキーがdictに含まれるのかわかっています。
> そんなdictは静的クラスで代替してあげましょう。
"""


from dataclasses import dataclass

@dataclass
class Config:
    batch_size: int
    learning_rate: float
    model_name: str
    use_gpu: bool = True  # デフォルト値

    def __post_init__(self):
        # バリデーションを自分で実装する
        if self.batch_size < 1:
            raise ValueError("batch_size must be >= 1")
        if not (0 < self.learning_rate < 1):
            raise ValueError("learning_rate must be between 0 and 1")

# --- dictから生成例 ---
data = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "model_name": "resnet50",
    "use_gpu": True
}

config = Config(**data)
print(config)             # → Config(batch_size=32, learning_rate=0.001, model_name='resnet50', use_gpu=True)
print(config.batch_size)  # 属性アクセスが可能

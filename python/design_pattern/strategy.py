# 簡単なSimUDuckアプリから始まった
from abc import ABC, abstractmethod

class FlyBehavior(ABC):
    @abstractmethod
    def fly(self):
        pass

class QuackBehavior(ABC):
    @abstractmethod
    def quack(self):
        pass

# スーパークラスの定義
class Duck(ABC):

    fly_behavior: FlyBehavior
    quack_behavior: QuackBehavior

    def __init__(self):
        pass

    @abstractmethod
    def display(self):
        pass

    def perform_fly(self):
        self.fly_behavior.fly()
    
    def perform_quack(self):
        self.quack_behavior.quack()

    # カモが泳ぐ振る舞いの実装
    def swim(self):
        print("みんな泳ぐよ！")

    def set_fly_behavior(self, fb: FlyBehavior):
        self.fly_behavior = fb
    
    def set_quack_behavior(self, qb: QuackBehavior):
        self.quack_behavior = qb
    
class FlyWithWings(FlyBehavior):
    def fly(self):
        print("羽ばたいて飛ぶよ！")

class FlyNoWay(FlyBehavior):
    def fly(self):
        print("飛べないよ！")

class Quack(QuackBehavior):
    def quack(self):
        print("ガーガー！")

class Squeak(QuackBehavior):
    def quack(self):
        print("キューキュー！")

class MuteQuack(QuackBehavior):
    def quack(self):
        print("サイレント！")

class ModelDuck(Duck):
    def __init__(self):
        self.fly_behavior = FlyNoWay()
        self.quack_behavior = MuteQuack()

    def display(self):
        print('模型のカモなのだ')

class FlyLikeRocket(FlyBehavior):
    def fly(self):
        print("ロケットになります！")


if __name__ == "__main__":
    model = ModelDuck()
    model.perform_fly()

    model.set_fly_behavior(FlyLikeRocket())
    model.perform_fly()
from typing import Protocol

class FizzBuzzPresenter(Protocol):
    def present(self) -> None:
        pass

class FizzBuzz:
    def __str__(self) -> str:
        return "FizzBuzz"

    def present(self) -> None:
        print(self.__str__())

class Fizz:
    def __str__(self) -> str:
        return "Fizz"

    def present(self) -> None:
        print(self.__str__())

class Buzz:
    def __str__(self) -> str:
        return "Buzz"

    def present(self) -> None:
        print(self.__str__())

# FizzBuzzPresenterを直接返却できないため具体的な実装クラスを用意
class NumberPresenter:
    def __init__(self, number: int):
        self.number = number
    
    def present(self) -> None:
        print(self.number)

    # def print(self) -> None:  # 👈 presentを実装しない！
    #     print(self.__str__())

# class Selector:
#     @staticmethod
#     def select(count: int) -> FizzBuzzPresenter:
#         if count % 3 == 0:
#             return Fizz()
#         return NumberPresenter(count)

class Selector:
    @staticmethod
    def select(count: int) -> FizzBuzzPresenter:
        # 要約変数
        divisible_by_3 = count % 3 == 0
        divisible_by_5 = count % 5 == 0

        if divisible_by_3 and divisible_by_5:
            return FizzBuzz()
        elif divisible_by_3:
            return Fizz()
        elif divisible_by_5:
            return Buzz()
        else:
            return

print(Selector.select(3))
print(Selector.select(5))
print(Selector.select(15))
print(Selector.select(34))

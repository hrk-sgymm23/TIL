def can_drink(age):
    if not isinstance(age, int):
        return "Invalid age."
    if (age < 0):
        return "You are not born yet."
    if (age < 20):
        return "You cannot drink."
    # いずれも一致しない場合のデフォルトの戻り値を最後の記述する
    return "You can drink."

age = 23
result = can_drink(age)
print(result)
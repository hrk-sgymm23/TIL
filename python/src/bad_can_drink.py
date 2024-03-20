# - 年齢（age）をもとに飲酒できるかどうかを判定する
#  - 年齢が0未満の場合は「You are not born yet.」と出力
#  - 年齢が0以上20未満の場合は「You cannot drink.」と出力
#  - 年齢が20以上の場合は「You can drink.」と出力
#  - 年齢が数字以外の場合は「Invalid age.」と出力

age = "23"

if isinstance(age, int):
    if (age < 0):
        print("You are not born yet.")
    elif (0 <= age and age < 20 ):
        print("You cannot drink.")
    else:
        print("You can drink.")
else:
    print("Invalid age.")
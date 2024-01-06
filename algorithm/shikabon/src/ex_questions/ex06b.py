# 範囲for文を使った回答
N = int(input())
A = list(map(int, input().split()))

count = 0

# Aの要素全てが偶数(正)である場合は処理を行う
while all(a % 2 == 0 for a in A):
    # 各要素を2でわり配列を更新
    A = [a // 2 for a in A]
    count += 1

print(count)
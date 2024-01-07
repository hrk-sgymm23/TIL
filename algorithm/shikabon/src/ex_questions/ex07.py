N = int(input())
A = list(map(int, input().split()))

# 問題として2人が大きいカードを取る戦略を取ったときとあるため、
# 大きい順にソートし交互とることを表現する
A.sort(reverse=True)
result = 0

# 今回求めるものは二人が取った値の差のため足しひきを要素分行う
for i in range(N):
    if i % 2 == 0:
        result += A[i]
    else:
        result -= A[i]

print(result)
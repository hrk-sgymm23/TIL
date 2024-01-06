# 06,06bでは要素によって割り切れる回数が異なる場合、最小回数がボトルネックになる
# 以上のことからNこの整数N1,N2,N3,,,に対してそれぞれ　2で何回われるかを求める。
# その最小値が答えになる

# 要素を一つずつ計算し、割り算できる回数を求める
def how_many_times(n):
    count = 0

    while n % 2 == 0:
        n //= 2
        count += 1

    return count

# tips: 一般に何らかの最小値を求める問題の際は初期値を大きい値にしておくと便利
INF = 2 ** 30
N = int(input())
A = list(map(int, input().split()))

result = INF

for a in A:
    count = how_many_times(a)
    # how_many_timesにて求めた値が以前how_many_timesで求めた値より小さければresult更新
    result = min(result, count)

print(result)





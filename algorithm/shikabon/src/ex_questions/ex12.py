# num[v] ...配列の中の値vの個数
# 以上のように定義される新しい配列をバケットと呼ぶことがある

# N個の整数 d0,d1,d2...dn-1に対して
# exist[v]...値vが含まれるならば1,含まれないならば0とする

# 制約としてd<=100のため
M = 101

N = int(input())

# 配列の要素数をあらかじめ決める
exist = [0] * M

for i in range(N):
    d = int(input())
    # バケット更新
    exist[d] = 1

print(exist)
print(sum(exist))
# a0+a1>xならば、a1をa0+a1-xだけ減らしてa0+a1=xとなるようにする
# そうでなければ何もしない
# 上記により「a0+a1<=x」が満たされた正体になる
# a0を除いたN-1個の整数a1,a2,...aN-1に対して全く同様の議論ができる
# a1+a2>xならば、a2をa1+a2-xだけ減らしてa1+a2=xとなるようにする
# そうでなければ何もしない

# まとめ
# a0>xならばa0=xとする
# 各i=0,1,...,N-2に対して
# ai+a(i+1)>xならばa(i+1)をai+a(i+1)-xだけ減らす

N, x = map(int, input().split())
a = list(map(int, input().split()))

result = 0

# a0>xならばa0=xとする
if a[0] > x:
    result += a[0] - x
    a[0] = x

for i in range(N-1):
    # ai+a(i+1)>xならばa(i+1)をai+a(i+1)-xだけ減らす
    if a[i] + a[i+1] > x:
        result += a[i] + a[i+1] - x
        # 横並びの後に来る値を更新
        a[i+1] = x - a[i]

print(result)
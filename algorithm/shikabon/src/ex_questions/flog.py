INF = 2 ** 60

N = int(input())
h = list(map(int, input().split()))

dp = [INF] * N

dp[0] = 0

for i in range(N):
    # 頂点i-1まで最短経路で行ってから、頂点iへと至る方法の最小コスト
    if i - 1 >= 0:
        dp[i] = min(dp[i], dp[i-1] + abs(h[i]-h[i-1]))
    # 頂点i-2まで最短経路で行ってから、頂点iへと至る方法の最小コスト
    if i - 2 >= 0:
        dp[i] = min(dp[i], dp[i-2] + abs(h[i]-h[i-2]))

print(dp[N-1])

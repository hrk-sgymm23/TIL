# A,C,G,Tからなる長さNの文字列Sが与えられる Qこのクエリに答えよ
# クエリ...整数li,riが与えられる。文字列Sのli文字目からri文字目までに部分文字列’AC’が何回登場する考える

# 例　
# a[i] S[i-1]がA、S[i]がCの時、１それ以外の時は0 ただしa[0]=0とする
# 文字列S TTACTTACTT
# 配列a  0,0,0,1,0,0,0,1,0,0

N, Q = map(int, input().split())
S = input()

# 累積和を求める
cs = [0] * (N+1)
for i in range(1,N):
    # インデックス0の値は処理しないためi+1
    cs[i + 1] = cs[i] + (S[i-1:i+1] == "AC")
# 入力例の場合　[0, 0, 1, 1, 2, 2, 2, 3, 3]
print(cs)

for q in range(Q):
    # 区間を取得
    l, r = map(int, input().split())
    # 右端に1を足して添字を0始まりにする
    l -= 1

    print(cs[r] - cs[l+1])
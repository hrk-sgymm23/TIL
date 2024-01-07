# 500円玉の枚数は0,1..AのA+1通り
# 100円玉の枚数は0,1..AのB+1通り
# 50円玉の枚数は0,1..AのC+1通り
#(A+1)(B+1)(C+1)通りを三重のfor文で表す
A = int(input())
B = int(input())
C = int(input())
X = int(input())

result = 0

# 500 * a + 100 * b + 50 * c == Xが成り立つ組み合わせを全探索で求める
for a in range(0, A + 1):
    for b in range(0, B + 1):
        for c in range(0, C + 1):
            if 500 * a + 100 * b + 50 * c == X:
                result += 1

print(result)



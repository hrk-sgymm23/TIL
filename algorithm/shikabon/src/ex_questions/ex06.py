N = int(input())
A = list(map(int, input().split()))

count = 0

# can_calcがTrueであるかぎり処理を行う
while True:
    can_calc = True
    # 与えられた配列の要素が全て偶数であるか確かめる
    for i in range(N):
        if A[i] % 2 == 1:
            can_calc = False

    if not can_calc:
        break

    for i in range(N):
        # //は小数点まで商を出さない　 5//2=2
        A[i] // 2
    
    ++count;

print(count)
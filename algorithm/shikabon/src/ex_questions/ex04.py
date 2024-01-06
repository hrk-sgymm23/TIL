K, A, B = map(int, input().split())

flag = False
for i in range(A, B + 1):
    if i % K == 0:
        flag = True

print("OK" if flag else "NG")

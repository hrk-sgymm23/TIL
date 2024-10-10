# https://www.hackerrank.com/challenges/py-set-union/problem?isFullScreen=true

# pythonのsetについて
# https://note.nkmk.me/python-set/

n = int(input())

eng_people = set(input().split())

b = int(input())

fra_people = set(input().split())

print(len(eng_people.union(fra_people)))

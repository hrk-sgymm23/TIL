# https://www.hackerrank.com/challenges/py-set-difference-operation/problem?isFullScreen=true

n = int(input())

eng_people = set(input().split())

b = int(input())

fra_people = set(input().split())

print(len(eng_people.difference(fra_people)))

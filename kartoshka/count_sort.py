n = int(input())
a = [0] * 11

in_list = [int(x) for x in input().split()]

for i in in_list:
    a[i] += 1

answer = ''
for i in range(10):
    answer += (str(i) + ' ') * a[i]
print(answer)

a = [1,2,3,4,5,6,7,8]
c = [1,3,4]
b=[a[i] for i in range(len(a)) if i in c]

print(a)
print(b)
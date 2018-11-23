sum = 0
x = 1
while x <= 100:
    sum += x*x
    x += 1
print(sum)

sum2 = 0
y = 1
while y <= 100:
    sum2 += y
    y += 1
sum2 *= sum2
print(sum2)

sum3 = sum2 - sum
print(sum3)
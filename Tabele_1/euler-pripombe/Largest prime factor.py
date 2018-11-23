x = 600851475143 
i = 2
while x > 1:
    if x % i == 0:
        x = x / i
        maxprime = i
    i += 1
print(maxprime)
    
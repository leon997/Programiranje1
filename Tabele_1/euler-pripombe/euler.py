# multiplies of 5 and 3
# problem 1
sestej = 0
stej = 1
while stej <= 1000:
    if stej % 3 == 0 and stej % 5 == 0:
        sestej += stej
    stej += 1
print(sestej)

# even fibonacci numbers
# problem 2

def fibonacci(n):
    '''Vrne n-ti člen Fibonaccijevega zaporedja 0, 1, 1, 2, 3, 5, 8…'''
    if n == 0:
        odgovor = 0
    elif n == 1:
        odgovor = 1
    else:
        odgovor = fibonacci(n - 1) + fibonacci(n - 2)
    return odgovor

print(fibonacci(10))
def vsota_soda(n):
    '''vsoa sodih stevil zaporedja do n člena'''
    stej = 0
    vsota = 0
    fib_ste = 1
    while fib_ste <= n:
        if fib_ste % 2 == 0:
            vsota += fib_ste
        stej += 1
        fib_ste = fibonacci(stej)
    return vsota
print(vsota_soda(4000000))

# largest rime number
# problem 3
import math
def je_prastevilo(n):
    '''pove če je n praštevilo'''
    if n == 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    else:
        return True


delitelj = 1
stevilka = 2
stevilo = 600851475143
while stevilka < math.sqrt(stevilo):
    if stevilo % stevilka == 0:
        if delitelj < stevilka and je_prastevilo(stevilka) :
            delitelj = stevilka
    stevilka += 1
print (delitelj)
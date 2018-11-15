#If we list all the natural numbers below 10 that are multiples of 3 or 5,
# we get 3, 5, 6 and 9. The sum of these multiples is 23.
#Find the sum of all the multiples of 3 or 5 below 1000.

def multiples_sum():
    """
    Vrne vsoto vseh večkratnikov števil 3 ali 5,
    ki so manjši od 1000
    """
    vsota = 0

    for i in range(0, 1000):
        if i % 3 == 0 or i % 5 == 0:
            vsota += i
    print(vsota)

multiples_sum()

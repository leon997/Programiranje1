#The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
#Find the sum of all the primes below two million.

def vsota_praštevil(omejitev):
    """
    vrne vsoto vseh praštevil manjših od 2000000
    """
    praštevila = []
    for n in range(2, omejitev+1):
        for p in praštevila:
            if n % p == 0: break     
            if n < p*p:
               praštevila.append(n)
               break
        else:
            praštevila.append(n)       
    return sum(praštevila)

print(vsota_praštevil(1999999))
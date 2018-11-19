#The prime factors of 13195 are 5, 7, 13 and 29.
#What is the largest prime factor of the number 600851475143 ?

def največji_prafaktor():
    """
    fun vrne največji prafaktor št 600851475143
    """
    največji = 0
    število = 600851475143
    delitelj = 2
    
    while delitelj * delitelj <= število:
        while število % delitelj == 0:
            največji = delitelj
            število = število / delitelj
        delitelj += 1
    if število > 1:
        return število
    return največji

print(največji_prafaktor())
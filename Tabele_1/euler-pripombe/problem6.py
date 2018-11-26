def razKvadratov():
    '''vrne razliko vsote kvadratov in kvadratov vsote'''
    i = 1
    x, y, y1 = 0, 0, 0
    while i <= 100:
        x = x + pow(i,2)
        y1 = y1 + i
        i += 1
    y = pow(y1,2)
    print(str(y-x))

razKvadratov()

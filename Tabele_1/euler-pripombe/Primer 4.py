max_pal = 0
for i in range(100,999):
    for j in range(100,999):
      mult = i * j 
      if str(mult) == str(mult)[::-1]: #preveri, če je število palindrom
          if mult > max_pal: 
              max_pal = mult
print (max_pal)
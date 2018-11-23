'''Seštevamo vsa števila, ki so deljiva s tri ali pet'''
i,skupno=0,0
while(i<1000):
    if(i%3==0 or i%5==0):
        skupno=skupno+i
    i += 1
print(skupno)
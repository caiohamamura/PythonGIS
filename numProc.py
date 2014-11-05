import os, time
point=[]
soma=0
for i in [i for i in os.listdir('D:/') if not i.find('points')]:
    a=open('D:/'+i,'r')
    soma-=1
    for j in a:soma+=1
print soma
# a.close()
# time.sleep(10)
# soma2=0
# for i in [i for i in os.listdir('D:/') if not i.find('savepoint')]:
    # a=open('D:/'+i,'r')
    # soma2-=1
    # for j in a:soma2+=1
# a.close()
# print (soma2-soma)/10.
# splitn = 10
# splitting = range(0,len(a),len(a)/splitn)
# splitting[-1] = len(a)
# AB1=numpy.concatenate([a[splitting[i]:splitting[i+1]]**2 for i in range(splitn)])
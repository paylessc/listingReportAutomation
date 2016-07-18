import csv

X = "856"
#X = input("Move from Box? : ") 
Y = "844"

def replace(l, a, b):
  for i,v in enumerate(l):
     if v == a:
        l.pop(i)
        l.insert(i, b)

fib1 =open("Box"+X+".csv")
fi_b1 = csv.reader(fib1)
next (fi_b1)

fob1 = open("Box"+X+" to "+Y+".csv",'w')
fo_b1 = csv.writer(fob1)
fo_b1.writerow(["SKU","BinRack"])

for row1 in fi_b1:
    
    BinRack1 = row1[1].split(",")

    cnt = 0
    for item in BinRack1:
        if item.startswith(X):
            if item.find('(')!=-1 or len(item)==len(X):
                item1 = Y+item.split(X)[1] 
                replace(BinRack1, item, item1)
            
    for item in BinRack1:
        if item.startswith(Y):
            if item.find('(')==-1:
                cnt = cnt + 1
            else:    
                cnt = cnt + int(item.split("(")[1].split(")")[0])
    
    dup = True
    idx = 0
    for item in BinRack1:
        if item.startswith(Y):
            if (dup) :
                if cnt == 1:
                    item1 = Y
                else:
                    item1 = Y+"("+str(cnt)+")"
                replace(BinRack1, item, item1)
                dup = False
            else:
                BinRack1.pop(idx)
        idx += 1  
        
    newBinRack1 = ",".join(BinRack1)  

    row1.pop()
    row1.append(newBinRack1)
    
    fo_b1.writerow(row1)

fob1.close()
fib1.close()  
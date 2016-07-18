import csv
import re
import itertools
                
fib1 = open("QueryData.csv", "r")
fi_b1 = csv.reader(fib1)
next (fi_b1)

fob1 = open("QueryData_out.csv", "w")
fo_b1 = csv.writer(fob1)

feb1 = open("QueryData_err.csv", "w")
fe_b1 = csv.writer(feb1)

for row1 in fi_b1:
    
    if row1[21] != "":
      
        BinRack1 = row1[21].split(",")
            
        for item in BinRack1:
        
            row2 = []
            binRack = False
            
            if item.find('(')==-1:
                boxNum = item
                brdcnt = 1
            else:
                boxNum = item.split("(")[0]
                brdcnt = item.split("(")[1].split(")")[0]
                    
            if boxNum == "":
                row2.append("Has Extra Comma ")           
                
            elif boxNum.find(".") != -1:
                row2.append("Has DOT ")
                
            elif boxNum.find(" ") != -1:
                row2.append("Has BLANK ")
                
            elif brdcnt == "":
                row2.append("Has extra '(' ")                
                
            #elif (boxNum.isalpha()):
            #    row2.append("Special Box ")
                                        
            else:
            
                binRack = True
                
                                                
                if (boxNum.isdigit() == False):

                    l = re.search(r'^[L,M,S,l,m,s][1-9][0-9]{2}', boxNum)

                    m = re.search(r'\d+$', boxNum)

                    if l is not None:
                        if len(boxNum) > 4:
                            binRack = False
                            row2.append("Missing Comma ")
                  
                    # if the string ends in digits m will be a Match object, or None otherwise.
                    elif m is not None:
                        
                        Num = m.group()
                        if boxNum[0].isalpha() and boxNum[1].isalpha() and len(Num) > 2:
                            binRack = False
                            row2.append("Missing Comma ")
                        elif boxNum[0].isalpha() and len(Num) > 3:
                            binRack = False
                            row2.append("Missing Comma ")
   
                elif len(boxNum) > 3:
                    binRack = False
                    row2.append("Missing Comma ")    

            if (binRack):
                row2.append(boxNum.upper())
                row2.append(brdcnt)
                row2.append(row1[0])
                fo_b1.writerow(row2)
            else:
                row2.append(row1[0])
                row2.append(boxNum)
                row2.append(row1[21])
                fe_b1.writerow(row2)
          
fib1.close()
fob1.close()
feb1.close()
            
f = open("QueryData_out.csv", "r")
lines = [line for line in f if line.strip()]
f.close()
lines.sort()

f = open('QueryData_out.csv', 'w')
f.writelines(lines)
f.close()

f = open("QueryData_err.csv", "r")
lines = [line for line in f if line.strip()]
f.close()
lines.sort()

f = open('QueryData_err.csv', 'w')
f.writelines("Issue/Comment,SKU,BoxNum,BinRack")
f.writelines('\n')
f.writelines(lines)
f.close()

with open('QueryData_out.csv') as input, open('QueryData_cnt.csv','w') as output:
    reader = csv.reader(input)
    writer = csv.writer(output)
    for boxNum, row in itertools.groupby(reader, lambda x: x[0]):
        boxlst = [int(x[1]) for x in row]
        boxcnt = sum(boxlst)
        writer.writerow([boxNum, boxcnt])

f = open("QueryData_cnt.csv", "r")
lines = [line for line in f if line.strip()]
f.close()
lines.sort()

f = open('QueryData_cnt.csv', 'w')
f.writelines("BinRack,Count")
f.writelines('\n')
f.writelines(lines)
f.close()


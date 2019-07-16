import pandas as pd
import csv
from collections import defaultdict
from random import randint

        
            
def add(s,mylist):
    
         with open("Scraped-Data/dataset_uncleaned.csv") as csvfile:
                    reader = csv.reader(csvfile)
            
                    l=len(mylist)
                    l=l-1
                    ss=mylist[0]
                   # print(l)
                    for num, row in enumerate(reader):
                            if ss in row[2]:
                                ss=row[2]
                                break
                            else:
                                    r=randint(1000000,9999999)
                                    ss='UMLS:C'
                                    for i in range(1):
                                        h=r
                                        ss+=str(h)
                                        ss+='_'
                                        ss+=mylist[0]     
                                
                    s='UMLS:C0011847_'+s           
                    row = [s,43,ss]  
                    with open('Scraped-Data/dataset_uncleaned.csv', 'a',newline="") as csvFile:
                            writer = csv.writer(csvFile)
                            writer.writerow(row)
                    csvFile.close()
                    rowlist=[]
                    k=1
                    for i in range(l):
                            for num, row in enumerate(reader):
                       
                                if mylist[i+1] in row[2]:
                                    ss=row[2]
                                    #print(ss)
                                   # break
                            if mylist[i+1] not in row[2]:
                                r=randint(1000000,9999999)
                                ss='UMLS:C'
                                #for i in range(l):
                                h=r
                                ss+=str(h)
                                ss+='_'
                                ss+=mylist[k]
                                #print(ss)
                                k=k+1
                                #print(k)
                                        
                           
                            rowlist.append(ss)
                    ll=len(rowlist)
                    
                    for i in range(ll):
                            row = ['','',rowlist[i]]
                            with open('Scraped-Data/dataset_uncleaned.csv', 'a',newline="") as csvFile:                                   
                                    writer = csv.writer(csvFile)
                                    writer.writerow(row)
                            csvFile.close()
 

           
            
# s="samir"
# mylist=["abaas","ibrahim","suad","mamdoh"]
# modify(s,mylist)


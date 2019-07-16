import pandas as pd
import numpy as np
from pandas import DataFrame
import prediction2

def fillter1(s):
    nt_data = pd.read_csv("Scraped-Data/test2.csv", encoding ="ISO-8859-1",)
    df = pd.DataFrame(nt_data)
    
    try:    
        df_filtered = df[ (df[s[0]]== 1) & (df[s[1]]== 1) ]
        mylist=df_filtered.columns[(df_filtered == 1).iloc[0]]
        mylist2=[]
        mylist2 = mylist.values.tolist()
        mylist3=list(set(mylist2)-set(s))
        l=len(mylist3)
        for i in range(l):
          mylist3[i] = mylist3[i].replace('Â', '') 
          mylist3[i] = mylist3[i].replace('Ã', '') 
          mylist3[i] = mylist3[i].replace('\xa0', ' ')
          mylist3[i] = mylist3[i].replace('\x82', '')
        if not mylist3:
          return s,[]
        else:
          return mylist3,[]
    except: 
        df_filtered = df[(df[s[0]]== 1)]
        mylist2=[]
        mylist=df_filtered.columns[(df_filtered == 1).iloc[0]] 
        mylist2 = mylist.values.tolist()
        mylist3=list(set(mylist2)-set(s))
        
        s1=mylist3[0]
        df_filtered = df[(df[s[1]]== 1)]
        
        mylist4=[]
        mylist=df_filtered.columns[(df_filtered == 1).iloc[0]] 
        mylist4 = mylist.values.tolist()
        mylist5=list(set(mylist4)-set(s))
        
        s2=mylist5[0]
        mylist6=[]
        mylist7=[]
        mylist6.append(s1)
        mylist6.append(s[0])
  
        mylist7.append(s2)
        mylist7.append(s[1])
        
        return mylist6,mylist7


def fillter3(s):
  nt_data = pd.read_csv("Scraped-Data/test2.csv", encoding ="ISO-8859-1",)
  df = pd.DataFrame(nt_data)
  df_filtered = df[(df[s[0]]== 1)]
  mylist=df_filtered.columns[(df_filtered == 1).iloc[0]]
  mylist2=[]
  mylist2 = mylist.values.tolist()
  mylist3=list(set(mylist2)-set(s))
  l=len(mylist3)
  for i in range(l):
    mylist3[i]= mylist3[i].replace('Â', '')
    mylist3[i]= mylist3[i].replace('Ã', '')
    mylist3[i]= mylist3[i].replace('\xa0', ' ')
    mylist3[i]= mylist3[i].replace('\x82', '')
  if not mylist3:
    return s,[]
  else:  
    return mylist3,[]



def fillter(mylist):
  try:
    mylist3 = fillter1(mylist)
    return mylist3
  except:
    prediction2.predict(mylist)
    return fillter3(mylist)

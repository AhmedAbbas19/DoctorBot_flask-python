import Data_Analysis
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier

def predict(mylist3):
    data=Data_Analysis.analysis()
    
    df_pivoted=Data_Analysis.analysis2(data)
    df_pivoted.to_csv("Scraped-Data/test2.csv")
    
    cols = df_pivoted.columns
    cols = cols[1:]
    x = df_pivoted[cols]
    y = df_pivoted['Source']
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42) 
    mnb = MultinomialNB()
    mnb = mnb.fit(x_train, y_train)
    mnb.score(x_test, y_test)
    
    mnb_tot = MultinomialNB()
    mnb_tot = mnb_tot.fit(x, y)
    
    disease_pred = mnb_tot.predict(x)
    disease_real = y.values
    
    dt = DecisionTreeClassifier()
    clf_dt=dt.fit(x,y)
    
    features = cols
    
    temp=[]
    count=0
    feature_dict = {}
    for i,f in enumerate(features):
        feature_dict[f] = i
        
    l=len(mylist3)
    
    for i in range(l):
        sym = mylist3[i].replace('Ã','')
        sym = sym.replace('Â','')
        sym = sym.replace('\xa0',' ')
        sym = sym.replace('\x82','')
        v=feature_dict[sym]
        sample_x = [i/v   if i ==v else i*0 for i in range(len(features))]
        temp.append(v)
    
    for i in temp:
        count=count+1
    for j in range(count):    
       del sample_x[temp[j]]     
       sample_x.insert(temp[j],1)       
    
    sample_x = np.array(sample_x).reshape(1,len(sample_x))
    
    return
import Question_Maker
import Prediction
 
def run(mylist3):
    mypre=[]
    mypre2=[]
    for i in range(20):
       p=Prediction.predict(mylist3)
       mypre2.append(p)
       if p not in mypre:
           mypre.append(p)
            
    l=len(mypre)
    mypre = [' '.join(item) for item in mypre]
    mypredict = []
    for i in range(l):
        disease = mypre[i].replace('Â', '')
        disease = disease.replace('Ã','')
        disease = disease.replace('\xa0',' ')
        disease = disease.replace('\x82','')
        mypredict.append(disease)
    
    return mypredict
import pandas as pd
import numpy as np
from difflib import get_close_matches
import sys

def closeMatches(word,patterns,thresh,du):
    result=get_close_matches(word,patterns,cutoff=thresh)
    l=[]
    #print(result)
    for r in result:
        for p in  du:
            if r in p.lower():
                l.append(p)
                break
    return l

def treatmentlist(sub,c):
    prescriptions=pd.merge(c,sub[['SUBJECT_ID','SEQ_NUM']],how='inner',on='SUBJECT_ID')
    d=prescriptions['DRUG_NAME_GENERIC'].value_counts()[:10]
    key=list(d.keys())
    print(key)
    result=pd.DataFrame()
    for k in key:
        result=result.append([prescriptions.loc[prescriptions['DRUG_NAME_GENERIC']==k,'STARTDATE':'SEQ_NUM'].iloc[0]])
        
    result=result.reset_index(drop=True)
    result.index+=1
    #print(result)
    result.to_csv('res.csv')
    
    return result

if __name__=='__main__':
    #inputdiag='Ludwigs angina - severe infection in the floor of the mouth and neck'
    inputdiag=sys.argv[1]
    a=pd.read_csv('d_icd_diagnoses.csv')
    b=pd.read_csv('DIAGNOSES_ICD.csv')
    c=pd.read_csv('PRESCRIPTIONS.csv')
    a=pd.DataFrame(a)
    b=pd.DataFrame(b)
    c=pd.DataFrame(c)
    result=pd.DataFrame()

     


    #print(a)
    #temp2=[i for i in ]
    temp=list(a['LONG_TITLE']) #.str.lower())  #if a['icd9_code'] in b['icd9_code'])
    #print(temp)
    if ',' in inputdiag:
        inputdiag=inputdiag.split(',')
        inputdiag=inputdiag[0]
    elif '-' in inputdiag:
        inputdiag=inputdiag.split('-')
        inputdiag=inputdiag[0]
    dt=inputdiag.lower().split( )
    #dt.reverse()
    #print(dt)

    l=len(dt)
    #inter=1/l
    thresh=0.4
    dset=set()
    dsetu=set()
    for i in range(l):
        for j in temp:
            if dt[i] in j.lower():
                dset.add(j.lower())
                dsetu.add(j)
    #diaglist1=[i for i in temp if dt[l-1] in i]
    #print(diaglist1,dt)
    diaglist=closeMatches(inputdiag ,dset,thresh,dsetu)
    print(diaglist)
    '''for wrd in dt:
        thresh+=thresh*inter
        tp=min(thresh,0.6)
        
        temp=closeMatches(wrd ,temp1,tp)
        
        print(temp)'''
    ind=-1
    diag_id=pd.DataFrame()
    #print(temp)
    if diaglist:
        ind=temp.index(diaglist[0])
    '''elif diaglist1:
        ind=temp.index(diaglist1[0])'''

    if ind!=-1:    
        diag_id=a.iloc[ind]
    #print(diag_id['icd9_code'])
    if not diag_id.empty:
        tid=diag_id['ICD9_CODE']
        #print(tid)
        #tid=str(53081)
        #print(b)
        #interdiag=pd.DataFrame()
        interdiag=b.loc[b['ICD9_CODE']==tid]
        #print(interdiag)
        result=treatmentlist(interdiag,c)

    if result.empty:
        print(0)
    else:
        print(1)
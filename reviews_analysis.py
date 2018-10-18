#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 10:41:22 2018

@author: sdic_lab
"""

import numpy as np

import scipy.stats as stat
import pandas as pd
import numpy as np
from IPython.core.display import display
import seaborn as sns
from gensim.summarization import keywords
from textblob import TextBlob
import gensim

import os



def chi2_compute(rate_l1,rate_l2):
    
    fr1 =  dict((x, 0) for x in range(1,6))

    for j in range(1,6):
        
        if j in set(rate_l1):
            fr1[j]=rate_l1.count(j)
    
    fr2 =  dict((x, 0) for x in range(1,6))
    
    for j in range(1,6):
        
        if j in set(rate_l2):
            fr2[j]=rate_l2.count(j)
            
    
    obs = np.array([[fr1[1],fr1[2], fr1[3], fr1[4],fr1[5]], [fr2[1], fr2[2], fr2[3], fr2[4], fr2[5]]])
    
    try:
      
       chi2, p = stat.chisquare(obs[0], f_exp = obs[1], ddof=1)
       
    except:
       obs = np.array([[fr1[2], fr1[3], fr1[4],fr1[5]], [ fr2[2], fr2[3], fr2[4], fr2[5]]])   
       chi2, p = stat.chisquare(obs[0], f_exp = obs[1], ddof=1)
    return p

    
def hotels_sort(ListsOfrates, ListOfnames, ListsOfReviews, ListsOfdates,locality):
    
    """ Sort the hotels based on the percentile ran of 4 and chi2 statistic """
    df_hotels = pd.read_csv(locality+'_tripadvisor_data.csv')
    N = len(df_hotels)

    tripadv_rates= df_hotels['tripadvisor_rating']
    
    
    rank = []   
    
    for rate in ListsOfrates:    
      
       rank.append(stat.percentileofscore(rate, 4))
       
    
    I= np.argsort(rank)    
    
    names = [ListOfnames[i] for i in I]
    reviews = [ListsOfReviews[i] for i in I]  
    dates = [ListsOfdates[i] for i in I]  
    rates = [ratesnew[i] for i in I]
    tripadv_s = [tripadv_rates[i] for i in I]
    
    L = [len(x) for x in rates]

    
    rank_s= np.sort(rank)
    c = []
    b = [(i,i+5) for i in range(0,100,5)]
    for r in b:
        
        l = []
        t=0
        rn = range(*r)
        for element in rank_s:
            if int(element) in rn:
                l.append(element)
                t=1
        if t:        
           c.append(l)
     
       

    rates_sn=[] 
    dates_sn =[]
    rank_sn=[]
    names_sn=[]
    P=[]
    reviews_sn = []
    tripadv_sn= []
    ind=0
    
    for ndx,K in enumerate(c):
       
       m= len(K) 
       
       p_values = []
       
       aux = rates[ind:ind+m]
       rank_aux=rank_s[ind:ind+m]
       L_aux = L[ind:ind+m]
       names_aux = names[ind:ind+m]
       reviews_aux= reviews[ind:ind+m]
       dates_aux = dates[ind: ind+m]
       tripadv_aux=  tripadv_s[ind:ind+m]
       
       ind_max = np.argmax(L_aux)
       
       
       rate_l1 = aux[ind_max]
       
       
       for rate_l2 in aux:
           
           p_values.append(chi2_compute(rate_l1,rate_l2))
       P.append(p_values)
           
       
       I1 = np.argsort(p_values)[::-1]
       for n in I1:
           rates_sn.append(aux[n])
           rank_sn.append(rank_aux[n])
           names_sn.append(names_aux[n])
           reviews_sn.append(reviews_aux[n])
           dates_sn.append(dates_aux[n])
           tripadv_sn.append(tripadv_aux[n])
        
       ind = ind+m
   
    return names_sn, rates_sn,  dates_sn, rank_sn, reviews_sn, tripadv_sn


def hotel_sentiment(reviews_hotel,threshold):
    
    """ Extract sentiments of features of a hotel using its text reviews; threshold serves to classify positive and negative statements """
    text =  ''.join(reviews_hotel)
    
    
    score_pos=[]
    score_neg=[]
    
    sent_pos = []
    sent_neg = []
    sc_pos=[]
    sc_neg=[]
    
    blob = TextBlob(text)
    
    for sentence in blob.sentences:
        sent = sentence.sentiment.polarity  
        
        if sent > threshold:
           sent_pos.append(sentence)
           sc_pos.append(sent)
          
           
        elif sent < threshold and sent !=0.0:
            sent_neg.append(sentence)
            sc_neg.append(sent)
          
    N = len(sent_pos)+len(sent_neg)
    perc_pos=float(len(sent_pos))/N
    perc_neg=float(len(sent_neg))/N 
    
    text = ''.join([str(x) for x in sent_pos])    
    keyp = keywords(text, words=15, scores=True,  pos_filter=('NN') , lemmatize=True)
    
    text = ''.join([str(x) for x in sent_neg]) 
    keyn =keywords(text, words=15, scores=True,  pos_filter=('NN') , lemmatize=True)
    
    keyp_list = [list(x) for x in keyp]
    
    keyn_list =  [list(x) for x in keyn]
    
    for j in range(0,len(keyp_list)):
                
            keyp_list[j][1]= keyp_list[j][1]*perc_pos
            
    for j in range(0,len(keyn_list)):
        
            keyn_list[j][1]= keyn_list[j][1]*perc_neg      

    
    return keyp_list, keyn_list
    

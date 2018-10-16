#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 15:30:48 2018

@author: sdic_lab
"""

from Tkinter import *

import matplotlib as mpl
mpl.rcParams['font.size'] = 14  
import matplotlib.pyplot as plt
   

def plot_sentiments(keyp_list, keyn_list):
    
        
    ''' pie charts '''
    T=0
    
    f, axarr = plt.subplots(1, 4)
    axarr[0].axis('off')
    axarr[1].axis('off')
    axarr[2].axis('off')
    axarr[3].axis('off')
    
    aspects = ['service', 'staff', 'clean', 'locat']
    
    for asp in aspects:
    
        t=0
        for j in range(0,len(keyp_list)):
        
            if asp in str(keyp_list[j][0]):
                
                t=1
                p_list=keyp_list[j][1]
                break
            
        if t == 0:
                p_list=-2
        
        t=0
        for j in range(0,len(keyn_list)):
        
            if asp in str(keyn_list[j][0]):
                
                t=1
                n_list = keyn_list[j][1]
                break
            
        if t == 0:
                n_list = -2
            
            
        
        if p_list==-2 and n_list != -2:
            
           asp_score=-1
           
           
        elif p_list!= -2 and n_list ==-2:
            
           asp_score=1
        
            
        elif p_list != -2 and n_list != -2:
           
           score = float(p_list)/n_list
           asp_score=score
        
        elif p_list ==-2 and n_list == -2:
            asp_score = 0
        
        
        
        if asp_score== 1 :
           sizes = [360]
           colors = ['green']
           plt.subplot(1,4,1)
           plt.pie(sizes, colors=colors, shadow = True, startangle=140 )  
           
        elif asp_score== -1  :
           sizes = [360]
           colors = ['red']
           plt.subplot(1,4,1)
           plt.pie(sizes, colors=colors, shadow = True, startangle=140 )  
              
        elif asp_score == 0:
            sizes = [360]
            colors = ['white']
            plt.subplot(1,4,1)
            plt.pie(sizes, colors=colors, shadow = True, startangle=140)
            
           
        else: 
            neg=360/float(1+asp_score)
            sizes = [ 360- neg, neg ]
            colors = ['green', 'red']
            labels = 'Positive', 'Negative'
            explode = (0.1, 0)
            plt.subplot(1,4,1)
            patches, texts =  plt.pie(sizes, explode=explode,  colors=colors, shadow = True, startangle=90)  
            if T == 0
                plt.legend(patches, labels, loc="best")
                T=1
        
        if asp == 'service'  :        
            plt.title('Service')
            
        elif asp == 'staff' :
            plt.title ('Staff')
            
        elif asp == 'clean' : 
            plt.title('Cleanliness')
            
        else :
            plt.title('Location')
    
        
    
def get_hotels_top_ten(hotel_names, hotel_ranks):
    
    window = Tk()
    window.geometry('500x500')
    
    window.title("HotelsNow, Top 10 Hotels")
    
    color= ['medium blue', 'blue2', 'blue',  'RoyalBlue3','RoyalBlue2','RoyalBlue1',   'DodgerBlue3','DodgerBlue2',   'SteelBlue3','SteelBlue2']
#        'SteelBlue1',  'SkyBlue3',  'SkyBlue2',  'SkyBlue1',  'LightSkyBlue2','LightSkyBlue1', 'SlateGray2', 'SlateGray1', 'LightSteelBlue2','LightSteelBlue1',  'LightBlue2', 
#        'LightBlue1']
    
    
    for ndx in range(0,10):
        row = Frame(window)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab=Label(row, width=30, text = hotel_names[ndx]+ str(hotel_rank[ndx]),  fg="white", background=color[ndx], font="ariel",anchor='w')#.grid(row=y, column=0, columnspan=3,sticky=W)
        lab.pack(side=LEFT)


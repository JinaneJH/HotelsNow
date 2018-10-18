#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 14:25:00 2018

@author: sdic_lab
"""

#  python tripadvisor_scraper.py "2018/10/01" "2018/11/12" "popularity" "boston" GENERATE the file 'tripadvisor_data.csv'

#  The function scrape_reviews(Nb_months,locality) read the url links of hotels from the file 'locality_tripadvisor_data.csv' and extract the reviews
#  of each hotel, those corresponding to the last Nb_months months

import urllib2
import sys
import re
from bs4 import BeautifulSoup
import requests

from datetime import date, datetime
import numpy as np
import pandas as pd
import time

from selenium import webdriver

import os




def diff_dates(date1, date2):
    return abs(date2-date1).days   # threshold 6 months; approx 180 days

    
def month_string_to_number(string):
    
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()
    
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')


def scrape_reviews(Nb_months,locality):
    
    
    now = datetime.now()   
    dtc= date(now.year,now.month,now.day)    
    Nb_days = Nb_months*30    
    df_hotels = pd.read_csv(locality+'_tripadvisor_data.csv')
    option = webdriver.ChromeOptions()
    path_chrome = "/Users/sdic_lab/Documents/project/myproject/chromedriver"
    browser = webdriver.Chrome(executable_path=path_chrome, chrome_options=option)  
    
    ListsOfreviews=[]
    ListsOfdates=[]
    ListsOfrates=[]
    for index, row in df_hotels.iterrows():
           
            print 'Extracting reviews for '+ row['hotel_name']
            list_date = []
            list_rate = []
            list_review = []
            
            
            url0 = row['url'] 
            
                    
            page = requests.get(url0)
    
            hotel_soup = BeautifulSoup(page.content, 'html.parser')
            
            ''' extract all dates'''
           
            date_review = hotel_soup.find_all(class_= "ratingDate")
           
            '''extract all rates '''
           
            rate_tags = []
            rates=[]
            for  container in hotel_soup.find_all('div', attrs={'class': "ui_column is-9"}):
                try:
                        rate_tags.append(str(container.find('span', {'class': re.compile(r'ui_bubble_rating bubble')})))
                except:
                        continue
            for rate in rate_tags:
                
                if rate != 'None': # because there are nontype empty rate in rate_tags
                
                    rates.append(re.search('<span class="ui_bubble_rating bubble_(.*)0"></span>', rate).group(1))
     
            ''' extract all review texts ''' 
            reviews = hotel_soup.find_all('div', attrs={'class':'reviewSelector'}) 
            text_review = []
            
           
            browser.quit()
            browser = webdriver.Chrome(executable_path=path_chrome, chrome_options=option)
            browser.get(url0)
            for review in reviews:  
                    
                 
                 review_id= review.get('id')
                 byid = browser.find_element_by_id(str(review_id))  
                 partial_text = byid.find_element_by_tag_name('p')
                 try:
                     partial_text.find_element_by_tag_name('span').click()
                     t=1
                 except: 
                     t=0
                 if t==0:
                     text_review.append(partial_text.text)
                 else:
                     time.sleep(2)              
                     full_review = browser.find_element_by_xpath('(//*[@id="'+ str(review_id) + '"]//p)[1]')
                     time.sleep(2)
                     text_review.append(full_review.text)
                     
                    
            '''select the most recent reviews '''
            for ndx, date0 in enumerate(date_review):
                
                d = str(date0.get_text())
                dt= d[9:-1]
                if 'today' in dt or 'yesterday' in dt or 'ago' in dt:
                    
                    list_date.append(dt)
                    list_review.append(text_review[ndx])
                    list_rate.append(rates[ndx])                   
                    
                    
                else:       
                    month = month_string_to_number(dt.split()[0])
                    day = dt.split()[1]
                    day = int(re.search('(.+?),', day).group(1))
                    year = int(dt.split()[2])
                    dt0= date(year,month,day)
                    if diff_dates(dt0, dtc) < Nb_days:
                        list_date.append(dt0)
                        list_review.append(text_review[ndx])
                        list_rate.append(rates[ndx])
                        
            ind= 5
            T=1
            seg = url0.split('Reviews')
            while T:
                   
                
                url = seg[0]+ 'Reviews'+ '-or' + str(ind) + seg[1]
                
               # try:
                
                page = requests.get(url)
                       
                hotel_soup = BeautifulSoup(page.content, 'html.parser')
               # except: 
               #     break
                
                ind=ind+5
                
                date_review = hotel_soup.find_all(class_= "ratingDate")
                reviews = hotel_soup.find_all('div', attrs={'class':'reviewSelector'}) 
               
                text_review = []               
                browser.quit()
                browser = webdriver.Chrome(executable_path=path_chrome, chrome_options=option)
                browser.get(url)
                for review in reviews:  
                    
                     review_id= review.get('id')
           
                     byid = browser.find_element_by_id(str(review_id))  
                             
                     partial_text = byid.find_element_by_tag_name('p')
                     
                     try:
                         partial_text.find_element_by_tag_name('span').click()
                         t=1
                     except: 
                         t=0
                     if t==0:
                         text_review.append(partial_text.text)
                     else:
                         time.sleep(2)              
                         full_review = browser.find_element_by_xpath('(//*[@id="'+ str(review_id) + '"]//p)[1]')
                         time.sleep(2)
                         text_review.append(full_review.text)
                         
                 
                     
                print(text_review)        
                        
                rate_tags = []
                rates=[]
                for  container in hotel_soup.find_all('div', attrs={'class': "ui_column is-9"}):
                        try:
                            rate_tags.append(str(container.find('span', {'class': re.compile(r'ui_bubble_rating bubble')})))
                        except:
                            continue
                for rate in rate_tags:
                    
                    if rate != 'None': # because there are nontype empty rate in rate_tags
                    
                        rates.append(re.search('<span class="ui_bubble_rating bubble_(.*)0"></span>', rate).group(1))       
                                                
                
                for ndx, date0 in enumerate(date_review):
                    
                    d = str(date0.get_text())
                    dt= d[9:-1]
                    if 'today' in dt or 'yesterday' in dt or 'ago' in dt:
                        
                        list_date.append(dt)
                        list_review.append(text_review[ndx])
                        list_rate.append(rates[ndx])
                        
                        
                    else:       
                        month = month_string_to_number(dt.split()[0])
                        day = dt.split()[1]
                        day = int(re.search('(.+?),', day).group(1))
                        year = int(dt.split()[2])
                        dt0= date(year,month,day)
                        if diff_dates(dt0, dtc) < Nb_days:
    
                            list_date.append(dt0)
                            list_review.append(text_review[ndx])
                            list_rate.append(rates[ndx])
                            
                        else: 
                            T= 0
              
                            break
                        
                        
            ListsOfdates.append(list_date)
            ListsOfreviews.append(list_review)
            ListsOfrates.append(list_rate)
     
    ListOfnames=[]
    for index, row in df_hotels.iterrows():
       
            ListOfnames.append(row['hotel_name'])
           
    reviews_hotels_df = pd.DataFrame({'Name': ListOfnames, 'Date' :ListsOfdates, 'Rate': ListsOfrates, 'Reviews': ListsOfreviews})        
            
    reviews_hotels_df.to_csv(locality+'_reviews_hotels.csv')

    return ListOfnames, ListsOfdates, ListsOfrates, ListsOfreviews 


    

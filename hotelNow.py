#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:19:19 2018

@author: sdic_lab
"""


import tripadvisor_scraper as scrapy

import reviews_parser as parser

from reviews_analysis import *

from result_plot import *


def main():
    
    locality = raw_input('Tell me what is your destination city ?')
    checkin_date = raw_input('And your check-in date')
    checkout_date = raw_input('What about your check-out date?')
    T=1
    while T:
        sort = raw_input('Do you want the most popular or the most economic hotels? choose p for most popular and c for most economic')
        if sort == p:
            option = 'popularity' 
            T=0
        elif sort == c:
            option ='priceLow'  
            T=0
        else: 
            input('Please choose p for most popular and c for lowest price!')
            continue
            
    """ generate a csv file with hotels urls and other info """    
    scrapy.main(locality, checkin_date, checkout_date, option) 


    ListsOfnames, ListsOfdates, ListsOfrates, ListsOfreviews  =  parser.scrape_reviews() # create reviews_hotels.csv

    names_sn, rates_sn,  dates_sn, rank_sn, reviews_sn, tripadv_sn = hotels_sort(ListsOfrates, ListsOfnames, ListsOfReviews, ListsOfdates)
    
   # for ndx in range(0,len(names_sn)):
   
    print "List of the top 10 hotels"   
    get_hotels_top_ten(hotel_names, hotel_ranks)
        
    keyp_list, keyn_list = hotel_sentiment(reviews_sn[ndx])
    print "Reviews' Sentiments for" + names_sn[0]+", the top hotel "
    plot_sentiments(keyp_list[0],keyn_list[0])





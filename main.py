# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 17:06:37 2020

@author: kucza
"""
import scrape_results_page as srp
import sqlalchemy
import preprocessing_functions as pf

number_of_pages_to_scrape = 100
logging_offset = True
query = 'SELECT MATCH_URL FROM C##TKUCZAK.IF_FINAL_DICTIONARY'

#create the db_connection
db_connection = sqlalchemy.create_engine('oracle+cx_oracle://C##tkuczak:TOMCIO@@@@localhost:1521')
                                         
#incremental scraping - get a list of match_urls which have already been scraped from the db
                       

for i in range(number_of_pages_to_scrape):
    #offset will be used to create the url
    offset = i*100
    
    #matches_page
    matches_page_url = 'https://www.hltv.org/results?offset=' + str(offset)
    try:
        error_code = srp.scrape_results_page(matches_page_url, db_connection, logging = True)
    except Exception:
        raise
    except BaseException:
        print('The maximum number of duplicates reached. The scraping will stop now.')
        break

    
    if logging_offset:
        print('Scraping offset ' + str(offset) + 'finished')
 

results_list = pf.query_to_list(db_connection, query)
    

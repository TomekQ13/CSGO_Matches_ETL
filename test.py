# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 20:50:35 2020

@author: kucza
"""

import scraper
import preprocessing_functions as pf

details_url = 'https://www.hltv.org/matches/2343939/btrg-vs-divine-vendetta-funspark-ulti-2020-asia-qualifier'

details_page_soup = pf.open_url(details_url)

g_grid_maps = details_page_soup.find("div", {"class":"col-6 col-7-small"})

#maps
flexbox_column = g_grid_maps.findAll("div", {"class": "mapholder"})

cs_map = flexbox_column[1]
len

cs_map.findAll("div", {"class": "results-team-score"})[1].text
cs_map.findAll("div", {"class": "results-team-score"})[0].text


for i in range(10):
    
    if i == 5:
        continue
    print(i)
    
url = 'https://www.hltv.org/matches/2314123/mask-off-vs-last-picks-dreamhack-open-montreal-2017-north-america-open-qualifier'
final_dict, results_pdf, teams_past_matches, h2h_table = scraper.scrape_match_details(url)

import db_connect as dc
con = dc.db_con()
con.truncate_interface()





import preprocessing_functions as pf
     
details_page_soup = pf.open_url(url)
lineups = details_page_soup.find("div", {"class": "lineups"})

tables = lineups.findAll("table", {"class": "table"})
len(tables[1].findAll("td", {"class": "player"}))

for i in range(4):
    print(i)
    
    
import sqlalchemy
import scsdm_etl.common
db_connection = sqlalchemy.create_engine('oracle+cx_oracle://C##tkuczak:TOMCIO@@@@localhost:1521')
                                
results = db_connection.execute(query_columns)

query_columns = "select column_name from sys.all_tab_columns where owner = 'C##TKUCZAK' and table_name = 'IF_FINAL_DICTIONARY' and column_name not like 'T_%'"
columns_list = scsdm_etl.common.query_to_list(db_connection, query_columns)
column_str = ', '.join(columns_list)
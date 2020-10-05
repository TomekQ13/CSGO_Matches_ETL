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
    
    
final_dict, results_pdf, teams_past_matches, h2h_table = scraper.scrape_match_details('https://www.hltv.org/matches/2339713/mc-vs-rock-candy-esea-mdl-season-33-australia')
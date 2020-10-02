import scraper
#import db_connect
import preprocessing_functions as pf
import pandas as pd

from sqlalchemy import types, create_engine


my_url = 'https://www.hltv.org/results'

page_soup =  pf.open_url(my_url)



#get the list of matches
container = page_soup.findAll("div", {"class":"result-con"})


#create the conection
conn = create_engine('oracle+cx_oracle://C##tkuczak:TOMCIO@@@@localhost:1521')

#iterate over the matches
#for match in enumerate(container):
    
    #get the match details url
details_url = 'https://www.hltv.org' + container[0].a['href']
    
    #scrape the match
final_dict, results_pdf, teams_past_matches, h2h_table = scraper.scrape_match_details(details_url)
    
final_dict_pd = pd.DataFrame(columns = final_dict.keys())
final_dict_pd = final_dict_pd.append(final_dict, ignore_index = True)
final_dict_pd.columns = ['match_url', 'left_team', 'right_team', 'left_team_nationality',
       'left_team_match_points', 'left_team_ranking', 'right_team_nationality',
       'right_team_match_points', 'right_team_ranking', 'tournament',
       'hour_of_match', 'day_of_match', 'month_of_match', 'year_of_match',
       'h2h_left_team_wins', 'h2h_right_team_wins', 'overtimes', 'match_type',
       'match_url', 'left_team_player_one', 'left_team_player_two',
       'left_team_player_three', 'left_team_player_four', 'left_team_player_five',
       'right_team_player_one', 'right_team_player_two', 'right_team_player_three',
       'right_team_player_four', 'right_team_player_five']
 
final_dict_pd.to_sql('IF_FINAL_DICTIONARY',
                     conn, if_exists = 'append', index = False, schema = 'C##TKUCZAK')
results_pdf.to_sql('IF_RESULTS_PDF', conn, if_exists = 'append', index = False, schema = 'C##TKUCZAK')
h2h_table.to_sql('IF_HEAD_TO_HEAD', conn, if_exists = 'append', index = False, schema = 'C##TKUCZAK')
teams_past_matches.to_sql('IF_TEAMS_PAST_MATCHES', conn, if_exists = 'append', index = False, schema = 'C##TKUCZAK')


#con = db_connect.start_con()
#cursor = con.cursor()
#results = cursor.execute("select * from test_table")
#
#for row in cursor:
#    print(row)
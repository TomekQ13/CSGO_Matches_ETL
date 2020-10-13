def scrape_results_page(my_url,
                        db_connection,
                        logging = True,
                        matches_list = [],
                        number_duplicates = 5,
                        logging_matches =  True):
    # scrapes one page of results - around 100 matches and inserts into the database

    import scraper
    #import db_connect
    import preprocessing_functions as pf
    import pandas as pd
    
    #my_url = 'https://www.hltv.org/results'
    
    page_soup =  pf.open_url(my_url)    
    
    #get the list of matches
    container = page_soup.findAll("div", {"class":"result-con"})    
    
    #initiate a variable counting dupicates for loading increments
    duplicates = 0
    
    #iterate over the matches
    for match in enumerate(container):
            
        #get the match details url
        details_url = 'https://www.hltv.org' + match[1].a['href']
        
        #loading only 
        #if match_url is already in the table display a message to the log and skip the load
        if (details_url in matches_list):
            print('Match ' + str(details_url) + ' has already been inserted into the table')
            duplicates = duplicates + 1
            print('Duplicates: ' + str(duplicates))
            continue
            
        if duplicates >= number_duplicates:
            raise BaseException('The maximum number of duplicates reached. The scraping will stop now.')
            
        
        #scrape the match
        try:
            final_dict, results_pdf, teams_past_matches, h2h_table = scraper.scrape_match_details(details_url)
        except:
            print('Scraping match identified by URL: ' + str(details_url) + ' failed')
            raise
            
        final_dict_pd = pd.DataFrame(columns = final_dict.keys())
        final_dict_pd = final_dict_pd.append(final_dict, ignore_index = True)
        
        #manual adjustment so the names of the column are the same as in the database
        final_dict_pd.columns = ['match_url', 'left_team', 'right_team', 'left_team_nationality',
               'left_team_match_points', 'left_team_ranking', 'right_team_nationality',
               'right_team_match_points', 'right_team_ranking', 'tournament',
               'hour_of_match', 'day_of_match', 'month_of_match', 'year_of_match',
               'h2h_left_team_wins', 'h2h_right_team_wins', 'overtimes', 'match_type',
               'match_url', 'left_team_player_one', 'left_team_player_two',
               'left_team_player_three', 'left_team_player_four', 'left_team_player_five',
               'right_team_player_one', 'right_team_player_two', 'right_team_player_three',
               'right_team_player_four', 'right_team_player_five']
        
        # append all the DataFrames to the databasetables
        final_dict_pd.to_sql('IF_FINAL_DICTIONARY',
                             db_connection, if_exists = 'append', index = False, schema = 'C##TKUCZAK')
        results_pdf.to_sql('IF_RESULTS_PDF', db_connection, if_exists = 'append', index = False, schema = 'C##TKUCZAK')
        h2h_table.to_sql('IF_HEAD_TO_HEAD', db_connection, if_exists = 'append', index = False, schema = 'C##TKUCZAK')
        teams_past_matches.to_sql('IF_TEAMS_PAST_MATCHES', db_connection, if_exists = 'append', index = False, schema = 'C##TKUCZAK')
        
        if logging_matches:
            print("Match " + str(match[0]) + " done. URL: " + str(details_url))
            
    if logging:
        print('Details page ' + str(my_url) + ' done')
        
    

#con = db_connect.start_con()
#cursor = con.cursor()
#results = cursor.execute("select * from test_table")
#
#for row in cursor:
#    print(row)
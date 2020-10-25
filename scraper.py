

def scrape_match_details(details_url):
    
    import pandas as pd    
    import preprocessing_functions as pf
        
    details_page_soup = pf.open_url(details_url)
    
    #getting match time
    timeAndEvent = details_page_soup.findAll("div", {"class":"timeAndEvent"})
    
    #get the time
    hour = timeAndEvent[0].div.text
    
    #get the date
    date = timeAndEvent[0].find("div", {"class":"date"}).text
    day, month, year = pf.date_parser(date)
      
    
    #get the torunament
    tournament = timeAndEvent[0].find("div", {"class":"event text-ellipsis"}).text
    
    #get the teamsBox - the box at the top of the screen
    teamsBox = details_page_soup.findAll("div", {"class":"standard-box teamsBox"})
    teams = teamsBox[0].findAll("div", {"class":"team"})
    
    #get information about the left team
    team_left_name =  teams[0].div.div.text
    team_left_nationality = teams[0].img["title"]
    
    #empty string counts as false, select the number of points for team left
    if teams[0].find("div", {"class":"lost"}):
        team_left_points = teams[0].find("div", {"class":"lost"}).text
    elif teams[0].find("div", {"class":"won"}):        
        team_left_points = teams[0].find("div", {"class":"won"}).text
    else:
        team_left_points = teams[0].find("div", {"class":"tie"}).text
        
    #get information about the right team
    team_right_name =  teams[1].div.div.text
    team_right_nationality = teams[1].img["title"]
    
    #empty string counts as false, select the number of points for team left
    if teams[1].find("div", {"class":"lost"}):
        team_right_points = teams[1].find("div", {"class":"lost"}).text
    elif teams[1].find("div", {"class":"won"}):        
        team_right_points = teams[1].find("div", {"class":"won"}).text
    else:
        team_right_points = teams[1].find("div", {"class":"tie"}).text
        
    #scrape maps and scores
    #first get into the Maps tab
    g_grid_maps = details_page_soup.find("div", {"class":"col-6 col-7-small"})
    
    #type of match - sometimes the information is missing and usually it is bo1
    try:
        match_type = g_grid_maps.find("div", {"class": "padding preformatted-text"}).text
    except:
        match_type = 'Probably best of one'
    
    #maps
    flexbox_column = g_grid_maps.findAll("div", {"class": "mapholder"})
    
    
    results_pdf = pd.DataFrame(columns = ["map_name", "team_left_score", "team_right_score", "map_number", "match_url"])
    map_number = 0
    for cs_map in enumerate(flexbox_column):
        results_dict = {}    
        map_number = map_number + 1
        #get the map name
        results_dict["map_name"] = cs_map[1].find("div", {"class": "mapname"}).text
        
        #get the team scores on the map,
        #try except if the match was planned to be more maps than was but for some reason was canceled
        
        try:
            results_dict["team_left_score"] = cs_map[1].findAll("div", {"class": "results-team-score"})[0].text
        except:
            results_dict["team_left_score"] = 'ERROR_TBA'
            
        try:
            results_dict["team_right_score"] = cs_map[1].findAll("div", {"class": "results-team-score"})[1].text
        except:
            results_dict["team_right_score"] = 'ERROR_TBA'            
            
        results_dict["map_number"] = map_number
        results_dict["match_url"] = details_url
        
        results_pdf = results_pdf.append(results_dict, ignore_index = True)
        
       
    #scrape lineups
    lineups = details_page_soup.find("div", {"class": "lineups"})
    
    lineups_dict = {}
    #get the two tables with lineups of the two teams and loop
    tables = lineups.findAll("table", {"class": "table"});  


       #loop by teams
    for cs_table in enumerate(tables):    
        players = cs_table[1].findAll("tr")[1].findAll("td", {"class": "player"})
        #here is also a possibility to get player details
       
        #loop by players
        for i in range(5):
            
            #assign to the correct team - left or right team
            if cs_table[0] == 0:                
                
                try:
                    player_name = players[i].text[2:-2]
                    if len(player_name) == 0:
                        player_name = 'ERROR_PLAYER_NO_NAME'
                    lineups_dict["team_left_player_"+str(i)] = player_name
                except IndexError:
                    lineups_dict["team_left_player_"+str(i)] = 'ERROR_PLAYER_NOT_FOUND'
                    print("team_left_player_"+str(i) + ' has not been found')
            else:
                try:
                    player_name = players[i].text[2:-2]
                    if len(player_name) == 0:
                        player_name = 'ERROR_PLAYER_NO_NAME'
                    lineups_dict["team_right_player_"+str(i)] = player_name
                except IndexError:
                    lineups_dict["team_right_player_"+str(i)] = 'ERROR_PLAYER_NOT_FOUND'
                    print("team_right_player_"+str(i) + ' has not been found')
                 
     #if there are 4 players add TBA as fifth player to avoid length mismatch
#        if len(players) == 4:
#            if cs_table[0] == 0:
#                lineups_dict['team_left_player_5'] = 'TBA'
#                print('Fifth player for team left not found')
#            else:
#                lineups_dict['team_right_player_5'] = 'TBA'
#                print('Fifth player for team rigt not found')
        
    #world rank    
    team_left_ranking = lineups.findAll("div", {"class": "teamRanking"})[0].text
    team_right_ranking = lineups.findAll("div", {"class": "teamRanking"})[1].text
    
    #past matches
    past_matches = details_page_soup.find("div", {"class": "past-matches"})
    tables_past_matches = past_matches.findAll("table", {"class": "table matches"})
    
    #new way to read past matches
    left_team_past_matches = pd.read_html(str(tables_past_matches))[0]
    
    #if there are no past matches
    if len(left_team_past_matches.columns) ==1:
        left_team_past_matches = pd.DataFrame(columns = ["type", "opponent", "result"])
    
    left_team_past_matches.columns = ["type", "opponent", "result"]
    left_team_past_matches["match_url"] = details_url
    left_team_past_matches["team"] = team_left_name
    
    right_team_past_matches = pd.read_html(str(tables_past_matches))[1]
    
    #if there are no past matches
    if len(right_team_past_matches.columns) ==1:
        right_team_past_matches = pd.DataFrame(columns = ["type", "opponent", "result"])
        
    right_team_past_matches.columns = ["type", "opponent", "result"]
    right_team_past_matches["match_url"] = details_url
    right_team_past_matches["team"] = team_right_name
    
    teams_past_matches =  left_team_past_matches.append(right_team_past_matches)
    #team_left_past_matches = tables_past_matches[0].findAll("tr", {"class": "table"})
    
   
    #head to head results
    head_to_head = details_page_soup.find("div", {"class": "head-to-head"})
    
    left_team_wins = head_to_head.findAll("div", {"class": "bold"})[0].text
    overtimes = head_to_head.findAll("div", {"class": "bold"})[1].text
    right_team_wins = head_to_head.findAll("div", {"class": "bold"})[2].text
    
    #the head to head results
    
    try:
        h2h_table = pd.read_html(str(details_page_soup.find("div", {"class": "standard-box head-to-head-listing"}).table))[0]
    except:
        h2h_table = pd.DataFrame(columns = ["match_date", "team_left", "delete", "team_right", "delete", "tournament", "map", "score"])
        print('Head to head not found for match ' + str(details_url))
    
    h2h_table.columns = ["match_date", "team_left", "delete", "team_right", "delete", "tournament", "map", "score"]
    
    h2h_table = h2h_table[["match_date", "team_left", "team_right", "tournament", "map", "score"]].copy()
    
    h2h_table["team_left"] = team_left_name
    h2h_table["team_right"] = team_right_name
    
    h2h_table["match_url"] = details_url
    
    #make the final dict
    
    final_dict = {}
    
    final_dict["match_details_url"] = details_url
    final_dict["left_team"] = team_left_name
    final_dict["right_team"] = team_right_name
    final_dict["left_team_nationality"] = team_left_nationality
    final_dict["left_team_match_points"] = team_left_points
    final_dict["left_team_ranking"] = team_left_ranking
    final_dict["right_team_nationality"] = team_right_nationality
    final_dict["right_team_match_points"] = team_right_points
    final_dict["right_team_ranking"] = team_right_ranking
    final_dict["tournament"] = tournament
    final_dict["hour_of_match"] = hour
    final_dict["day_of_match"] = day
    final_dict["month_of_match"] = month
    final_dict["year_of_match"] = year
    final_dict["h2h_left_team_wins"] = left_team_wins
    final_dict["h2h_right_team_wins"] = right_team_wins
    final_dict["overtimes"] = overtimes
    final_dict["match_type"] = match_type
    final_dict["match_url"] = details_url
    
    final_dict = pf.merge_dicts(final_dict, lineups_dict)
    

    return final_dict, results_pdf, teams_past_matches, h2h_table


#TO DO modify h2h_table so the date is parsed in IFa better format



    
        
    
        
        
    
    
    
    

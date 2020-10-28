

def main():
    import scrape_results_page as srp
    import sqlalchemy
    import preprocessing_functions as pf
    import urllib.error
    import time
    
    number_of_pages_to_scrape = 1000
    logging_offset = True
    starting_offset = 0
    query = 'SELECT MATCH_URL FROM C##TKUCZAK.IF_FINAL_DICTIONARY'
    
    
    #create the db_connection
    db_connection = sqlalchemy.create_engine('oracle+cx_oracle://C##tkuczak:TOMCIO@@@@localhost:1521')
                             
                                    
    #incremental scraping - get a list of match_urls which have already been scraped from the db
    results_list = pf.query_to_list(db_connection, query) 
    
    #Some URL's are broken 
    matches_to_skip = [
            'https://www.hltv.org/matches/2291761/mousesports-vs-madjick-esl-one-cologne-2014-south-west-pre-qualifier',
            'https://www.hltv.org/matches/2291488/wild-fire-vs-madjick-dreamhack-summer-2014-pre-qualifier-3']
    
    def loop(matches_to_skip = None):
        
        if matches_to_skip == None:
            matches_to_skip = []            
            
        for i in range(number_of_pages_to_scrape):
            #offset will be used to create the url
            offset = starting_offset + i*100
            
            #matches_page
            matches_page_url = 'https://www.hltv.org/results?offset=' + str(offset)
            if matches_page_url in matches_to_skip:
                print('Skipping match with URL: ' + matches_page_url)
                continue
            
            try:
                srp.scrape_results_page(matches_page_url,
                                        db_connection,
                                        logging = True,
                                        matches_list = results_list,
                                        number_duplicates = 9999999,
                                        matches_to_skip = matches_to_skip)
            except Exception:
                raise
        
            if logging_offset:
                print('Scraping offset ' + str(offset) + ' finished')
                
    try:
        loop(matches_to_skip = matches_to_skip)
    except urllib.error.HTTPError as e:
        print('Exception: ' + str(e) + ' caught. Waiting 60 seconds and restarting the scraping.')
        time.sleep(60)
        
        #select the already scraped results once again to avoid scraping duplicates
        results_list = pf.query_to_list(db_connection, query) 
        
        try:
            loop(matches_to_skip = matches_to_skip)
        except urllib.error.HTTPError as e:
            print('Exception: ' + str(e) + ' caught again.')

        
    print('Scraping finished')

if __name__ == '__main__':
    main()


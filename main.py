

def main():
    import scrape_results_page as srp
    import sqlalchemy
    import preprocessing_functions as pf
    
    number_of_pages_to_scrape = 1000
    logging_offset = True
    starting_offset = 45900
    query = 'SELECT MATCH_URL FROM C##TKUCZAK.IF_FINAL_DICTIONARY'
    
    
    #create the db_connection
    db_connection = sqlalchemy.create_engine('oracle+cx_oracle://C##tkuczak:TOMCIO@@@@localhost:1521')
                             
    results_list = pf.query_to_list(db_connection, query)                                 
    #incremental scraping - get a list of match_urls which have already been scraped from the db
                           
    def loop():
        for i in range(number_of_pages_to_scrape):
            #offset will be used to create the url
            offset = starting_offset + i*100
            
            #matches_page
            matches_page_url = 'https://www.hltv.org/results?offset=' + str(offset)
            try:
                srp.scrape_results_page(matches_page_url,
                                        db_connection,
                                        logging = True,
                                        matches_list = results_list,
                                        number_duplicates = 9999999)
            except BaseException as be:
#                print('The maximum number of duplicates reached. The scraping will stop now.' + str(be) )
#                break
                raise
            except Exception:
                raise

        
            if logging_offset:
                print('Scraping offset ' + str(offset) + ' finished')
                
    try:
        loop()
    except Exception as e:
        print('Exception: ' + str(e) + ' caught')
        #loop()
        
    print('Scraping finished')

if __name__ == '__main__':
    main()

    
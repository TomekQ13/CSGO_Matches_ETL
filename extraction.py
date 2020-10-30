def extraction(comments = '', echo = False):
    from scsdm_etl.extract_load import extract_load
    
    extraction = extract_load(echo = echo)    
    
    extraction.open_run_id(etl_code = 'EXTRACTION, TRANSFORMATION, LOAD', comments = comments)
    
    extraction.insert_exists(source_table = 'IF_FINAL_DICTIONARY', target_table = 'EX_FINAL_DICTIONARY')
    extraction.insert_exists(source_table = 'IF_HEAD_TO_HEAD', target_table = 'EX_HEAD_TO_HEAD')
    extraction.insert_exists(source_table = 'IF_RESULTS_PDF', target_table = 'EX_RESULTS_PDF')
    extraction.insert_exists(source_table = 'IF_TEAMS_PAST_MATCHES', target_table = 'EX_TEAMS_PAST_MATCHES')
    
    #extraction.close_run_id()
    print('Extraction finished')
    
    return extraction.run_id
    

if __name__ == '__main__':
    extraction()
    
    
    
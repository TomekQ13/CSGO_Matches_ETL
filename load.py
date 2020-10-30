def load(comments = '', echo = False, run_id = None):
    from scsdm_etl.extract_load import extract_load
    
       
    
    if not run_id:
        load = extract_load(echo = echo) 
        load.open_run_id(etl_code = 'LOAD', comments = comments)
    else:
        load = extract_load(echo = echo, run_id = run_id) 

    load.insert_exists(source_table = 'TR_HEAD_TO_HEAD', target_table = 'SCSDM_HEAD_TO_HEAD', exists_column = 'MATCH_RK')
    load.insert_exists(source_table = 'TR_LINEUP', target_table = 'SCSDM_LINEUP', exists_column = 'MATCH_RK')
    load.insert_exists(source_table = 'TR_MAP', target_table = 'SCSDM_MAP', exists_column = 'MATCH_RK')
    load.insert_exists(source_table = 'TR_MATCH', target_table = 'SCSDM_MATCH', exists_column = 'MATCH_RK')
    
    load.close_run_id()
    print('Load finished')
    

if __name__ == '__main__':
    load()
    
from scsdm_etl.extract_load import extract_load



class transform(extract_load):
    def load_rk(self, rk_table_schema = 'C##TKUCZAK', rk_table = 'TR_MAP_MATCH_RK'):
         import sqlalchemy as sql
#        from scsdm_etl.common import query_to_list
#        from sqlalchemy import text
        
        #check if run_id for the etl_code is open
         if self.etl_code == '-1' and self.run_id == -1:
            raise Exception('Open run_id first.')
        
        #get the current max match_rk
#        max_rk_query = text('select coalesce(max(match_rk),0) from ' + rk_table_schema + '.' + rk_table)
#        max_rk = query_to_list(self.engine, max_rk_query)[0]
#        print('Current max MATCH_RK is: ' + str(max_rk))
        
         print ('Processing with RUN_ID: ' + str(self.run_id))
        #insert match_urls which do not have an rk yet into into map_match_rk
         query_rk = sql.text('insert into ' + rk_table_schema + '.' + rk_table +
                                  ' (INSERT_RUN_ID, MATCH_URL) select distinct ' +
                                  str(self.run_id) + ' as "INSERT_RUN_ID" , MATCH_URL  from ' +
                                  'C##TKUCZAK.EX_FINAL_DICTIONARY' + 
                                  ' t1' + ' where not exists(select MATCH_URL' + 
                                  ' from ' + rk_table_schema + '.' + rk_table + ' t2 where t1.MATCH_URL ' +
                                  '= t2.MATCH_URL)')
                                  
         res = self.engine.execute(query_rk)
         print('Inserted: ' + str(res.rowcount) + ' rows')
     
    
    
    def head_to_head(self,
                     source_schema = 'C##TKUCZAK',
                     source_table = 'EX_HEAD_TO_HEAD',
                     target_schema = 'C##TKUCZAK',
                     target_table = 'TR_HEAD_TO_HEAD',
                     run_id = None,
                     initial_load = False):
        import sqlalchemy as sql
        #if run_id not assigned as an argument then assign the current run_id
        if not run_id:
            run_id = self.run_id
        
        transform_query = sql.text('insert into ' + target_schema + '.' + target_table + 
                            '(T_INSERT_RUN_ID, MATCH_RK, LT_NAME, RT_NAME, MAP_NAME, LT_SCORE, RT_SCORE, TOURNAMENT) ' +
                            "select " + str(run_id) + " as T_INSERT_RUN_ID, t2.MATCH_RK, t1.TEAM_LEFT, t1.TEAM_RIGHT, substr(t1.MAP, instr(t1.MAP, ' ')) as MAP_NAME, substr(t1.SCORE,1,2) as LT_SCORE, substr(t1.SCORE, instr(t1.SCORE, '-') + 1, 3) as RT_SCORE, t1.TOURNAMENT " +
                            'from ' + source_schema + '.' + source_table + ' t1 left join C##TKUCZAK.TR_MAP_MATCH_RK t2 ' + 
                            'on t1.MATCH_URL = t2.MATCH_URL')
        
        #execute the load query with where clause if not initial load and without if initial load    
        if initial_load:
            res = self.engine.execute(transform_query)
        
            print('Inserted: ' + str(res.rowcount) + ' rows with run_id: ' + str(run_id))
        else:
            res = self.engine.execute(transform_query + ' where t1.T_INSERT_RUN_ID = ' + str(run_id))
         
            print('Inserted: ' + str(res.rowcount) + ' rows with run_id: ' + str(run_id))
        
        
               
        



test=extract_load()
test.open_run_id('EXTRACT', 'Testing extraction from FINAL_DICTIONARY')
test.insert_exists(source_table = 'IF_FINAL_DICTIONARY', target_table = 'EX_FINAL_DICTIONARY')
test.insert_exists(source_table = 'IF_HEAD_TO_HEAD', target_table = 'EX_HEAD_TO_HEAD')
test.insert_exists(source_table = 'IF_TEAMS_PAST_MATCHES', target_table = 'EX_TEAMS_PAST_MATCHES')
test.insert_exists(source_table = 'IF_RESULTS_PDF', target_table = 'EX_RESULTS_PDF')

test = transform()
test.open_run_id(etl_code = 'TRANSFORM', comments = 'Testing head to head transform')
test.head_to_head(initial_load = True)
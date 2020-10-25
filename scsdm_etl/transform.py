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
     
        
    def transform_insert(self,
                         source_table,
                         target_table,
                         transform_query,
                         source_schema = 'C##TKUCZAK',
                         target_schema = 'C##TKUCZAK',
                         run_id = None,
                         initial_load = False):
        
        import sqlalchemy as sql
        from datetime import datetime
        
                #if run_id not assigned as an argument then assign the current run_id
        if not run_id:
            run_id = self.run_id
        
        #insert the run_id into the query
        transform_query = transform_query.replace('__run_id__', str(run_id))
        
        transform_query = sql.text(transform_query)
               
        #save time before load start
        time_before_transform = datetime.now()
        
        #execute the load query with where clause if not initial load and without if initial load    
        if initial_load:
            res = self.engine.execute(transform_query)        
        else:
            res = self.engine.execute(transform_query + ' where t1.T_INSERT_RUN_ID = ' + str(run_id))
            
        #save time after transform and calculat time difference
        time_after_transform = datetime.now()
        time_diff = time_after_transform - time_before_transform
         
        #print messages to the log
        print('Table ' + target_table + ' loaded')
        print('Inserted: ' + str(res.rowcount) + ' rows with run_id: ' + str(run_id) + '. The insert took: ' + str(time_diff))


test=extract_load()
test.open_run_id('EXTRACT', 'Testing extraction from FINAL_DICTIONARY')
test.insert_exists(source_table = 'IF_FINAL_DICTIONARY', target_table = 'EX_FINAL_DICTIONARY')
test.insert_exists(source_table = 'IF_HEAD_TO_HEAD', target_table = 'EX_HEAD_TO_HEAD')
test.insert_exists(source_table = 'IF_TEAMS_PAST_MATCHES', target_table = 'EX_TEAMS_PAST_MATCHES')
test.insert_exists(source_table = 'IF_RESULTS_PDF', target_table = 'EX_RESULTS_PDF')

#queries exclude duplicates - to be assessed if this can cause possible data loss and perhaps do this earlier

head_to_head_query = '''insert into C##TKUCZAK.TR_HEAD_TO_HEAD 
(T_INSERT_RUN_ID, MATCH_RK, LT_NAME, RT_NAME, MAP_NAME, LT_SCORE, RT_SCORE, TOURNAMENT) 
select distinct __run_id__ as T_INSERT_RUN_ID, t2.MATCH_RK, t1.TEAM_LEFT, t1.TEAM_RIGHT, substr(t1.MAP, instr(t1.MAP, ' ')) as MAP_NAME, substr(t1.SCORE,1,2) as LT_SCORE, substr(t1.SCORE, instr(t1.SCORE, '-') + 1, 3) as RT_SCORE, t1.TOURNAMENT
from C##TKUCZAK.EX_HEAD_TO_HEAD t1 left join C##TKUCZAK.TR_MAP_MATCH_RK t2 
on t1.MATCH_URL = t2.MATCH_URL'''
                            
lineup_query = '''insert into C##TKUCZAK.TR_LINEUP 
(T_INSERT_RUN_ID, MATCH_RK, LT_PLAYER_ONE, LT_PLAYER_TWO, LT_PLAYER_THREE, LT_PLAYER_FOUR, LT_PLAYER_FIVE, RT_PLAYER_ONE, RT_PLAYER_TWO, RT_PLAYER_THREE, RT_PLAYER_FOUR, RT_PLAYER_FIVE) 
select distinct __run_id__ as T_INSERT_RUN_ID, t2.MATCH_RK, LEFT_TEAM_PLAYER_ONE, LEFT_TEAM_PLAYER_TWO, LEFT_TEAM_PLAYER_THREE, LEFT_TEAM_PLAYER_FOUR, LEFT_TEAM_PLAYER_FIVE, 
RIGHT_TEAM_PLAYER_ONE, RIGHT_TEAM_PLAYER_TWO, RIGHT_TEAM_PLAYER_THREE, RIGHT_TEAM_PLAYER_FOUR, RIGHT_TEAM_PLAYER_FIVE
from C##TKUCZAK.EX_FINAL_DICTIONARY t1 left join C##TKUCZAK.TR_MAP_MATCH_RK t2
on t1.MATCH_URL = t2.MATCH_URL'''

map_query = '''insert into C##TKUCZAK.TR_MAP 
(T_INSERT_RUN_ID, MATCH_RK, MAP_NAME, MAP_NUMBER, LT_SCORE, RT_SCORE) 
select distinct __run_id__ as "T_INSERT_RUN_ID", t2.MATCH_RK,  t1.MAP_NAME, t1.MAP_NUMBER as "MAP_NUMBER", regexp_replace(t1.TEAM_LEFT_SCORE, '-|ERRRO_TBA|TBA|ERROR_TBA') as "LT_SCORE", regexp_replace(t1.TEAM_RIGHT_SCORE, '-|ERRRO_TBA|TBA|ERROR_TBA') as "RT_SCORE"
from C##TKUCZAK.EX_RESULTS_PDF t1 left join C##TKUCZAK.TR_MAP_MATCH_RK t2 
on t1.MATCH_URL = t2.MATCH_URL'''

match_query = '''insert into C##TKUCZAK.TR_MATCH 
(MATCH_RK, LT_NAME, RT_NAME, LT_NATIONALITY, RT_NATIONALITY, LT_RANKING, RT_RANKING, TOURNAMENT, MATCH_HOUR, MATCH_DAY, MATCH_MONTH, YEAR_OF_THE_MATCH, HEAD_TO_HEAD_OVERTIMES, T_INSERT_RUN_ID) 
select distinct t2.MATCH_RK, t1.LEFT_TEAM, t1.RIGHT_TEAM, t1.LEFT_TEAM_NATIONALITY, t1.RIGHT_TEAM_NATIONALITY, t1.LEFT_TEAM_RANKING, t1.RIGHT_TEAM_RANKING, t1.TOURNAMENT, t1.HOUR_OF_MATCH, t1.DAY_OF_MATCH, t1.MONTH_OF_MATCH, t1.YEAR_OF_MATCH, t1.OVERTIMES, __run_id__ as "T_INSERT_RUN_ID" 
from C##TKUCZAK.EX_FINAL_DICTIONARY t1
left join C##TKUCZAK.TR_MAP_MATCH_RK t2 
on t1.MATCH_URL = t2.MATCH_URL'''

transform_inst = transform()
transform_inst.open_run_id(etl_code = 'TRANSFORM', comments = 'Testing head to head transform')
transform_inst.transform_insert(source_table = 'EX_HEAD_TO_HEAD', target_table = 'TR_HEAD_TO_HEAD', initial_load = True, transform_query = head_to_head_query)
transform_inst.transform_insert(source_table = 'EX_FINAL_DICTIONARY', target_table = 'TR_LINEUP ', initial_load = True, transform_query = lineup_query)
transform_inst.transform_insert(source_table = 'EX_RESULTS_PDF', target_table = 'TR_MAP', initial_load = True, transform_query = map_query)
transform_inst.transform_insert(source_table = 'EX_FINAL_DICTIONARY ', target_table = 'TR_MATCH ', initial_load = True, transform_query = match_query)
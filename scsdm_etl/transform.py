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
        
        transform_query = transform_query
               
        #save time before load start
        time_before_transform = datetime.now()
        
        #execute the load query with where clause if not initial load and without if initial load    
        if initial_load:
            res = self.engine.execute(sql.text(transform_query))   
        else:
            res = self.engine.execute(sql.text(transform_query + ' where t1.T_INSERT_RUN_ID = ' + str(run_id)))
            
        #save time after transform and calculat time difference
        time_after_transform = datetime.now()
        time_diff = time_after_transform - time_before_transform
         
        #print messages to the log
        print('Table ' + target_table + ' loaded')
        print('Inserted: ' + str(res.rowcount) + ' rows with run_id: ' + str(run_id) + '. The insert took: ' + str(time_diff))




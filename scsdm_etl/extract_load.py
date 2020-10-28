#this module consists of a class with methods to run the extracts
class extract_load:
    def __init__(self,
                 load_status_table = "C##TKUCZAK.LOAD_STATUS",
                 connect_string = 'oracle+cx_oracle://C##TKUCZAK:TOMCIO@@@@localhost:1521',
                 echo = True):
        #estabilish the database connection
        import sqlalchemy as sql
             
        self.connect_string = connect_string
        self.engine = sql.create_engine(connect_string, echo = echo)
        self.etl_code = '-1'
        self.run_id = -1
        self.load_status_table = load_status_table
        
        #create a dictionary with parameters to use as bind variables
        self.parameters = {}
        self.parameters['etl_code'] = self.etl_code
        self.parameters['run_id'] = self.run_id

        
    def open_run_id(self, etl_code, comments):
        
        import scsdm_etl.common
        import sqlalchemy as sql
        
        #add comments as a parameter in the parameters dictionary
        self.parameters['run_id_comments'] = comments
        self.etl_code = etl_code
        self.parameters['etl_code'] = etl_code
        
        #set the queries as variables
        query_update = sql.text("update " + self.load_status_table + " set close_dttm = current_timestamp where ETL_CODE = :etl_code and close_dttm is null")
        query_open_run_id = sql.text("insert into " + self.load_status_table + " (ETL_CODE, COMMENTS) values (:etl_code, :run_id_comments)")
        
        
        
        #if run_id is open close the open one and open a new one with the etl_code                
        try:
#            if self.run_id != -1 and self.etl_code != '-1':
                #close the open one                
            self.engine.execute(query_update, self.parameters)
                
                #open a new one                                
            self.engine.execute(query_open_run_id, self.parameters)
                
#            else:
#                #only open a new one
#                self.engine.execute(query_open_run_id, self.parameters)
                
        #if not possible then raise Exception and show message
        except Exception as e:
            print('RUN_ID not opened')
            raise e
            
        #select the opened run_id and assign to a parameter        
        try:
            #select opened run_id
            select_run_id = sql.text('select RUN_ID from ' + self.load_status_table + ' where ETL_CODE = :etl_code and CLOSE_DTTM is null')
            run_id = scsdm_etl.common.query_to_list(self.engine, select_run_id, self.parameters)
            
            #assign parameters
            self.run_id = run_id[0]
            self.etl_code = etl_code
            print('RUN_ID: ' + str(self.run_id))
            
        except Exception as e:
            print('RUN_ID could not be selected')
            raise e
        
        
        
        
    def insert_exists(self, source_table, target_table, exists_column = 'MATCH_URL', source_schema = 'C##TKUCZAK', target_schema = 'C##TKUCZAK'):
        #the function performans to a load to the extraction layer with exists on MATCH_URL - the table has to have match_url column
        
        import scsdm_etl.common
        
        #check if RUN_ID is opne
        if self.etl_code == '-1' and self.run_id == -1:
           raise Exception('Open run_id first.')
        
        #select a list of columns to a variable
        query_columns = "select column_name from sys.all_tab_columns where owner = '" + target_schema + "' and table_name = '" + target_table + "' and column_name not like 'T_INSERT%'"
        
        columns_list = scsdm_etl.common.query_to_list(self.engine, query_columns, param_dict = {})
        column_str = ', '.join(columns_list)
        
        #select number of rows before 
        
        
        res = self.engine.execute('insert into ' + target_schema + '.' + target_table +
                            '(T_INSERT_RUN_ID, ' + column_str + ') select ' + str(self.run_id) + ' as "T_INSERT_RUN_ID", ' + 
                            column_str + ' from ' + source_schema + '.' + source_table + 
                            ' t1' + ' where not exists(select t2.' + exists_column + 
                            ' from ' + target_schema + '.' + target_table + ' t2 where t1.' +
                            exists_column + ' = t2.' + exists_column + ')')
        print('Inserted: ' + str(res.rowcount) + ' rows')


    def insert(self, source_table, target_table, exists_column = 'MATCH_URL', source_schema = 'C##TKUCZAK', target_schema = 'C##TKUCZAK', initial_load = False):
               
        import sqlalchemy as sql
        from scsdm_etl.common import columns_to_string
        
        #check if run_id is open
        if self.etl_code == '-1' and self.run_id == -1:
            raise Exception('Open run_id first.')
            
        #PART 1. delete rows with the current run_id from the target table       
        if initial_load:
            delete_query = sql.text('delete from ' + target_schema + '.' + target_table)
        else:
            delete_query = sql.text('delete from ' + target_schema + '.' + target_table + ' where T_INSERT_RUN_ID = ' + str(self.run_id))
            
        delete = self.engine.execute(delete_query)
        
        print(str(delete.rowcount) + ' rows deleted.')
        
        #PART 2 - INSERT
        #select all columns
        columns = columns_to_string(engine = self.engine, schema = target_schema, table = target_table, include_technical = False)
        
        #create the insert query        
        #add where clause if delta load
        if not initial_load:
            insert_query = 'insert into ' + target_schema + '.' + target_table + ' (' + columns + ', T_INSERT_RUN_ID) ' + 'select ' + columns + ', ' +  str(self.run_id) + ' as "T_INSERT_RUN_ID" from ' + source_schema + '.' + source_table + ' where T_INSERT_RUN_ID = ' + str(self.run_id)
        else:
            insert_query = 'insert into ' + target_schema + '.' + target_table + ' (' + columns + ', T_INSERT_RUN_ID) ' + 'select ' + columns + ', ' +  str(self.run_id) + ' as "T_INSERT_RUN_ID" from ' + source_schema + '.' + source_table
        insert = self.engine.execute(sql.text(insert_query))
        
        print('Inserted ' + str(insert.rowcount) + ' rows.')
        
    def close_run_id(self, etl_code = None):
        
        if not etl_code == None:
            self.parameters['etl_code'] = etl_code
        
        import sqlalchemy as sql
        
        query_update = sql.text("update " + self.load_status_table + " set close_dttm = current_timestamp where ETL_CODE = :etl_code and close_dttm is null")
        
        update_execute = self.engine.execute(query_update, self.parameters)
        
        if update_execute.rowcount == 0:
            raise Exception('No open run id. Open run id first.')
        

               
#this module consists of a class with methods to run the extracts
class ext_and_load:
    def __init__(self,
                 load_status_table = "C##TKUCZAK.LOAD_STATUS",
                 connect_string = 'oracle+cx_oracle://C##TKUCZAK:TOMCIO@@@@localhost:1521'):
        #estabilish the database connection
        import sqlalchemy as sql
             
        self.connect_string = connect_string
        self.engine = sql.create_engine(connect_string, echo = True)
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
        
        #set the queries as variables
        query_update = sql.text("update " + self.load_status_table + " set close_dttm = current_timestamp where ETL_CODE = :etl_code and close_dttm is null")
        query_open_run_id = sql.text("insert into " + self.load_status_table + " (ETL_CODE, COMMENTS) values (:etl_code, :run_id_comments)")
        
        
        
        #if run_id is open close the open one and open a new one with the etl_code                
        try:
            if self.run_id != -1 and self.etl_code != '-1':
                #close the open one                
                self.engine.execute(query_update, self.parameters)
                
                #open a new one                                
                self.engine.execute(query_open_run_id, self.parameters)
                
            else:
                #only open a new one
                self.engine.execute(query_open_run_id, self.parameters)
                
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
            self.run_id = run_id
            self.etl_code = etl_code
            print('RUN_ID: ' + str(self.run_id))
            
        except Exception as e:
            print('RUN_ID could not be selected')
            raise e
        
        
        
        
    def insert_exists(self,source_table, target_table, exists_column = 'MATCH_URL', source_schema = 'C##TKUCZAK', target_schema = 'C##TKUCZAK'):
        #the function performans to a load to the extraction layer with exists on MATCH_URL - the table has to have match_url column
        #select a list of columns to a variable
        import common
        query_columns = "select column_name from sys.all_tab_columns where owner = " + str(target_schema) + " and table_name = " + str(target_table) + " and column_name not like 'T_%'"
        columns_list = common.query_to_list(self.engine, query_columns)
        column_str = ', '.join(columns_list)
        
        #select number of rows before 
        
        
        res = self.engine.execute('insert into ' + target_schema + '.' + target_table +
                            '(' + column_str + ') select ' +
                            column_str + ' from ' + source_schema + '.' + source_table + 
                            ' t1' + ' where not exists(select t2.' + exists_column + 
                            ' from ' + target_schema + '.' + target_table + ' t2 where t1.' +
                            exists_column + ' = t2.' + exists_column + ')')
        print('Inserted: ' + str(res.rowcount) + ' rows')
        





test=ext_and_load()

test.open_run_id('test', 'test_comment')
test.open_run_id('test', 'test_comment')



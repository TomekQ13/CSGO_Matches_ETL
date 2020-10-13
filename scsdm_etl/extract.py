#this module consists of a class with methods to run the extracts
class extract:
    def __init__(self,
                 etl_code = 'EXTRACT',
                 connect_string = 'oracle+cx_oracle://C##tkuczak:TOMCIO@@@@localhost:1521'):
        #estabilish the database connection
        import sqlalchemy as sql
             
        self.connect_string = connect_string
        self.engine = sql.create_engine(connect_string)
        self.etl_code = etl_code
        
    def insert_exists(self, exists_column = 'MATCH_URL', source_schema = 'C##TKUCZAK', target_schema = 'C##TKUCZAK', source_table = 'IF_FINAL_DICTIONARY', target_table = 'EX_FINAL_DICTIONARY'):
        #the function performans to a load to the extraction layer with exists on MATCH_URL - the table has to have match_url column
        #select a list of columns to a variable
        import common
        engine = self.engine
        query_columns = "select column_name from sys.all_tab_columns where owner = 'C##TKUCZAK' and table_name = 'IF_FINAL_DICTIONARY' and column_name not like 'T_%'"
        columns_list = common.query_to_list(engine, query_columns)
        column_str = ', '.join(columns_list)
        
        
        self.engine.execute('insert into ' + target_schema + '.' + target_table +
                            '(' + column_str + ') select ' +
                            column_str + ' from ' + source_schema + '.' + source_table + 
                            ' t1' + ' where not exists(select t2.' + exists_column + 
                            ' from ' + target_schema + '.' + target_table + ' t2 where t1.' +
                            exists_column + ' = t2.' + exists_column + ')')
        
a = extract()

a.insert_exists()




        query_columns = "select column_name from sys.all_tab_columns where owner = 'C##TKUCZAK' and table_name = 'IF_FINAL_DICTIONARY' and column_name not like 'T_%';"
        columns_list = common.query_to_list(self.engine, query_columns)
result = a.engine.execute(query_columns)

def query_to_list(engine, query, param_dict = {}):
    #transfers query results to a list
    try:
        results = engine.execute(query, param_dict)
    except:
        raise #BaseException("Query could not be executed or was executed with errors")
        
    results_list = [row[0] for row in results]
        
    return results_list

def select_to_pandas(sql, engine):
    import pandas as pd
    return pd.read_sql(sql, engine)

                
def truncate_interface(engine,
                       query1 = 'truncate table C##TKUCZAK.IF_HEAD_TO_HEAD',
                       query2 = 'truncate table C##TKUCZAK.IF_RESULTS_PDF',
                       query3 = 'truncate table C##TKUCZAK.IF_TEAMS_PAST_MATCHES',
                       query4 = 'delete from C##TKUCZAK.IF_FINAL_DICTIONARY'):
                          engine.execute(query1)
                          engine.execute(query2)
                          engine.execute(query3)
                          engine.execute(query4)
                          
                          
                          
def columns_to_string(schema, table, engine, include_technical = False, param_dict = {}):
    from scsdm_etl.common import query_to_list
    
    query_columns = "select column_name from sys.all_tab_columns where owner = '" + schema + "' and table_name = '" + table + "'"
    
    if not include_technical:
        query_columns = query_columns + " and column_name not like 'T_INSERT%'"
        
    columns_list = query_to_list(engine, query_columns, param_dict)
    column_str = ', '.join(columns_list)
    
    return column_str
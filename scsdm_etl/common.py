def query_to_list(engine, query):
    #transfers query results to a list
    try:
        results = engine.execute(query)
    except:
        raise #BaseException("Query could not be executed or was executed with errors")
        
    results_list = [row[0] for row in results]
        
    return results_list
    
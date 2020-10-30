def do_etl(echo = False, inital_load = False):
    from load import load
    from extraction import extraction
    from transformation import transformation
    
    
    run_id = extraction(echo = echo)
    
    transformation(echo = echo, inital_load = inital_load, run_id = run_id)
    
    load(echo = echo, run_id = run_id)

if __name__ == '__main__':
    do_etl(inital_load = False, echo = False)
    
    

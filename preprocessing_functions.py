def date_parser(input_date):
    #parses date from day of month year  (e.g. 26th of September 2020) to separate variables for day, month and year 
    
    #check if input format is string
    if not isinstance(input_date, str):
        raise BaseException("Input date has to be a string")
        return    
    
    #check if the format is correct - the input string has to contain exactly 3 spaces
    first_space = input_date.find(" ")
    second_space = input_date[first_space + 1:].find(" ") + first_space + 1
    third_space = input_date[second_space + 1:].find(" ") + second_space + 1
    
    if first_space == -1 or input_date[first_space + 1:].find(" ") == -1 or input_date[second_space + 1:].find(" ") == -1:
        raise BaseException("Input date does not contain 3 spaces. Please make sure that the input format is correct.")
        return
    
    #check if at least first character is numeric
    if not input_date[0].isnumeric():
        raise BaseException("First character has to be numeric. Make sure that the input format is correct")
        return
    
    #day
    if input_date[1].isnumeric():
        day = input_date[0:2]
    else:
        day = input_date[0]
        
    #month
    month = input_date[second_space + 1:third_space]
    
    #year
    year = input_date[third_space + 1:]
    
    return day, month, year
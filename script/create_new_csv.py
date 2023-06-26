def create_new_csv(path = './data/new_accumulated_capital.csv',
                           path_raw ='./data/data_raw.csv',
                           year = 2023,
                           all_equal = True,
                           realistic = False):
    """Function to create a new csv using the raw data.
    Optional Arguments:
    path (str): The path to save the new CSV file (including the filename as name.csv).    path_raw (str): Where is the raw data base.
    path_raw (str): The path to the raw database.
    year (int): The year to analyze. Must be at least 2020.
    (Year will be included in filename if isn't 2023)
    progressive (bool): Flag to set up cuts in the saver 
    based on income.
    all_householders (bool): Flag to treat all individuals 
    as heads of households or not.   
    """
    
    import pandas as pd
    import numpy as np
    
    path = str(path)
    path_raw = str(path_raw)
    
    if not isinstance(year, int):
        raise TypeError("Only integers are allowed")

    if year < 2020:
        raise ValueError("Only integers greater than or equal to 2020 are allowed")
    
    if year != 2023:
        from os import getcwd
        path = path[:-4]+'_'+str(year)+'.csv'

    def saver_match(df,inflation = 0.044,max_return=1e+4,k=0,
                    progressive = realistic,
                    all_householders=all_equal):
        """Function to calculate the saver match using a database.
        Argument:
        df (pandas DataFrame): The database.

        Optional Arguments:
        k (int): Number of years for calculating inflation.
        progressive (bool): Flag to set up cuts in the saver 
        based on income.
        all_householders (bool): Flag to treat all individuals 
        as heads of households or not.
        """

        row = []
        _ = df['income'].tolist()
        inflation_rate = ((1+inflation)**3)

        def complications2(lower,upper,j):
                lower_ = lower*inflation_rate
                upper_ = upper*inflation_rate
                if progressive:
                    mean_category = (upper_ + lower_)/2
                    if _[j] < lower_ :
                        return max_return*0.5 
                    elif (_[j] >= lower_) or (_[j]< mean_category):
                        return max_return*0.2 
                    elif (_[j] >= mean_category) or (_[j] < upper_):
                        return max_return*0.1
                    else:
                        return 0
                else:
                        return max_return*0.5 

        for row1 in range(len(df)):
            if (_[row1]*inflation_rate) < (max_return * inflation_rate):
                row.append(_[row1]*0.5)

            elif all_equal:
                lower = 41e+3
                upper = 71e+3 
                row.append(complications2(lower,upper,row1))

            else:
                _2 = df['family_kind'].tolist() 
                if _2[row1] == 1:
                    lower = 41e+3
                    upper = 71e+3 
                    row.append(complications2(lower,upper,row1))

                else:
                    _3 = df['marital_status'].tolist() 
                    if _3[row1] == 5:
                        lower = 20500
                        upper = 35500 
                        row.append(complications2(lower,upper,row1))
                    else:
                        lower = 20500
                        upper = 35500 
                        row.append(complications2(lower,upper,row1))
        return(row)



    df_raw = pd.read_csv(path_raw)
     

    df = df_raw.copy()
    year = 2023
    n = year - 2020
    test = (65 - (df['initial_age'] + n))
    age_new = test.copy()
    for i in range(len(age_new)) :
        if age_new[i] > n : age_new[i] = 3
    df_new = df[test>1].copy()

    acumulated = df_new['accumulated_capital']
    income = df_new['income']
    contribution = df_new['annual_contribution']
    new_accumulated_capital = acumulated + (contribution*income) + saver_match(df = df_new)

    rate = 0.044
    new_income = income * (1+rate)

    if year > 2021:
        for i in range(n-1):
            new_accumulated_capital = (new_accumulated_capital + (contribution*new_income) + 
                                       saver_match(df = df_new,k=(i+1)) )
            new_income = new_income * (1+rate)
    if year == 2021:
        new_accumulated_capital = (new_accumulated_capital + (contribution*new_income) + 
                                       saver_match(df = df_new,k=(i+1)) )
    
    df_new['new_accumulated_capital'] = new_accumulated_capital
    

    df_new.to_csv(path_or_buf=path)
    return print("The new database was created in: \n {0}"
                 .format(path))


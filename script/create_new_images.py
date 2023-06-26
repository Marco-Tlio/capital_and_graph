def create_new_images(path = './graph/',
                           path_data ='./data/data_raw.csv',
                           year = 2023,
                           size = [15,8],
                           size_cm = False):
    """Function to create a two new graphs using the data that was constructed.

    Optional Arguments:
    path (str): The path to the folder where the two images will be saved (including the filename as name.csv).
    path_data (str): The location of the database.
    year (int): The year to analyze. Must be at least 2020. If not specified, it defaults to 2023.
    names (list of str): Names of the graphs (requires a list with two strings).
    titles (list of str): Names to be displayed on the graphs (requires a list with two strings).
    size (list of int): The size of the figures in inches (requires a list with two integers).
    size_cm (bool): Flag to set up the sizes using centimeters.
    """

    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    from os import getcwd

    if size_cm:
         size = 0.4*size
    size_using = tuple(size)
    
    path = str(path)
    path_data = str(path_data)

    if year < 2020:
        raise ValueError("Only integers greater than or equal to 2020 are allowed")

    if year != 2023:
        names = ["Weighted_Average"+'_'+str(year)+'.png',
             "Percentage_Points"+'_'+str(year)+'.png']    
    if year== 2023:
        names = ["Weighted_Average"+'.png',
             "Percentage_Points"+'.png']  

    df_new2 = df_new.copy()
    n = year - 2020
    df['initial_age'] + n
    def categorise(row):  
        if row['new_accumulated_capital'] < 0 :
            return 0
        return 1

    df_new2 = df_new.copy()
    df_new2['readiness_rating'] = df_new2.apply(lambda row: categorise(row), axis=1)
    labels = ['[35,39]', '[40,44]', '[45,49]', '[50,54]',  '[55,59]', '[60,64]']
    df_new2['age_cohort'] = pd.cut(x = df['initial_age'] + n, bins = 6, labels = labels, include_lowest = True)
    all_pop = sum(df_new2['weight'])

    category_race = ['White','Black','Hispanic','Other']
    df_new2['race'] = df_new2['race'].astype('category')
    df_new2['race'] = df_new2['race'].cat.rename_categories(category_race)

    #First plot

    df_new3 = df_new2[new_accumulated_capital<0]
    df_value = df_new3.groupby(['age_cohort', 'race'])['weight'].sum().reset_index()
    df_value2 = df_new3.groupby(['age_cohort', 'race'])['new_accumulated_capital'].sum().reset_index()

    df_value_plot = df_value.copy()
    df_value_plot['weight'] = (df_value['weight']*df_value2['new_accumulated_capital'])/all_pop

    df_value_plot.columns = ['Age Cohort','Race','Weighted Average Savings']
    sns.set()

    fig, ax = plt.subplots()

    fig.set_size_inches(size)
    plot = sns.barplot(ax = ax, data = df_value_plot, x = 'Age Cohort', y = 'Weighted Average Savings', hue = 'Race')
    plot.set_title('Weighted_Average Retirement Savings Shortfall by Race and Age Group' +'('+ str(year)+')')
    plt.legend(loc='center right')
    plt.savefig(path+names[0])
    #plt.show()
    #plt.close()
    
    #Second plot
    df_new4 = df_new2.copy()
    df_value = df_new4.groupby(['age_cohort', 'race','readiness_rating'])['weight'].sum().reset_index()
    df_value['weight'] = (df_value['weight']/all_pop) * 100
    df_value_plot = df_value[df_value['readiness_rating']==1]
    df_value_plot.columns = ['Age Cohort','Race','readiness_rating','Retirement Readiness Rating']

    sns.set()
    fig, ax = plt.subplots()
    fig.set_size_inches(size)
    plot = sns.barplot(ax = ax, data = df_value_plot, x = 'Age Cohort', y = 'Retirement Readiness Rating', hue = 'Race')
    plot.set_title('Percentage Points of Retirement Readiness Rating')
    plot.set_ylabel('Retirement Readiness Rating (%)')
    plt.savefig(path+names[1])
    plt.close()
    
    return print("The new images were created in: \n {0}"
                 .format(path))

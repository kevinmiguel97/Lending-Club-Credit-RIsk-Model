# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import regex as re

# Settings 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_info_rows', 30)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Date processing function
def process_date(df, column, today):
    """      
    Function that converts date in the format 'mmm-yy' to datetime and 
    creates a column with the months since that date and a estabised today date. 
    
    Parameters:
    -----------
    df: dataframe
        Dataframe to convert
    
    column: str
        Column name 
    
    today: datetime
        Date to use as Today
    """
    # Create new date column name
    date_col_name = str(column+'_date')

    # Create months since column name
    months_since_col_name = str('months_since_'+ column)

    df[date_col_name] = pd.to_datetime(df[column], format='%b-%y')

    # Transform data
    df[months_since_col_name] = df[date_col_name].apply(lambda x: (today.year - x.year)*12 + (today.month - x.month))

    return df

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def create_woe_discrete(column_name, X, y):
    # Get variable of interest
    df1 = pd.DataFrame(X[column_name])
    # Add target variable
    df1['target'] = y

    # Group data
    df1 = df1.groupby(column_name).agg({'target': ['count', 'sum']})

    # Rename columns
    df1.columns = ['observations', 'good_count']

    # Total pct
    df1['pct_total'] = df1['observations'] / df1['observations'].sum()

    # Get pct of good
    df1['good_prop'] = df1['good_count'] / df1['good_count'].sum()

    # Calculate bad loan values
    df1['bad_count'] = df1['observations'] - df1['good_count']

    df1['bad_prop'] = df1['bad_count'] / df1['bad_count'].sum()

    # Rearange columns
    df1 = df1[['observations', 'pct_total', 'good_count', 'bad_count', 'good_prop', 'bad_prop']]

    # Calculate WoE
    df1['weight_of_evidence'] = np.log(df1['good_prop'] / df1['bad_prop'])  

    df1['good-bad'] = df1['good_prop'] - df1['bad_prop']

    # Calculate information value
    df1['info_value'] = np.sum(df1['weight_of_evidence'] * df1['good-bad'])
    info_value = np.sum(df1['weight_of_evidence'] * df1['good-bad'])

    # Sort table
    df1 = df1.sort_values(by='weight_of_evidence')

    # Reset index
    df1 = df1.reset_index()

    return {'table': df1, 'info_value': info_value}

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def plot_weight_of_evidence(df, width=12, height=8): 
    column = df.columns[0]
    # Set the figure size
    fig, ax = plt.subplots(figsize=(width, height))

    # Plot the scatter plot with adjusted width
    df.plot.scatter(x=column, y='weight_of_evidence', c='DarkBlue', ax=ax)
    # Line connecting the points
    plt.plot(df[column], df['weight_of_evidence'], color='blue')
    plt.title('Weight of Evidence {}'.format(column))
    # Display the plot
    plt.show()
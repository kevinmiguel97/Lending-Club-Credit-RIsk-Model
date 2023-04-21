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
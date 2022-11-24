import pandas as pd

def convert_df(df:pd.DataFrame):
    return df.to_csv().encode('utf-8')
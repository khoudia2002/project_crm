import pandas as pd
import streamlit as st

#import des fichiers
@st.cache_data
def file_load_csv(data_path): 
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError:
        print("File not found")
        None
    except ModuleNotFoundError:
        print("Module not found")
        None

#Nettoyage de account 
def clean_acc_data(account_df): 
    clean_acc_df = account_df.fillna(value='None')
    return clean_acc_df

#nettoyage de sales_pipeline
def clean_sp_data(sales_pipeline_df):
    clean_sp_df = sales_pipeline_df.fillna(value=0)
   
    return clean_sp_df

#Remplacer les dates vides par NaT

def clean_sp_time(sales_pipeline_df):
     clean_sp_time = sales_pipeline_df.fillna(value=pd.NaT)
     #clean_sp_time = sales_pipeline_df['close_date'].fillna(value=pd.NaT)
     return clean_sp_time



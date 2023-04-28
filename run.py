# %%
import pandas as pd
from dateutil.parser import parse
import numpy as np
import os
from common import *

import sys

country_name = sys.argv[1]
model = sys.argv[2]
print(country_name, model)


# %%
op_df = pd.read_csv('data/OperatorDataSPOT_USD.csv', encoding='latin1')
op_df['Country_name'].unique()

# %%
def month_to_quarter (month):
    if month in [1,2,3]:
        return 'Q1'
    elif month in [4,5,6]:
        return 'Q2'
    elif month in [7,8,9]:
        return 'Q3'
    else: return 'Q4'
    
metric_id = [351, 352, 353]
attr_id = [0, 1691, 1692, 1690, 1687, 88, 1688, 1689, 1685, 1757, 1758, 836, 1684, 800, 1686]
if model == 'online':
    org_name_dict = org_id_to_name(country=country_name, company='')

    for i in org_name_dict:
        print(fetch_excel_data(org_name_dict[i], country_name, i))
        
    integrate_data(country=country_name)

    col_dict = dict(zip(['Operator_Id', 'Operator_name', 'metric_name', 'attribute_name', 'attribute_Id'], 
    ['Organisation_id', 'Organisation_Name', 'Metric_name', 'Attribute_name', 'attribute_id']))

    op_df = pd.read_excel(f'{country_name.capitalize()} Main.xlsx').rename(columns=col_dict)
    value_vars = ['Q1 2022', 'Q2 2022', 'Q3 2022',
        'Q4 2022', 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024',
        'Q2 2024', 'Q3 2024', 'Q4 2024']
        


    main_df = pd.melt(op_df, id_vars=['Organisation_id', 'Organisation_Name', 'metric_id', 'Metric_name','attribute_id', 'Attribute_name'], value_vars=value_vars, var_name='date', value_name='value_main').rename(columns={'Organisation_id': 'organisation_id'})
    q_dict = {'Q1': '01-01-', 'Q2': '01-04-', 'Q3': '01-07-', 'Q4': '01-10-'}
    main_df['date'] = main_df['date'].apply(lambda x:  parse(q_dict[x.split()[0]] + str(x.split()[1])))
else:
    op_df = pd.read_csv('data/OperatorDataSPOT_USD.csv', encoding='latin1')


    op_df = op_df.loc[(op_df['Country_name'] == country_name.capitalize()) 
    & (op_df['Metric_id'].isin(metric_id)) 
    & (op_df['Attribute_id'].isin(attr_id))].reset_index(drop=True)


    value_vars = [i for i in op_df.iloc[:, 9:].columns]


    main_df = pd.melt(op_df, id_vars=['Organisation_id', 'Organisation_Name', 'Metric_id', 'Metric_name','Attribute_id', 'Attribute_name'], value_vars=value_vars, var_name='date', value_name='value_main').rename(columns={'Organisation_id': 'organisation_id', 'Metric_id': "metric_id", 'Attribute_id': "attribute_id"})

    main_df['date'] = main_df['date'].map(parse)
    main_df.head()
# 


jp_df = pd.read_csv(f'{country_name.capitalize()} Operator.csv').iloc[:, :6]
jp_df.loc[(jp_df['metric_id'].isin(metric_id)) & (jp_df['attribute_id'].isin(attr_id))].reset_index(drop=True)
# , encoding='latin1'

jp_df['date'] = jp_df['date'].map(parse)
# jp_df.date = jp_df.date.map(parse)
jp_df.head()



check_df = pd.merge(jp_df, main_df, on=['organisation_id', 'metric_id', 'attribute_id', 'date'])
check_df['diff_wrt_main'] = check_df['value_main']-check_df['value']

check_df.loc[((check_df['diff_wrt_main']>3) | (check_df['diff_wrt_main']<-3) | (check_df["value"].isnull()) | (check_df["value_main"].isnull())) & (check_df['date'].dt.year.isin([2022, 2023, 2024])), ['Organisation_Name', 'Metric_name', 'Attribute_name', 'date', 'value', 'value_main', 'diff_wrt_main']]

# .sort_values(by = ['diff_wrt_main'])
# .to_csv('hungary_checklist.csv')

error_df = check_df.loc[((check_df['diff_wrt_main']>3) | (check_df['diff_wrt_main']<-3) | (check_df["value"].isnull()) | (check_df["value_main"].isnull())) & (check_df['date'].dt.year.isin([2022, 2023, 2024])), ['Organisation_Name', 'Metric_name', 'Attribute_name', 'date', 'value', 'value_main', 'diff_wrt_main']]

error_df['year'] = error_df['date'].dt.year.astype(str)

error_df['quarter'] = error_df['date'].dt.day.map(month_to_quarter) +'-'+ error_df['year']

error_df['summary'] = error_df.groupby(['Organisation_Name', 'Metric_name', 'Attribute_name'])['quarter'].transform(lambda x : ', '.join(x))
error_df.drop_duplicates(subset=['Organisation_Name', 'Metric_name', 'Attribute_name', 'summary']).reset_index(drop=True).loc[: , ['Organisation_Name', 'Metric_name', 'Attribute_name', 'summary']]
# error_df.quarter = 'Q'+error_df.quarter.astype(str)


error_df.groupby(['Organisation_Name', 'Metric_name', 'Attribute_name', 'summary'])['summary'].count().to_excel(f'summary_{country_name}.xlsx')
error_df.groupby(['Organisation_Name', 'Metric_name', 'Attribute_name', 'summary'])['summary'].count()

check_df.loc[check_df.value_main==0]

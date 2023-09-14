import pandas as pd
import numpy as np
import streamlit as st
from collections import Counter

st.title('Interactive Text Input Example')

cust_id = st.text_input('Enter Customer ID:')
datee = st.text_input('Enter Date:')

df = pd.read_csv(r'Online_Retail.csv')

df['detailed_description'] = np.nan
for i in range(df['Description'].size):
    if str(df['Description'][i]) != 'nan':
        df['detailed_description'][i] = " ".join(df['Description'][i].split(' ')[-2:])

df['date'] = df['InvoiceDate'].apply(lambda x: x.split(" ")[0])
df['InvoiceNo'] = pd.to_numeric(df['InvoiceNo'], errors='coerce')
df.corr()
df2 = df.drop(df[df['Quantity'] < 0].index)
df2.dropna(inplace=True)

items = df2['detailed_description'].unique()
ids = df2[df2['CustomerID'].notnull()]['CustomerID'].unique()
dates = df2['InvoiceDate'].apply(lambda x: x.split(' ')[0]).unique()


def case1(id, date):
    df6 = df2[df2['date'] == date]
    occurence_count = Counter(df6[df6['CustomerID'] == float(id)]['detailed_description'])
    return occurence_count.most_common(1)[0][0]
def case2(id, date):
    occurence_count = Counter(df2[df2['date'] == date]['detailed_description'])
    return occurence_count.most_common(1)[0][0]
def case3(id, date):
    occurence_count = Counter(df2[df2['CustomerID'] == id]['detailed_description'])
    return occurence_count.most_common(1)[0][0]
def case4(id, date):
    occurence_count = Counter(df2['detailed_description'])
    return occurence_count.most_common(1)[0][0]


if cust_id in ids and datee in dates:
    ans = case1(cust_id, datee)
elif cust_id not in ids and datee in dates:
    ans = case2(cust_id, datee)
elif cust_id in ids and datee not in dates:
    ans = case3(cust_id, datee)
else:
    ans = case4(cust_id, datee)
    
st.write(f'You entered: {ans}')

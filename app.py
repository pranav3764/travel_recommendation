import streamlit as st
import pickle
import pandas as pd
from unidecode import unidecode


model = pickle.load(open('model.pkl', 'rb'))
df2 = pd.read_csv("worldcities.csv")
df3 = df2[df2['population'].notna()]
df4 = df3[df3['country'] == 'India']
df5 = df4[df4['population'] > 50000]
df6 = df5[['city', 'lat', 'lng']]
temp_city = list(df6['city'])
l2 = df6.iloc[:, -1:-3:-1]
clusters = model.fit_predict(l2)
clusters = list(clusters)
df6['clusters'] = clusters

for i in range(len(temp_city)):
    temp_city[i] = unidecode(temp_city[i])
df6['city'] = temp_city
print(df6)
st.title("Travel Recommendetion")

input_city = st.text_input('Enter City').capitalize()
output = df6.loc[df6['city'] == input_city, 'clusters']
if st.button('Suggest'):
    cities = df6.loc[df6['clusters'].astype(int) == int(output), 'city']
    for c in range(6):
        if cities.iloc[c] == input_city:
            continue
        else:
            st.write(cities.iloc[c])


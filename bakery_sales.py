import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# load data
@st.cache_data
def load_data():
    df = pd.read_csv("Bakery sales.csv")
    # data cleaning
    df.drop(columns='Unnamed: 0', inplace=True)
    df['date'] = pd.to_datetime(df.date)
    df['ticket_number'] = df.ticket_number.astype('object')
    df['unit_price']=df.unit_price.str.replace(',','.').str.replace(' €','')
    df['unit_price'] = df.unit_price.astype('float')
    # calculate sales
    sales = df.Quantity * df.unit_price
    # add a new column to the dataframe
    df['sales'] = sales
    # return cleaned dataframe
    return df
    
df = load_data()
# app structure
st.title("Bakery Sales App")
st.sidebar.title("Filters")

# display the dataset
st.subheader("Data Preview")
st.dataframe(df.head())

# create a filter for articles and ticket numbers
articles = df['article'].unique()
ticketNos10 = df['ticket_number'].value_counts().head(10).reset_index()["ticket_number"]


# create a multiselect for articles
selected_articles = st.sidebar.multiselect("Products",articles,[articles[0],articles[20]])
top10_ticketNos = st.sidebar.selectbox("Top 10 Tickets", ticketNos10[:10])

# filter
filtered_articles = df[df["article"].isin(selected_articles)]

# display filtered table
st.subheader("Filtered table")
if not selected_articles:
    st.error("select an article")
else:
    st.dataframe(filtered_articles.sample(3))
                       
# calculations
total_sales = np.round(df['sales'].sum())
total_qty = np.round(df['Quantity'].sum())
no_articles = len(articles)
no_filtered_articles = filtered_articles['article'].nunique()
total_filtered_sales = np.round(filtered_articles['sales'].sum(),2)
total_filtered_qty = np.round(filtered_articles['Quantity'].sum(),2)

# display in columns
col1, col2, col3 = st.columns(3)
# sales
if not selected_articles:
    col1.metric("Total Sales", f'{total_sales:,}')
else:
    col1.metric("Total Sales", f'{total_filtered_sales:,}')

# quantity
if not selected_articles:
    col2.metric("Quantity", f'{total_qty:,}')
else:
    col2.metric("Quantity", f'{total_qty:,}')

# show number of articles based on the filter
if not selected_articles:
    col3.metric("No. of Products", no_articles)
else:
    col3.metric("No. of Products", no_filtered_articles)


# charts
st.header("Plotting")
# data
article_grp = df.groupby('article')['sales'].sum()
article_grp = article_grp.sort_values(ascending=False)[:-3]
table = article_grp.reset_index()

# selection fron the filter
filtered_table = table[table['article'].isin(selected_articles)]

# bar plot
st.subheader("Bar chart")
fig1, ax1 = plt.subplots(figsize=(10,6))
ax1.bar(filtered_table['article'],filtered_table['sales'])
st.pyplot(fig1)

# pie chart
# percentages
st.subheader("pie chart")
fig2, ax2 = plt.subplots(figsize=(7,5))
ax2.pie(filtered_table['sales'],
        labels=selected_articles,
        autopct="%1.1f%%")
st.pyplot(fig2)

st.subheader("Trend Analysis")
daily_sales = df.groupby('date')['sales'].sum()

fig3, ax3 = plt.subplots(figsize=(12,6))
ax3.plot(daily_sales.index, daily_sales.values)
st.pyplot(fig3)




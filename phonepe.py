import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import mysql.connector
import requests
import json
from PIL import Image


# dataframe creation
#sql connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="radha",
    database="Youtube_data",
    port="3306",
    auth_plugin='mysql_native_password'
    )
cursor = mydb.cursor()

# aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
table1 = cursor.fetchall()
cursor.close()
mydb.commit()

Aggre_insurance = pd.DataFrame(table1, columns = ("States", "Years", "Quarter", "Transaction_type", 
                                                  "Transaction_count", "Transaction_amount"))

# aggre_transaction_df
cursor = mydb.cursor()
cursor.execute("SELECT * FROM aggregated_transaction")
table2 = cursor.fetchall()
cursor.close()
mydb.commit()


Aggre_transaction = pd.DataFrame(table2, columns = ("States", "Years", "Quarter", "Transaction_type", 
                                                  "Transaction_count", "Transaction_amount"))

# aggre_user_df
cursor = mydb.cursor()
cursor.execute("SELECT * FROM aggregated_user")
table3 = cursor.fetchall()
cursor.close()
mydb.commit()


Aggre_user = pd.DataFrame(table3, columns = ("States", "Years", "Quarter", "Brands", 
                                                  "Transaction_count", "Percentage"))

# map_insurance_df
cursor = mydb.cursor()
cursor.execute("SELECT * FROM map_insurance")
table4 = cursor.fetchall()
cursor.close()
mydb.commit()


map_insurance = pd.DataFrame(table4, columns = ("States", "Years", "Quarter", "Districts", 
                                                  "Transaction_count", "Transaction_amount"))

# map_transaction_df
cursor = mydb.cursor()
cursor.execute("SELECT * FROM map_transaction")
table5 = cursor.fetchall()
cursor.close()
mydb.commit()


map_transaction = pd.DataFrame(table5, columns = ("States", "Years", "Quarter", "District", 
                                                  "Transaction_count", "Transaction_amount"))

# map_user_df
cursor = mydb.cursor()
cursor.execute("SELECT * FROM map_user")
table6 = cursor.fetchall()
cursor.close()
mydb.commit()


map_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "District", 
                                                  "RegisteredUsers", "AppOpens"))

# top_insurance_df
cursor = mydb.cursor()
cursor.execute("SELECT * FROM top_insurance")
table7 = cursor.fetchall()
cursor.close()
mydb.commit()


top_insurance = pd.DataFrame(table7, columns = ("States", "Years", "Quarter", "Pincodes", 
                                                  "Transaction_count", "Transaction_amount"))

# top_transaction_df
cursor = mydb.cursor()
cursor.execute("SELECT * FROM top_transaction")
table8 = cursor.fetchall()
cursor.close()
mydb.commit()


top_transaction = pd.DataFrame(table8, columns = ("States", "Years", "Quarter", "Pincodes", 
                                                  "Transaction_count", "Transaction_amount"))

# top_user_df
cursor = mydb.cursor()
cursor.execute("SELECT * FROM top_user")
table9 = cursor.fetchall()
cursor.close()
mydb.commit()


top_user = pd.DataFrame(table9, columns = ("States", "Years", "Quarter", "Pincodes", 
                                                  "RegisteredUsers"))



def Transaction_amount_count_Y(df, year):
    tacy = df[df["Years"]==year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[['Transaction_count', 'Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(tacyg, x='States', y='Transaction_amount', title=f"{year} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x='States', y='Transaction_count', title=f"{year} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.algae_r, height=650, width=600)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:


        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)

        data1 = json.loads(response.content)
        states_name = []
        for future in data1["features"]:
            states_name.append(future["properties"]['ST_NM'])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale="Rainbow", 
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_data="States", title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600, width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale="Rainbow", 
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_data="States", title=f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height=600, width=600)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):
    tacy = df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[['Transaction_count', 'Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(tacyg, x='States', y='Transaction_amount', title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x='States', y='Transaction_count', title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.algae_r, height=650, width=600)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)

        data1 = json.loads(response.content)
        states_name = []
        for future in data1["features"]:
            states_name.append(future["properties"]['ST_NM'])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale="Rainbow", 
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_data="States", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600, width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale="Rainbow", 
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_data="States", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height=600, width=600)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    return tacy

def Aggre_Tran_Transaction_type(df, state):

    tacy = df[df["States"]==state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("Transaction_type")[['Transaction_count', 'Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_pie_1 = px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT ", hole=0.5)

        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width=600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)

        st.plotly_chart(fig_pie_2)   

#Aggregated user analysis 1
def Aggre_user_plot_1(df, year):
    aguy = df[df['Years']==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")['Transaction_count'].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.amp_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy


#Aggregaed user analysis 2
def Agree_user_plot_2(df, quarter):
    aguyq = df[df['Quarter']==quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyqg, x= "Brands", y= "Transaction_count", title= f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                        width= 1000, color_discrete_sequence= px.colors.sequential.amp_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#Aggregaed user analysis 3
def Agree_user_plot_3(df, state):
    auyqs = df[df["States"]==state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1 = px.line(auyqs, x="Brands", y="Transaction_count", hover_data="Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width=800, markers=True)
    st.plotly_chart(fig_line_1)
    return auyqs

#map insurance district
def Map_insur_District(df, state):
    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    # Determine the correct column name for district
    district_col = 'Districts' if 'Districts' in tacy.columns else 'District'

    tacyg = tacy.groupby(district_col)[['Transaction_count', 'Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x="Transaction_amount", y=district_col, orientation='h', height=600,
                           title=f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Magenta_r)

        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(tacyg, x="Transaction_count", y=district_col, orientation='h', height=600,
                           title=f"{state.upper()} DISTRICTS AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Mint_r)

        st.plotly_chart(fig_bar_2)
    return tacy

#map user plot1
def map_user_plot_1(df, year):
    muy = df[df['Years']==year]
    muy.reset_index(drop=True, inplace=True)

    muyg = muy.groupby("States")[['RegisteredUsers','AppOpens']].sum()
    muyg.reset_index(inplace=True)

    fig_line_1 = px.line(muyg, x="States", y=["RegisteredUsers", "AppOpens"], 
                            title= f"{year} REGISTERED USER AND APPOPENS", width=800, height=800, markers=True, color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig_line_1)

    return muy

#map user plot2
def map_user_plot_2(df, quarter):
    muyq = df[df['Quarter']==quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg = muyq.groupby("States")[['RegisteredUsers','AppOpens']].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1 = px.line(muyqg, x="States", y=["RegisteredUsers", "AppOpens"], 
                            title= f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USER AND APPOPENS", width=800, height=800, markers=True,
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    return muyq

# map user plot 3
def map_user_plot_3(df, state):    
    muyqs = df[df['States']==state]
    muyqs.reset_index(drop=True, inplace=True)

    col1, col2 =st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x="RegisteredUsers", y="District", orientation="h",
                                    title="REGISTERED USER", height=800, color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_1)
    with  col2:
        fig_map_user_bar_2 = px.bar(muyqs, x="AppOpens", y="District", orientation="h",
                                    title="APPOPENS", height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_2)

# Top insurance plot 1
def Top_insurance_plot_1(df,state):
    tiy = df[df['States']==state]
    tiy.reset_index(drop=True, inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_top_insur_bar_1 = px.bar(tiy, x="Quarter", y="Transaction_amount", hover_data= "Pincodes",
                                        title="TRANSACTION AMOUNT", height=650, width=600, color_discrete_sequence=px.colors.sequential.deep_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2 = px.bar(tiy, x="Quarter", y="Transaction_count", hover_data= "Pincodes",
                                        title="TRANSACTION COUNT", height=650, width=600, color_discrete_sequence=px.colors.sequential.Teal_r)
        st.plotly_chart(fig_top_insur_bar_2)


# Function to plot top user data
def top_user_plot_1(df, year):
    tuy = df[df['Years'] == year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarter"])['RegisteredUsers'].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1 = px.bar(tuyg, x="States", y="RegisteredUsers", title=f"{year} REGISTERED USERS", color="Quarter",
                            width=1000, height=800, color_discrete_sequence=px.colors.sequential.gray_r, hover_name="States")
    st.plotly_chart(fig_top_plot_1)
    return tuy

def top_user_plot_2(df, state):
    tuys = df[df['States'] == state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2 = px.bar(tuys, x="Quarter", y="RegisteredUsers", title="REGISTERED USERS, PINCODES, QUARTER",
                            width=1000, height=800, color="RegisteredUsers", hover_data="Pincodes", color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)

# Function to fetch and plot top transaction amount
#sql connection
def top_chart_transaction_amount(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radha",
        database="Youtube_data",
        port="3306",
        auth_plugin='mysql_native_password'
        )
    cursor = mydb.cursor()

    #plot_1
    query1= f""" SELECT States, AVG(Transaction_amount) as transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY transaction_amount DESC
                limit 10 """
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()


    df_1 = pd.DataFrame(table_1, columns=("states","transaction_amount"))

    col1, col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x='states', y='transaction_amount', title="TOP 10 TRANSACTION AMOUNT",hover_name="states",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f""" SELECT States, AVG(Transaction_amount) as transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY transaction_amount 
                limit 10 """
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states","transaction_amount"))

    with col2:
        fig_amount_2 = px.bar(df_2, x='states', y='transaction_amount', title="LAST 10 TRANSACTION AMOUNT",hover_name="states",
                    color_discrete_sequence=px.colors.sequential.BuGn_r , height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f""" SELECT States, avg(Transaction_amount) as transaction_amount
                FROM {table_name}
                group by states
                order by transaction_amount 
                """
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states","transaction_amount"))


    fig_amount_3 = px.bar(df_3, y='states', x='transaction_amount', title="AVERAGE OF TRANSACTION AMOUNT",hover_name="states", orientation="h",
                color_discrete_sequence=px.colors.sequential.Aggrnyl , height=800, width=1000)
    st.plotly_chart(fig_amount_3)

# Function to fetch and plot top transaction count
#sql connection
def top_chart_transaction_count(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radha",
        database="Youtube_data",
        port="3306",
        auth_plugin='mysql_native_password'
        )
    cursor = mydb.cursor()

    #plot_1
    query1= f""" SELECT States, AVG(Transaction_count) as Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count DESC
                limit 10 """
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    col1, col2=st.columns(2)
    
    df_1 = pd.DataFrame(table_1, columns=("states","Transaction_count"))

    with col1:
        fig_amount = px.bar(df_1, x='states', y='Transaction_count', title="TOP 10 TRANSACTION COUNT",hover_name="states",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f""" SELECT States, AVG(Transaction_count) as Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count 
                limit 10 """
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    
    df_2 = pd.DataFrame(table_2, columns=("states","Transaction_count"))

    with col2:
        fig_amount_2 = px.bar(df_2, x='states', y='Transaction_count', title="LAST 10 TRANSACTION COUNT",hover_name="states",
                    color_discrete_sequence=px.colors.sequential.BuGn_r , height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f""" SELECT States, avg(Transaction_count) as Transaction_count
                FROM {table_name}
                group by states
                order by Transaction_count 
                """
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states","Transaction_count"))


    fig_amount_3 = px.bar(df_3, y='states', x='Transaction_count', title="AVERAGE OF TRANSACTION COUNT",hover_name="states", orientation="h",
                color_discrete_sequence=px.colors.sequential.Aggrnyl , height=800, width=1000)
    st.plotly_chart(fig_amount_3)

# Function to fetch and plot top registered users
#sql connection
def top_chart_registered_user(table_name,state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radha",
        database="Youtube_data",
        port="3306",
        auth_plugin='mysql_native_password'
        )
    cursor = mydb.cursor()

    #plot_1
    query1= f'''select districts, sum(registeredusers) as registereduser
                from {table_name}
                where states ='{state}'
                group by districts
                order by registereduser desc
                limit 10 '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("districts","registereduser"))

    col1, col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x='districts', y='registereduser', title=" TOP 10 REGISTERED USER",hover_name="districts",
                    color_discrete_sequence=px.colors.sequential.amp_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select districts, sum(registeredusers) as registereduser
                from {table_name}
                where states ='{state}'
                group by districts
                order by registereduser 
                limit 10 '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts","registereduser"))

    with col2:
        fig_amount_2 = px.bar(df_2, x='districts', y='registereduser', title="LAST 10 REGISTERED USER",hover_name="districts",
                    color_discrete_sequence=px.colors.sequential.algae_r , height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select districts, avg(registeredusers) as registereduser
                from {table_name}
                where states ='{state}'
                group by districts
                order by registereduser'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts","registereduser"))


    fig_amount_3 = px.bar(df_3, y='districts', x='registereduser', title="AVERAGE OF REGISTERED USER",hover_name="districts", orientation="h",
                color_discrete_sequence=px.colors.sequential.Greys_r , height=800, width=1000)
    st.plotly_chart(fig_amount_3)


# Function to plot top AppOpens
#sql connection
def top_chart_appopens(table_name,state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radha",
        database="Youtube_data",
        port="3306",
        auth_plugin='mysql_native_password'
        )
    cursor = mydb.cursor()

    #plot_1
    query1= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states ='{state}'
                group by districts
                order by appopens desc
                limit 10 '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("districts","appopens"))

    col1, col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x='districts', y='appopens', title=" TOP 10 APPOPENS",hover_name="districts",
                    color_discrete_sequence=px.colors.sequential.amp_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states ='{state}'
                group by districts
                order by appopens 
                limit 10 '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts","appopens"))

    with col2:
        fig_amount_2 = px.bar(df_2, x='districts', y='appopens', title="LAST 10 APPOPENS",hover_name="districts",
                    color_discrete_sequence=px.colors.sequential.algae_r , height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select districts, avg(appopens) as appopens
                from {table_name}
                where states ='{state}'
                group by districts
                order by appopens'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts","appopens"))

    fig_amount_3 = px.bar(df_3, y='districts', x='appopens', title="AVERAGE OF APPOPENS",hover_name="districts", orientation="h",
                color_discrete_sequence=px.colors.sequential.Greys_r , height=800, width=1000)
    st.plotly_chart(fig_amount_3)

# Function to plot registered users
#sql connection
def top_chart_registered_users(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radha",
        database="Youtube_data",
        port="3306",
        auth_plugin='mysql_native_password'
        )
    cursor = mydb.cursor()

    #plot_1
    query1= f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10 '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states","registeredusers"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x='states', y='registeredusers', title=" TOP 10 REGISTERED USERS",hover_name="states",
                    color_discrete_sequence=px.colors.sequential.ice, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers 
                limit 10 '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states","registeredusers"))

    with col2:
        fig_amount_2 = px.bar(df_2, x='states', y='registeredusers', title="LAST 10 REGISTERED USERS",hover_name="states",
                    color_discrete_sequence=px.colors.sequential.Mint_r , height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select states, avg(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers '''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states","registeredusers"))


    fig_amount_3 = px.bar(df_3, y='states', x='registeredusers', title="AVERAGE OF REGISTERED USERS",hover_name="states", orientation="h",
                color_discrete_sequence=px.colors.sequential.speed_r , height=800, width=1000)
    st.plotly_chart(fig_amount_3)

#Top 10 Brands by Transaction Count in Aggregated User
def top_brands_by_transaction_count(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radha",
        database="Youtube_data",
        port="3306",
        auth_plugin='mysql_native_password'
    )
    cursor = mydb.cursor()

    query = f"""
        SELECT Brands, SUM(Transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY Brands
        ORDER BY transaction_count DESC
        LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    mydb.commit()
    cursor.close()
    mydb.close()

    df = pd.DataFrame(results, columns=["Brands", "transaction_count"])

    fig = px.bar(df, x='Brands', y='transaction_count', title="Top 10 Brands by Transaction Count",
                 color_discrete_sequence=px.colors.sequential.Oranges_r)
    st.plotly_chart(fig)

#Monthly Transaction Amount Trend for a Selected State:
def monthly_transaction_trend(table_name, state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radha",
        database="Youtube_data",
        port="3306",
        auth_plugin='mysql_native_password'
    )
    cursor = mydb.cursor()

    query = f"""
        SELECT DATE_FORMAT(Date, '%Y-%m') AS month, SUM(Transaction_amount) AS transaction_amount
        FROM {table_name}
        WHERE States = '{state}'
        GROUP BY month
        ORDER BY month
    """
    cursor.execute(query)
    results = cursor.fetchall()
    mydb.commit()
    cursor.close()
    mydb.close()

    df = pd.DataFrame(results, columns=["month", "transaction_amount"])

    fig = px.line(df, x='month', y='transaction_amount', title=f"Monthly Transaction Amount Trend in {state}",
                  markers=True, color_discrete_sequence=px.colors.sequential.Emrld_r)
    st.plotly_chart(fig)



# streamlit part

st.set_page_config(layout='wide')
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

    select = option_menu("Main Menu", ["Home", "Data Exploration", "Top Charts"])

if select == "Home":

    col1,col2=st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("India's Leading Digital Payments App")
        st.markdown("### **About PhonePe**")
        st.markdown("PhonePe is a revolutionary Indian digital payments and financial technology company that offers a wide range of services and features to enhance your financial transactions.")
        
        st.markdown("### **Features**")
        st.write("- **Credit and Debit Card Linking**: Easily link your cards for quick payments.")
        st.write("- **Bank Balance Check**: Check your bank balance anytime, anywhere.")
        st.write("- **Money Storage**: Securely store money in your PhonePe wallet.")
        st.write("- **Pin Authorization**: Ensure secure transactions with PIN authorization.")
        st.write("- **Instant Money Transfer**: Transfer money instantly to anyone, anywhere.")
        st.write("- **Bill Payments**: Pay your utility bills, mobile recharges, and more effortlessly.")
        st.write("- **Insurance Services**: Buy and manage insurance policies right from the app.")
        st.write("- **Investment Options**: Invest in mutual funds, gold, and more with ease.")
        st.write("- **QR Code Payments**: Scan QR codes to make payments at stores, cabs, and more.")
        
        
    with col2:
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.image(Image.open(r"D:\phonepe_project\phonepe.image.webp"), width=600)

    col3,col4=st.columns(2)
    with col3:
        st.image(Image.open(r"D:\phonepe_project\phonepe1.image.webp"), width=500)
        
    with col4:
        st.markdown("### **Security Features**")
        st.write("- **End-to-End Encryption**: Your data is protected with advanced encryption techniques.")
        st.write("- **Fraud Detection**: Real-time fraud detection ensures your transactions are safe.")
        st.write("- **Two-Factor Authentication**: Additional layer of security with two-factor authentication.")

        st.markdown("### **Why Choose PhonePe?**")
        st.write("- **User-Friendly Interface**: Simple and intuitive interface for all age groups.")
        st.write("- **Wide Acceptance**: Accepted at millions of merchants across India.")
        st.write("- **24/7 Customer Support**: Dedicated support team available round the clock.")
        st.write("- **Innovative Solutions**: Constantly evolving with new features and services.")
        
        st.markdown("### **Download the App Now**")
        st.download_button("Download PhonePe App", "https://www.phonepe.com/app-download/")


elif select == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("Select The Method", ['Insurance Analysis', 'Transaction Analysis', 'User Analysis'])
        
        if method == 'Insurance Analysis':

            col1, col2 = st.columns(2)

            with col1:
                years = st.slider("Select the year", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(), Aggre_insurance["Years"].min())
            tac_Y = Transaction_amount_count_Y(Aggre_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                        
                    quarters = st.slider("Select the Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)


        elif method == 'Transaction Analysis':
             
             col1, col2 = st.columns(2)

             with col1:
                years = st.slider("Select the year", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(), Aggre_transaction["Years"].min())
             Aggre_tran_tac_Y = Transaction_amount_count_Y(Aggre_transaction, years)

             col1, col2 = st.columns(2)
             with col1:
                 states = st.selectbox("Select the State", Aggre_tran_tac_Y["States"].unique())

             Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)

             col1, col2 = st.columns(2)
             with col1:
                        
                    quarters = st.slider("Select the Quarter", Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(), Aggre_tran_tac_Y["Quarter"].min())
             Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)

             col1, col2 = st.columns(2)
             with col1:
                 states = st.selectbox("Select the State", Aggre_tran_tac_Y_Q["States"].unique(), key='states_Q')
                             
             Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)

        elif method == 'User Analysis':

            col1, col2 = st.columns(2)
            with col1:
                        
                    years = st.slider("Select the Quarter", Aggre_user["Years"].min(), Aggre_user["Years"].max(), Aggre_user["Years"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)


            col1, col2 = st.columns(2)
            with col1:
                        
                    quarters = st.slider("Select the Quarter", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Agree_user_plot_2(Aggre_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                 states = st.selectbox("Select the State", Aggre_user_Y_Q["States"].unique(), key='states_r')
                             
            Agree_user_plot_3(Aggre_user_Y_Q, states)
                

    with tab2:
        method_2 = st.radio('Select The Method', ['Map Insurance', 'Map Transaction', 'Map User'])

        if method_2 == 'Map Insurance':

            col1, col2 = st.columns(2)

            with col1:
                years = st.slider("Select the year", map_insurance["Years"].min(), map_insurance["Years"].max(), map_insurance["Years"].min(), key='year_Q')
            map_insur_tac_Y = Transaction_amount_count_Y(map_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                 states = st.selectbox("Select the State", map_insur_tac_Y["States"].unique(), key='states_c')
            Map_insur_District(map_insur_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                        
                    quarters = st.slider("Select the Quarter", map_insur_tac_Y["Quarter"].min(), map_insur_tac_Y["Quarter"].max(), map_insur_tac_Y["Quarter"].min(), key='Quarter_Q')
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                 states = st.selectbox("Select the State", map_insur_tac_Y_Q["States"].unique(), key='states_x')
                             
            Map_insur_District(map_insur_tac_Y_Q, states)
        

        elif method_2 == 'Map Transaction':

            col1, col2 = st.columns(2)

            with col1:
                years = st.slider("Select the year", map_transaction["Years"].min(), map_transaction["Years"].max(), map_transaction["Years"].min(), key='year_k')
            map_tran_tac_Y = Transaction_amount_count_Y(map_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                 states = st.selectbox("Select the State", map_tran_tac_Y["States"].unique(), key='states_m')
            Map_insur_District(map_tran_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                        
                    quarters = st.slider("Select the Quarter", map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(), map_tran_tac_Y["Quarter"].min(), key='Quarter_l')
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                 states = st.selectbox("Select the State", map_tran_tac_Y_Q["States"].unique(), key='states_p')
                             
            Map_insur_District(map_tran_tac_Y_Q, states)


        elif method_2 == 'Map User':
              col1, col2 = st.columns(2)

              with col1:
                years = st.slider("Select the year", map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min(), key='year_v')
              map_user_Y = map_user_plot_1(map_user, years)

              col1, col2 = st.columns(2)
              with col1:
                        
                    quarters = st.slider("Select the Quarter", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min(), key='Quarter_m')
              map_user_Y_Q = map_user_plot_2(map_user_Y, quarters)

              col1, col2 = st.columns(2)
              with col1:
                 states = st.selectbox("Select the State", map_user_Y_Q["States"].unique())
                             
              map_user_plot_3(map_user_Y_Q, states)
            

    with tab3:
        method_3 = st.radio('Select The Method', ['Top Insurance', 'Top Transaction', 'Top user'])

        if method_3 == 'Top Insurance':
            col1, col2 = st.columns(2)

            with col1:
                years = st.slider("Select the year", top_insurance["Years"].min(), top_insurance["Years"].max(), top_insurance["Years"].min(), key='year_t')
            top_insur_tac_Y = Transaction_amount_count_Y(top_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                 states = st.selectbox("Select the State", top_insur_tac_Y["States"].unique(), key='states_Se')                      
            Top_insurance_plot_1(top_insur_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                        
                    quarters = st.slider("Select the Quarter", top_insur_tac_Y["Quarter"].min(), top_insur_tac_Y["Quarter"].max(), top_insur_tac_Y["Quarter"].min(), key='Quarter_t')
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)


        elif method_3 == 'Top Transaction':

            col1, col2 = st.columns(2)

            with col1:
                years = st.slider("Select the year", top_transaction["Years"].min(), top_transaction["Years"].max(), top_transaction["Years"].min(), key='year_ty')
            top_tran_tac_Y = Transaction_amount_count_Y(top_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                 states = st.selectbox("Select the State", top_tran_tac_Y["States"].unique(), key='states_tt')                      
            Top_insurance_plot_1(top_tran_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                        
                    quarters = st.slider("Select the Quarter", top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(), top_tran_tac_Y["Quarter"].min(), key='Quarter_tt')
            top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)


        elif method_3 == 'Top User':

            col1, col2 = st.columns(2)

        with col1:
            years = st.slider("Select the year", int(top_user["Years"].min()), int(top_user["Years"].max()), int(top_user["Years"].min()), key='year_tp')
        top_user_Y = top_user_plot_1(top_user, years)

        col1, col2 = st.columns(2)
        with col1:
            states = st.selectbox("Select the State", top_user_Y["States"].unique(), key='states_to')
        top_user_plot_2(top_user_Y, states)
            



elif select == "Top Charts":
    question = st.selectbox("Select the Question", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered user of Map User",
                                                    "9. AppOpens of Map User",
                                                    "10. Registered Users of Top User",
                                                    "11. Top 10 Brands by Transaction Count in Aggregated User",
                                                    "12. Monthly Transaction Amount Trend for a Selected State"])

    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":
    
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered user of Map User":
        
       states = st.selectbox("Select the state",  map_user["States"].unique())
       st.subheader("REGISTERED USERS")
       top_chart_registered_user("map_user", states)

    elif question == "9. AppOpens of Map User":
        
       states = st.selectbox("Select the state",  map_user["States"].unique())
       st.subheader("APPOPENS")
       top_chart_appopens("map_user", states)

    elif question == "10. Registered Users of Top User":        
       
       st.subheader("REGISTERED USERS OF TOP USERS")
       top_chart_registered_users("top_user")

    elif question == "11. Top 10 Brands by Transaction Count in Aggregated User":        
       
        st.subheader("TOP BRANDS IN AGGREGATED USER")
        top_brands_by_transaction_count("aggregated_user")

    """elif question == "12. Monthly Transaction Amount Trend for a Selected State":        
       
       state = st.selectbox("Select the state", map_transaction["States"].unique())
       st.subheader(f"MONTHLY TRANSACTION AMOUNT TREND IN {state.upper()}")
       monthly_transaction_trend("map_transaction", state)"""
    
    
    
    

    



import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image

# DataFrame Creation

#sql connection

mydb= mysql.connector.connect(host="localhost",
                      user="santhosh",
                      port="3306",
                      database="phonepe_data",
                      password="santhosh",
                      auth_plugin= "mysql_native_password")

cursor= mydb.cursor(buffered=True)

#Aggre_insurance_df

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance= pd.DataFrame(table1, columns=("States","Years","Quarter","Transaction_type",
                                               "Transaction_count","Transaction_amount"))

#Aggre_transaction_df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2, columns=("States","Years","Quarter","Transaction_type",
                                               "Transaction_count","Transaction_amount"))

#Aggre_user_df

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user= pd.DataFrame(table3, columns=("States","Years","Quarter","Brands",
                                               "Transaction_count","Percentage"))

#Map_insurance_df

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

Map_insurance= pd.DataFrame(table4, columns=("States","Years","Quarter","Districts",
                                               "Transaction_count","Transaction_amount")) 

#Map_transaction_df

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

Map_transaction= pd.DataFrame(table5, columns=("States","Years","Quarter","Districts",
                                               "Transaction_count","Transaction_amount"))  

#Map_user_df

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

Map_user= pd.DataFrame(table6, columns=("States","Years","Quarter","Districts",
                                               "RegisteredUsers","AppOpens"))

#Top_insurance_df

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

Top_insurance= pd.DataFrame(table7, columns=("States","Years","Quarter","Pincodes",
                                               "Transaction_count","Transaction_amount"))

#Top_transaction_df

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

Top_transaction= pd.DataFrame(table8, columns=("States","Years","Quarter","Pincodes",
                                               "Transaction_count","Transaction_amount"))

#Top_user_df

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

Top_user= pd.DataFrame(table9, columns=("States","Years","Quarter","Pincodes",
                                               "Registered_users"))

def Transaction_amount_count_Y(df,year):

    #Transaction Amount Count Year= TACY
    TACY=df[df["Years"]== year]
    TACY.reset_index(drop=True, inplace= True)

    TACY_G=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACY_G.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount= px.bar(TACY_G, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount)
    
    with col2:

        fig_count= px.bar(TACY_G, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)

    
    col1,col2= st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)

        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()    

        fig_india_1= px.choropleth(TACY_G, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(TACY_G["Transaction_amount"].min(),TACY_G["Transaction_amount"].max()),
                                hover_name= "States",title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    
    with col2:

        fig_india_2= px.choropleth(TACY_G, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACY_G["Transaction_count"].min(),TACY_G["Transaction_count"].max()),
                                hover_name= "States",title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return TACY

def Transaction_amount_count_Y_Q(df, quarter):

    #Transaction Amount Count Year= TACY
    TACY=df[df["Quarter"]== quarter]
    TACY.reset_index(drop=True, inplace= True)

    TACY_G=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACY_G.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount= px.bar(TACY_G, x="States", y="Transaction_amount", title=f"{TACY["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count= px.bar(TACY_G, x="States", y="Transaction_count", title=f"{TACY["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)

        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()    

        fig_india_1= px.choropleth(TACY_G, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(TACY_G["Transaction_amount"].min(),TACY_G["Transaction_amount"].max()),
                                hover_name= "States",title= f"{TACY["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:    

        fig_india_2= px.choropleth(TACY_G, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACY_G["Transaction_count"].min(),TACY_G["Transaction_count"].max()),
                                hover_name= "States",title= f"{TACY["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return TACY    

def Aggre_trans_Transaction_type(df, state):

    TACY=df[df["States"]== state]
    TACY.reset_index(drop=True, inplace= True)

    TACY_G=TACY.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    TACY_G.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=TACY_G, names="Transaction_type", values= "Transaction_amount",
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)

    with col2:

        fig_pie_2=px.pie(data_frame=TACY_G, names="Transaction_type", values= "Transaction_count",
                        width=600, title= f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)  


#Aggre_User_Analysis_1

def Aggre_user_plot_01(df, year):

    aguy=df[df["Years"]==year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_01= px.bar(aguyg, x="Brands", y="Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.Bluered, hover_name= "Brands")

    st.plotly_chart(fig_bar_01)

    return aguy 

# Aggre_user_Analysis_2
def Aggre_user_plot_02(df, quarter):
    aguyq=df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)
    
    fig_bar_01= px.bar(aguyqg, x="Brands", y="Transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                        width=1000, color_discrete_sequence=px.colors.sequential.Bluered, hover_name= "Brands")
    st.plotly_chart(fig_bar_01)

    return aguyq

#Aggre_user_analysis_3

def Aggre_user_plot_03(df, state):
    aguyqs=df[df["States"]== state]
    aguyqs.reset_index(drop= True, inplace= True)

    
    fig_line_1= px.line(aguyqs, x="Brands", y="Transaction_count", hover_data="Percentage",
                        title= f"{state.upper()}: BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000, markers= True)
    st.plotly_chart(fig_line_1)
    

#Map_insurance_district
def Map_insur_Districts(df, state):

    TACY=df[df["States"]== state]
    TACY.reset_index(drop=True, inplace= True)

    TACY_G=TACY.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    TACY_G.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1=px.bar(TACY_G, x= "Transaction_amount", y="Districts", orientation="h", height= 600,
                     title=f"{state.upper()}, DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Purples)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2=px.bar(TACY_G, x= "Transaction_count", y="Districts", orientation="h", height= 600,
                        title=f"{state.upper()}, DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_bar_2)  

# map_user_plot_1

def map_user_plot_1(df, year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop= True, inplace= True)

    muyg=muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x="States", y=["RegisteredUsers","AppOpens"],
                            title= f"{year}: REGISTERUSER, APPOPENS", width=1000, height= 800, markers= True,
                            color_discrete_sequence= px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_line_1)

    return muy   

# map_user_plot_2

def map_user_plot_2(df, quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg=muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_2= px.line(muyqg, x="States", y=["RegisteredUsers","AppOpens"],
                            title= f"{df['Years'].min()} YEAR {quarter} QUARTER : REGISTERUSER, APPOPENS", width=1000, height= 800, markers= True,
                            color_discrete_sequence= px.colors.sequential.Hot_r)
    st.plotly_chart(fig_line_2)

    return muyq  

#Map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.drop_duplicates(inplace= True)
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_map_bar_1= px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation= "h",
                            title=f"{states.upper()} REGISTRED USER", height=800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:

        fig_map_bar_2= px.bar(muyqs, x="AppOpens", y="Districts", orientation= "h",
                            title=f"{states.upper()} APPOPENS ", height=800, color_discrete_sequence= px.colors.sequential.Blues_r)
        st.plotly_chart(fig_map_bar_2)

#Top_insurance_plot_1
def Top_insurance_plot_1(df, state):

    tiy=df[df["States"]==state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_top_insur_bar_1= px.bar(tiy, x="Quarter", y="Transaction_amount",hover_data= "Pincodes",
                                title="TRANSACTION AMOUNT", height=650, width=600, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:    

        fig_top_insur_bar_2= px.bar(tiy, x="Quarter", y="Transaction_count",hover_data= "Pincodes",
                                title="TRANSACTION COUNT", height=650, width=600, color_discrete_sequence= px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_top_insur_bar_2)

# Top_User_polt_1
def Top_user_plot_1(df, year):
    tuy=df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg=pd.DataFrame(tuy.groupby(["States", "Quarter"])["Registered_users"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x="States", y= "Registered_users", color= "Quarter",width=1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Oranges_r, hover_name="States",
                        title=f"{year}: REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

#Top_user-plot_2
def Top_user_plot_2(df, state):
    tuys=df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2= px.bar(tuys, x= "Quarter", y= "Registered_users", title= "REGISTERED USERS, PINCODES, QUARTER",
                        width=1000, height= 800, color="Registered_users", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)

#sql connection

def Top_chart_transaction_amount(table_name):
    mydb= mysql.connector.connect(host="localhost",
                      user="santhosh",
                      port="3306",
                      database="phonepe_data",
                      password="santhosh",
                      auth_plugin= "mysql_native_password")
    cursor= mydb.cursor()

    # Plot_1
    query_1= f"""select States, sum(Transaction_amount) as Transaction_amount
                from {table_name}
                group by States
                order by Transaction_amount desc
                limit 10;"""
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States", "Transaction_amount"))
    col1,col2= st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="States", y="Transaction_amount", title= "TOP 10 STATES", hover_name= "States",
                             color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #Plot_2
    query_2= f"""select States, sum(Transaction_amount) as Transaction_amount
                from {table_name}
                group by States
                order by Transaction_amount 
                limit 10;"""
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States", "Transaction_amount"))

    with col2:

        fig_amount_2= px.bar(df_2, x="States", y="Transaction_amount", title= "LAST 10 STATES", hover_name= "States",
                             color_discrete_sequence=px.colors.sequential.Pinkyl,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #Plot_3
    query_3= f"""select States, avg(Transaction_amount) as Transaction_amount
                from {table_name}
                group by States
                order by Transaction_amount;"""
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States", "Transaction_amount"))

    fig_amount_3= px.bar(df_3, x="Transaction_amount", y="States", title= "AVG TRANSACTION AMOUNT", hover_name= "States", orientation= "h",
                         color_discrete_sequence=px.colors.sequential.ice_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#sql connection

def Top_chart_transaction_count(table_name):
    mydb= mysql.connector.connect(host="localhost",
                      user="santhosh",
                      port="3306",
                      database="phonepe_data",
                      password="santhosh",
                      auth_plugin= "mysql_native_password")
    
    cursor= mydb.cursor()

    # Plot_1
    query_1= f"""select States, sum(Transaction_count) as Transaction_count
                from {table_name}
                group by States
                order by Transaction_count desc
                limit 10;"""
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States", "Transaction_count"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount_1= px.bar(df_1, x="States", y="Transaction_count", title= " TOP 10 STATES", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #Plot_2
    query_2= f"""select States, sum(Transaction_count) as Transaction_count
                from {table_name}
                group by States
                order by Transaction_count 
                limit 10;"""
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States", "Transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="States", y="Transaction_count", title= "LAST 10 STATES", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Pinkyl,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #Plot_3
    query_3= f"""select States, avg(Transaction_count) as Transaction_count
                from {table_name}
                group by States
                order by Transaction_count;"""
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States", "Transaction_count"))

    fig_amount_3= px.bar(df_3, x="Transaction_count", y="States", title= "AVG TRANSACTION COUNT", hover_name= "States", orientation= "h",
                    color_discrete_sequence=px.colors.sequential.ice_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)


#sql connection

def Top_chart_registered_user(table_name, state):
    mydb= mysql.connector.connect(host="localhost",
                      user="santhosh",
                      port="3306",
                      database="phonepe_data",
                      password="santhosh",
                      auth_plugin= "mysql_native_password")

    cursor= mydb.cursor()

    # Plot_1
    query_1= f"""select Districts, sum(RegisteredUsers) as RegisterUsers
                 from {table_name}
                 where States='{state}'
                 group by Districts
                 order by RegisterUsers desc
                 limit 10;"""
                 
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "RegisterUsers"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="Districts", y="RegisterUsers", title= "TOP 10 REGISTERED USER", hover_name= "Districts",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #Plot_2
    query_2= f"""select Districts, sum(RegisteredUsers) as RegisterUsers
                 from {table_name}
                 where States='{state}'
                 group by Districts
                 order by RegisterUsers
                 limit 10;"""
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "RegisterUsers"))

    with col2:

        fig_amount_2= px.bar(df_2, x="Districts", y="RegisterUsers", title= "LAST 10 REGISTERED USER", hover_name= "Districts",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #Plot_3
    query_3= f"""select Districts, avg(RegisteredUsers) as RegisterUsers
                 from {table_name}
                 where States='{state}'
                 group by Districts
                 order by RegisterUsers;"""
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "RegisterUsers"))

    fig_amount_3= px.bar(df_3, x="RegisterUsers", y="Districts", title= "AVG OF REGISTER USER", hover_name= "Districts", orientation= "h",
                    color_discrete_sequence=px.colors.sequential.Magenta_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#sql connection

def Top_chart_appopens(table_name, state):
    mydb= mysql.connector.connect(host="localhost",
                      user="santhosh",
                      port="3306",
                      database="phonepe_data",
                      password="santhosh",
                      auth_plugin= "mysql_native_password")

    cursor= mydb.cursor()

    # Plot_1
    query_1= f"""select Districts, sum(AppOpens) as AppOpens
                 from {table_name}
                 where States='{state}'
                 group by Districts
                 order by AppOpens desc
                 limit 10;"""
                 
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "AppOpens"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="Districts", y="AppOpens", title= "TOP 10 APPOPENS", hover_name= "Districts",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #Plot_2
    query_2= f"""select Districts, sum(AppOpens) as AppOpens
                 from {table_name}
                 where States='{state}'
                 group by Districts
                 order by AppOpens
                 limit 10;"""
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "AppOpens"))

    with col2:
        fig_amount_2= px.bar(df_2, x="Districts", y="AppOpens", title= "LAST 10 APPOPENS", hover_name= "Districts",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #Plot_3
    query_3= f"""select Districts, avg(AppOpens) as AppOpens
                 from {table_name}
                 where States='{state}'
                 group by Districts
                 order by AppOpens;"""
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "AppOpens"))

    fig_amount_3= px.bar(df_3, x="AppOpens", y="Districts", title= "AVG OF APPOPENS", hover_name= "Districts", orientation= "h",
                    color_discrete_sequence=px.colors.sequential.Magenta_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#sql connection

def Top_chart_registered_users(table_name):
    mydb= mysql.connector.connect(host="localhost",
                      user="santhosh",
                      port="3306",
                      database="phonepe_data",
                      password="santhosh",
                      auth_plugin= "mysql_native_password")

    cursor= mydb.cursor()

    # Plot_1
    query_1= f"""select States, sum(Registered_users) as Registered_users
                 from {table_name}
                 group by States
                 order by Registered_users desc
                 limit 10;"""
                 
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("States", "Registered_users"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="States", y="Registered_users", title= "TOP 10 STATES", hover_name= "States",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #Plot_2
    query_2= f"""select States, sum(Registered_users) as Registered_users
                 from {table_name}
                 group by States
                 order by Registered_users 
                 limit 10;"""
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("States", "Registered_users"))

    with col2: 
        fig_amount_2= px.bar(df_2, x="States", y="Registered_users", title= "LAST 10 STATES", hover_name= "States",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #Plot_3
    query_3= f"""select States, avg(Registered_users) as Registered_users
                 from {table_name}
                 group by States
                 order by Registered_users;"""
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("States", "Registered_users"))

    fig_amount_3= px.bar(df_3, x="Registered_users", y="States", title= "AVG OF REGISTER USER", hover_name= "States", orientation= "h",
                    color_discrete_sequence=px.colors.sequential.ice_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)




# Streamlit Part

st.set_page_config(layout="wide")

select=option_menu(menu_title=None, options=["HOME","ABOUT","DATA EXPLORATION","INSIGHTS"], icons=["house","book","bar-chart-fill"] ,orientation="horizontal",
                   default_index=0,
                   styles={"container":{"padding": "0!important", "background-color": "black", "size": "cover"},
                           "icons":{"color": "white", "font-size": "20px"},
                           "nav-link":{"font-size": "20px", "text-align":"center", "margin": "-2px", "--hover-color": "#6F36AD"},
                           "nav-link-selected": {"background-color": "#6F36AD"}})
if select == "HOME":

    st.image(Image.open(r"C:\Users\Santhosh\Desktop\CapstoneProject\Capstone\Phonepe\PhonePe_pic-removebg-preview.png"),width=175)

   

    col1,col2 = st.columns(2)
    with col1:
        st.subheader( "PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.markdown("  ")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:

        st.video(r"C:\Users\Santhosh\Desktop\CapstoneProject\Capstone\Phonepe\Phonepe video.mp4")

    
if select == "ABOUT":
    st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    col1,col2 = st.columns(2)

    with col1:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        

        st.image(Image.open(r"C:\Users\Santhosh\Desktop\CapstoneProject\Capstone\Phonepe\phonepe.jpg"),width=600)

        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:
        st.subheader("Phonepe Now Everywhere..!")
        st.video(r"C:\Users\Santhosh\Desktop\CapstoneProject\Capstone\Phonepe\phonepe video2.mp4")

elif select == "DATA EXPLORATION":

    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method_1=st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])
        
        if method_1 == "Insurance Analysis":
           
           col1,col2= st.columns(2)
           with col1:
           
            years= st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
           TACY_Y= Transaction_amount_count_Y(Aggre_insurance,years)

           col1,col2= st.columns(2)
           with col1:
               
               quarters= st.slider("Select The Quarter",TACY_Y["Quarter"].min(),TACY_Y["Quarter"].max(),TACY_Y["Quarter"].min())
           Transaction_amount_count_Y_Q(TACY_Y, quarters)

        elif method_1 == "Transaction Analysis":

            col1,col2= st.columns(2)
            with col1:
           
             years= st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_trans_TACY_Y= Transaction_amount_count_Y(Aggre_transaction,years)
            
            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State", Aggre_trans_TACY_Y["States"].unique())

            Aggre_trans_Transaction_type(Aggre_trans_TACY_Y, states)

            col1,col2= st.columns(2)
            with col1:
               
               quarters= st.slider("Select The Quarter",Aggre_trans_TACY_Y["Quarter"].min(),Aggre_trans_TACY_Y["Quarter"].max(),Aggre_trans_TACY_Y["Quarter"].min())
            Aggre_trans_TACY_Y_Q = Transaction_amount_count_Y_Q(Aggre_trans_TACY_Y, quarters)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_TA", Aggre_trans_TACY_Y_Q["States"].unique())

            Aggre_trans_Transaction_type(Aggre_trans_TACY_Y_Q, states)   
            
             

        elif method_1 == "User Analysis":
            
            col1,col2= st.columns(2)
            with col1:
           
             years= st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_year= Aggre_user_plot_01(Aggre_user, years)
            
            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",Aggre_user_year["Quarter"].min(),Aggre_user_year["Quarter"].max(),Aggre_user_year["Quarter"].min())
            Aggre_user_year_quarter = Aggre_user_plot_02(Aggre_user_year, quarters)
        
            
            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State", Aggre_user_year_quarter["States"].unique())

            Aggre_user_plot_03(Aggre_user_year_quarter, states)


    with tab2:

        method_2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method_2 == "Map Insurance":
            
            col1,col2= st.columns(2)
            with col1:
           
               years= st.slider("Select The Year_MI",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            Map_insur_TAC_Y= Transaction_amount_count_Y(Map_insurance,years) 


            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_MI", Map_insur_TAC_Y["States"].unique())

            Map_insur_Districts(Map_insur_TAC_Y, states)

            col1,col2= st.columns(2)
            with col1:
               
               quarters= st.slider("Select The Quarter_MI",Map_insur_TAC_Y["Quarter"].min(),Map_insur_TAC_Y["Quarter"].max(),Map_insur_TAC_Y["Quarter"].min())
            Map_insur_TAC_Y_Q = Transaction_amount_count_Y_Q(Map_insur_TAC_Y, quarters)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_MA", Map_insur_TAC_Y_Q["States"].unique())

            Map_insur_Districts(Map_insur_TAC_Y_Q, states)   

           
        elif method_2 == "Map Transaction":
            col1,col2= st.columns(2)
            with col1:
           
               years= st.slider("Select The Year_MI",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            Map_tran_TAC_Y= Transaction_amount_count_Y(Map_transaction,years) 


            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_MI", Map_tran_TAC_Y["States"].unique())

            Map_insur_Districts(Map_tran_TAC_Y, states)

            col1,col2= st.columns(2)
            with col1:
               
               quarters= st.slider("Select The Quarter_MI",Map_tran_TAC_Y["Quarter"].min(),Map_tran_TAC_Y["Quarter"].max(),Map_tran_TAC_Y["Quarter"].min())
            Map_tran_TAC_Y_Q = Transaction_amount_count_Y_Q(Map_tran_TAC_Y, quarters)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_MA", Map_tran_TAC_Y_Q["States"].unique())

            Map_insur_Districts(Map_tran_TAC_Y_Q, states)

        elif method_2 == "Map User":

            col1,col2= st.columns(2)
            with col1:
           
               years= st.slider("Select The Year_MU",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            Map_user_Y= map_user_plot_1(Map_user, years)

            col1,col2= st.columns(2)
            with col1:
               
               quarters= st.slider("Select The Quarter_MU",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q = map_user_plot_2(Map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_MU", Map_user_Y_Q["States"].unique())

            map_user_plot_3(Map_user_Y_Q, states)
            

    with tab3:

        method_3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method_3 == "Top Insurance":
            
            col1,col2= st.columns(2)
            with col1:
           
               years= st.slider("Select The Year_TI",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_insur_TAC_Y= Transaction_amount_count_Y(Top_insurance,years)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_TI", Top_insur_TAC_Y["States"].unique())

            Top_insurance_plot_1(Top_insur_TAC_Y, states) 

            col1,col2= st.columns(2)
            with col1:
               
               quarters= st.slider("Select The Quarter_TI",Top_insur_TAC_Y["Quarter"].min(),Top_insur_TAC_Y["Quarter"].max(),Top_insur_TAC_Y["Quarter"].min())
            Top_insur_TAC__Y_Q = Transaction_amount_count_Y_Q(Top_insur_TAC_Y, quarters)

        elif method_3 == "Top Transaction":
            
            col1,col2= st.columns(2)
            with col1:
           
               years= st.slider("Select The Year_TT",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_tran_TAC_Y= Transaction_amount_count_Y(Top_transaction,years)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_TT", Top_tran_TAC_Y["States"].unique())

            Top_insurance_plot_1(Top_tran_TAC_Y, states) 

            col1,col2= st.columns(2)
            with col1:
               
               quarters= st.slider("Select The Quarter_TT",Top_tran_TAC_Y["Quarter"].min(),Top_tran_TAC_Y["Quarter"].max(),Top_tran_TAC_Y["Quarter"].min())
            Top_tran_TAC__Y_Q = Transaction_amount_count_Y_Q(Top_tran_TAC_Y, quarters)

        elif method_3 == "Top User":
            
            col1,col2= st.columns(2)
            with col1:
           
               years= st.slider("Select The Year_TU",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_TAC_Y= Top_user_plot_1(Top_user,years)

            col1,col2= st.columns(2)
            with col1:

                states= st.selectbox("Select The State_TU", Top_user_TAC_Y["States"].unique())

            Top_user_plot_2(Top_user_TAC_Y, states) 

elif select == "INSIGHTS":
    Question= st.selectbox("Select The Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                  "2. Transaction Amount and Count of Map Insurance",
                                                  "3. Transaction Amount and Count of Top Insurance",
                                                  "4. Transaction Amount and count of Aggregated Transaction",
                                                  "5. Transaction Amount and Count of Map Transaction",
                                                  "6. Transaction Amount and Count of Top Transaction",
                                                  "7. Transaction count of Aggregated User",
                                                  "8. Registred User of Map User",
                                                  "9. App opens of Map User",
                                                  "10. Registred User of Top User"
                                                  ])
    
    if Question== "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_insurance")

    elif Question== "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_insurance")    

    elif Question== "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_insurance")

    elif Question== "4. Transaction Amount and count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_transaction")  

    elif Question== "5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_transaction")

    elif Question== "6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_transaction")
 
    elif Question== "7. Transaction count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_user")

    elif Question== "8. Registred User of Map User":
        
        states= st.selectbox("Select The State", Map_user["States"].unique())
        st.subheader("REGISTERED USER")
        Top_chart_registered_user("map_user", states)

    elif Question== "9. App opens of Map User":
        
        states= st.selectbox("Select The State", Map_user["States"].unique())
        st.subheader("APPOPENS")
        Top_chart_appopens("map_user", states)
    
    elif Question== "10. Registred User of Top User":
        
        st.subheader("REGISTERED USER")
        Top_chart_registered_users("top_user")
#************************  Libraries and Modules #**************************************
import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import camelot
import json
import requests
import tabula


# *****************************************************************************************************************************
st.set_page_config(page_title = 'Homelessness in LA', 
    layout='wide',
    page_icon='')

st.title('Homelessness in LA')

st.markdown(""" 
This dashboard will provide a simple statistical visualiztion of homelessness in LA and connection of Racidivism with it. 
We will see the existing services in the area and neighboring cities helping to end Recidivism and Homelessness.

#### **Data source:**
*   [HUD EXCHANGE](https://www.hudexchange.info/programs/coc/coc-homeless-populations-and-subpopulations-reports/?filter_Year=&filter_Scope=&filter_State=&filter_CoC=&program=CoC&group=PopSub)
*   [Greater LOS ANGELES Homeless Count](https://www.lahsa.org/documents?id=4692-2020-greater-los-angeles-homeless-count-total-point-in-time-homeless-population-by-geographic-areas).
*   [311 Homeless Encampments Requests](https://data.lacity.org/City-Infrastructure-Service-Requests/311-Homeless-Encampments-Requests/az43-p47q).
*   [Local Homeless Shelter Data](https://www.kaggle.com/rezag7/homeless-dataset).
*   [Offender Recidivism](https://data.ok.gov/dataset/offender-recidivism/resource/5fbf505b-994c-4d9a-be7a-4356fde1e538/).
*   [Directory Of Service Providers](https://data.ca.gov/dataset/directory-of-service-providers1/resource/2b77a934-7425-4539-9caf-fa05bbabbe59/).
*   [Los Angeles Homeless Services Authority](https://www.lahsa.org/documents?id=4680-2020-greater-los-angeles-homeless-count-city-of-los-angeles)
*   [CALIFORNIA OPEN DATA](https://data.ca.gov/dataset/monthly-admissions-and-releases/resource/678df413-638f-4294-a03c-a4ac0399368e)
*   [Crime and Incarceration by State](https://www.kaggle.com/christophercorrea/prisoners-and-crime-in-united-states?select=crime_and_incarceration_by_state.csv)
*   [California Department of Corrections and Rehabilitation](https://www.cdcr.ca.gov/research/wp-content/uploads/sites/174/2021/03/Recidivism-Report-for-Offenders-Released-in-Fiscal-Year-2014-15.pdf)
""")
# ************************************************ Dataframes ***************************************************************************

df1 = pd.read_csv('data/homeless_prep.csv')
new = df1.filter(['AGE','GENDER','substanceabuse','probation','assistancetype','VETERAN','NIGHTS'],axis=1)

DATA_URL = ('data/services.csv')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data = load_data(24038)
tables = camelot.read_pdf('data/homeless_popu.pdf',pages="all",flavor="lattice")
# tables.n # This object will show how many tables are extracted from a pdf
tables.export("data/homeless_percent.csv")


# *************************************************Sidebar Menu******************************************************************

st.sidebar.header('Main Menu')


selected_col = st.sidebar.multiselect('Homlessness Statisitcs', new.columns)

# Sidebar - Service selection in CA by county

selected_pos = st.sidebar.multiselect('Homeless Services',data['services'])

# Sidebar - Arrest Data in LA
felon = pd.read_csv("data/felon.csv")
unique_pos =  felon['Type of Conviction']
selected_pos = st.sidebar.multiselect('LA Arrest Statistics', unique_pos)

st.sidebar.markdown(f'<b>Contact</b>',unsafe_allow_html=True)
st.sidebar.markdown(f'Phone   717-999-222',unsafe_allow_html=True)
st.sidebar.markdown(f'Email   info@homeless.org',unsafe_allow_html=True)

#***************************************## First Section *********************************************
df1 = pd.read_csv('data/homeless_prep.csv')
new = df1.filter(['AGE','GENDER','substanceabuse','probation','assistancetype','VETERAN','NIGHTS'],axis=1)

# Create components 
st.markdown("## Los Angeles Homeless Statistics")

first, second, third = st.beta_columns(3)

with first:
    st.markdown(f'<h4 style="text-align: left; color: blue;">2020 Greater LA Homeless Count</h4>',unsafe_allow_html=True)
    total = pd.read_excel("data/homeless_percent-page-1-table-1.xlsx")
    number1 = total.Total.sum()  
    st.markdown(f"<h2 style='text-align: left; color: red;'>{number1}</h2>", unsafe_allow_html=True)

with second:
    st.markdown(f'<h4 style="text-align: center; color: blue;">311 Homeless Encampments Requests(2017-2018)</h4>',unsafe_allow_html=True)
    ra = requests.get("https://data.lacity.org/resource/az43-p47q.json")
    data = ra.json()
    df = pd.json_normalize(data)
    number2 = df.status.count()
    st.markdown(f"<h2 style='text-align: center; color: red;'>{number2}</h2>", unsafe_allow_html=True)

with third:
    st.markdown(f'<h4 style="text-align: center; color: blue;"> Homeless Demographic by Race </h4>',unsafe_allow_html=True)
    demograph = pd.read_excel('data/demograph.xlsx')
    hispanic  = demograph['Total'][0]
    nHispanic = demograph['Total'][1]
    st.markdown(f"<h4 style='text-align: right; color: black;'> Non Hispanic</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: right; color: red;'> {nHispanic} </h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: right; color: black;'> Hispanic </h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: right; color: red;'> {hispanic} </h4>", unsafe_allow_html=True)


st.markdown("", unsafe_allow_html=True) 

chart_1 = st.beta_container()

with chart_1:
    homeless_stat = pd.DataFrame(new)

    fig = px.scatter(homeless_stat, x="AGE", y="GENDER",
            color="NIGHTS",opacity=0.9,
            hover_data=['assistancetype','substanceabuse','probation','VETERAN']                
        )
    fig.update_layout(
    height=500,
    title_text='LA County Local Shelter Data Analytics')
    st.plotly_chart(fig)
    
st.markdown("<hr/>", unsafe_allow_html=True)   

# ************************************** Second Section **********************************************
 
DATA_URL = ('data/services.csv')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data = load_data(24038)

st.markdown("## Services in Los Angeles and Surrounding Cities")

first, second, third, fourth ,fifth = st.beta_columns(5)

with first:
    st.markdown(f'<h4 style="text-align: left; color: blue;">Homeless</h4>',unsafe_allow_html=True)
    number1 = data['services'].isin(["Homeless Services"]).sum()    
    st.markdown(f"<h1 style='text-align: left; color: red;font-size: 30px;'>{number1}</h1>", unsafe_allow_html=True)

with second:
    st.markdown(f'<h4 style="text-align: left; color: blue;">Emergency</h4>',unsafe_allow_html=True)
    number2 = data ['services'].isin(["Emergency Services"]).sum() 
    st.markdown(f"<h1 style='text-align: left; color: red;font-size: 30px;'>{number2}</h1>", unsafe_allow_html=True)

with third:
    st.markdown(f'<h4 style="text-align: left; color: blue;">Employment</h4>',unsafe_allow_html=True)
    number3 = data['services'].isin(["Employment Services"]).sum()
    st.markdown(f"<h1 style='text-align: left; color: red;font-size: 30px;'>{number3}</h1>", unsafe_allow_html=True)

with fourth:
    st.markdown(f'<h4 style="text-align: left; color: blue;">Health</h4>',unsafe_allow_html=True)
    number4 = data['services'].isin(["Health Services"]).sum()
    st.markdown(f"<h1 style='text-align:left; color: red; font-size: 30px;'>{number4}</h1>", unsafe_allow_html=True)

with fifth:
    st.markdown(f'<h4 style="text-align: left; color: blue;"> Food/Nutrition</h4>',unsafe_allow_html=True)
    number5 = data['services'].isin(["Food/Nutrition Services"]).sum()
    st.markdown(f"<h1 style='text-align:left; color: red; font-size: 30px;'>{number5}</h1>", unsafe_allow_html=True)

chart_1,chart_2 = st.beta_columns(2)

with chart_1:
    contain1 = st.beta_container()
    with contain1:
        st.map(data,use_container_width=True)    
    
with chart_2:
    contain2 = st.beta_container()
    with contain2:
        fig = px.scatter_mapbox(data_frame = data, lat="latitude", lon="longitude", color="services",hover_name="services",hover_data=data,title="Service Provider Infomation",width=800,height=500,zoom=6,size_max=10)
        fig.update_layout(mapbox_style="open-street-map") 
        fig
    
st.markdown("<hr/>", unsafe_allow_html=True)

# ****************************************** Third Section *********************************************************** 

st.markdown("## Recidivism Statistics")

chart_1, chart_2= st.beta_columns(2)

with chart_1:    
    dfs = pd.read_csv('data/return.csv')
    dfs['FY 2008-09'] = pd.to_numeric(dfs['FY 2008-09'], errors='coerce')
    dfs['FY 2009-10'] = pd.to_numeric(dfs['FY 2009-10'], errors='coerce')
    dfs['FY 2010-11'] = pd.to_numeric(dfs['FY 2010-11'], errors='coerce')
    dfs['FY 2011-12'] = pd.to_numeric(dfs['FY 2011-12'], errors='coerce')
    dfs['FY 2012-13'] = pd.to_numeric(dfs['FY 2012-13'], errors='coerce')
    dfs['FY 2013-14'] = pd.to_numeric(dfs['FY 2013-14'], errors='coerce')
    dfs['FY 2014-15'] = pd.to_numeric(dfs['FY 2014-15'], errors='coerce')
    st.area_chart(dfs)
    
with chart_2:
    felon = pd.read_csv("data/felon.csv")
    felon.rename(columns={'Number':'FY13-14','Number.1':'FY14-15'},inplace=True)
    felon['FY13-14'] = pd.to_numeric(felon['FY13-14'], errors='coerce')
    felon['FY14-15'] = pd.to_numeric(felon['FY14-15'], errors='coerce')
    ax = plt.gca()
    felon.plot(kind='bar',x='Type of Conviction',y='FY13-14',ax=ax)
    felon.plot(kind='bar',x='Type of Conviction',y='FY14-15', color='red', ax=ax)
    st.line_chart(felon,width=500)
    
#************************************* Form Section ****************************************
       
st.markdown("<hr/>", unsafe_allow_html=True)
st.subheader("Get in Touch")
form = st.form(key='my_form')
form.text_input(label='Name')
form.text_input(label='Email')
form.text_input(label='Comments/Feedback')
submit = submit_button = form.form_submit_button(label='Submit')
if submit:
    st.write(f'We appreciate your time')




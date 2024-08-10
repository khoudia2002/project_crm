# Import des librairies 
import pandas as pd 
import streamlit as st
from tools import * 
from csv import *
import plotly.express as px
import matplotlib as plt
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(
        page_title="Analyse des données du CRM",
        page_icon="img/logo_sales.png",
        layout="wide",
        initial_sidebar_state="expanded",)

#import du fichier account
account_df = file_load_csv("./datasets/accounts.csv")

acc_df_clean=clean_acc_data(account_df)


#import du fichier sales pipeline
sales_pipeline_df = file_load_csv("./datasets/sales_pipeline.csv")
sp_df_clean=clean_sp_data(sales_pipeline_df)
sp_time_clean=clean_sp_time(sales_pipeline_df)

#import du fichier products
products_df = file_load_csv("./datasets/sales_products.csv")
#import de sales_teams 
sales_teams_df = file_load_csv("./datasets/sales_teams.csv")
#Ouvrir les fichier CSV
account_df = pd.read_csv('./datasets/accounts.csv') # Afficher le DataFrame
sales_pipeline_df = pd.read_csv('./datasets/sales_pipeline.csv') 
products_df = pd.read_csv('./datasets/products.csv') 
sales_teams_df = pd.read_csv('./datasets/sales_teams.csv') 

# le monbres total de accounts
total_accounts=acc_df_clean.account.nunique()

# le nombre total de produits 
total_product=products_df['product'].nunique()
# le nombres total de pays
total_countries=acc_df_clean.office_location.nunique()
# le nombres total de secteur
total_sector=acc_df_clean.sector.nunique()
# Le nombre total d’agents
total_agent=sales_teams_df.sales_agent.nunique()






##################################################################################################################
#MISE EN PAGE

st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

st.sidebar.title("Navigation")

pages = ["Acceuil","Comprehension du profil des clients ", "Évaluation de la performance des équipes de vente", "Analyse du cycle de vente"]

#page = st.sidebar.radio("Aller vers la page :", pages)


page = st.sidebar.selectbox(
    'Aller sur la page',
    pages
)
st.sidebar.title("Filtrer les données")
if page == pages[0] :
    col1,col2=st.columns([1,3])
    col1.image("img/logo_sales.png",width=120)
    #col2.title("Analyse des données du CRM")
    with col2:
        header_html = "<h3 style='color: #6600ff; font-family: Arial, sans-serif; font-size: 48px;'>Analyse des données du CRM</h3>"

        st.markdown(header_html, unsafe_allow_html=True)

    
    st.header("Principaux KPIs")

    col1, col2, col3, col4 ,col5= st.columns(5)

    col1.metric(label=" Clients", value=total_accounts)
    col2.metric(label=" Produits", value=total_product)
    col3.metric(label=" Pays", value=total_countries)
    col4.metric(label="Agent commerciaux", value=total_agent)
    col5.metric(label="Sector", value=total_sector)
     
    style_metric_cards()
    #3.	Le produit le plus rentable
    col1,col2=st.columns(2)
    col1.subheader("Rentabilité des produits ")
    col1.bar_chart(sales_pipeline_df[sales_pipeline_df['deal_stage']=='Won'].groupby('product')['close_value'].sum().sort_values(ascending=False),x_label="produit",y_label="Valeur du deal",color='#77B5FE')
    
   
    #	Le produit le plus vendus
    #Le produit qui a  le plus de deal_stage=Won
    col2.subheader("Vente des produits ")
    col2.bar_chart(sales_pipeline_df[sales_pipeline_df['deal_stage']=='Won']['product'].value_counts().sort_values(ascending=False),x_label="produit",y_label="Nombre de deals gagnés",color='#D473D4')
    col1,col2=st.columns(2)
    with col1:

     #client qui achètent le plus
        top_clients_df = sp_df_clean[sp_df_clean['deal_stage'] == 'Won']['account'].value_counts().head(5).reset_index()

        # Renommer les colonnes
        top_clients_df.columns = ['Client', 'Nombre de transactions']

        # Afficher le DataFrame avec les nouveaux titres de colonnes
        st.subheader("Top 5 meilleurs clients")
        st.dataframe(top_clients_df, width=300)
        
    with col2:
        st.subheader(" Classement des secteurs les plus prolifique")
        

        #Classez les secteurs selon les revenues qu'ils générents
        data=acc_df_clean['revenue'].groupby(acc_df_clean['sector']).sum().sort_values(ascending=False)
        #st.dataframe(data)
        st.bar_chart(data,x_label="secteur", y_label="chiffre d'affaires")

   



elif page == pages[1] : 
    col1,col2=st.columns([1,3])
    col1.image("img/logo_sales.png",width=120)
    with col2:
        header_html = "<h3 style='color: #6600ff; font-family: Arial, sans-serif; font-size: 48px;'>Analyse des données du CRM</h3>"

        st.markdown(header_html, unsafe_allow_html=True)

    
    st.header("Comprehension du profil des clients",divider=True)
    
   
   
    
   #Déterminez les clients avec les chiffres d’affaires les plus élevé Top 10
#accounts.head()

    col1,col2=st.columns(2)
    col1.subheader("Top 10 des clients avec les chiffres d'affaires les plus élevés")
    col2.subheader("Proportion des clients par secteur")


    col1,col2=st.columns(2)
    client_by_sector=acc_df_clean['account'].groupby(acc_df_clean['sector']).count().reset_index()
    #Déterminez les clients avec les chiffres d’affaires les plus élevé Top 10
    col1.bar_chart(acc_df_clean[['account','revenue']].sort_values(by="revenue", ascending=False).head(10).set_index('account'), x_label="clients", y_label="chiffre d'affaires")
    
    with col2:
    #client par secteur
       
        fig = px.pie(client_by_sector, values="account", names="sector", hole=0.5)
        
        st.plotly_chart(fig, use_container_width=True)
   
    #Classer les clients par pays 

    #	Classez les clients par secteur aux USA qui est  leader du marché

    col1,col2=st.columns(2)
    with col1:

        st.subheader(" Classement des clients par pays ")
        acc_df_clean['account'].groupby(acc_df_clean['office_location']).count()
        acc_df_clean['location_grouped'] = acc_df_clean['office_location'].apply(lambda x: x if x == 'United States' else 'Autre')
        data=acc_df_clean['account'].groupby(acc_df_clean['location_grouped']).count().reset_index()
        fig = px.pie(data, values='account', names='location_grouped', hole=0.5)
        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
       
       st.subheader("Propotion de client par secteur aux USA ")
       sector_data=acc_df_clean[acc_df_clean['office_location']=='United States']['sector'].value_counts().reset_index()
       sector_data.columns = ['sector', 'count']
       fig = px.pie(sector_data, values='count', names='sector', hole=0.5)
        
       st.plotly_chart(fig, use_container_width=True)
   
    #	Donnez des intervalle d’années pour voir l’évolution des secteurs où il y’a plus de création d’entreprise
    # interval=range(1978,2019,10)
    # acc_df_clean['year_established_interval'] = pd.cut(acc_df_clean['year_established'], bins=interval)
    # evolution = acc_df_clean.groupby(['year_established_interval', 'sector'])['account'].count().reset_index()
    # evolution.pivot(index='year_established_interval', columns='sector', values='account')
    # st.bar_chart(evolution,x_label="années",y_label="nombres d'entreprise")


elif page==pages[2]:
    col1,col2=st.columns([1,3])
    col1.image("img/logo_sales.png",width=120)
    with col2:
        header_html = "<h3 style='color: #6600ff; font-family: Arial, sans-serif; font-size: 48px;'>Analyse des données du CRM</h3>"

        st.markdown(header_html, unsafe_allow_html=True)

    
    st.header("Evaluation de la performance des équipe de vente",divider=True)

     #Faire les metrics pour les agents en fonction des deals 
    total_agent_won= sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Won']['sales_agent'].nunique()
    total_agent_lost= sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Lost']['sales_agent'].nunique()
    total_agent_engaging= sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Engaging']['sales_agent'].nunique()
    total_agent_prospecting= sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Prospecting']['sales_agent'].nunique()

    #schéma du cycle de vente 
    col1, col2, col3, col4 ,col5= st.columns(5)

    col1.metric(label="Total des agents", value=total_agent)
    col2.metric(label="Agents Deals gagnés ", value=total_agent_won)
    col3.metric(label="Agents Deals perdu", value=total_agent_lost)
    col4.metric(label="Agents en cours de deals ", value=total_agent_engaging)
    col5.metric(label="Agents en propection", value=total_agent_prospecting)
    style_metric_cards()

    #4. Le nombre de sales_agent par regional_office
    col1,col2=st.columns(2)
    
    with col1:
        data=sales_teams_df['sales_agent'].groupby(sales_teams_df['regional_office']).count().reset_index()
        
        fig = px.pie(data, values='sales_agent', names='regional_office', hole=0.5)
                
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Classement des employés qui effectue les deal le plus rapidement")
        sp_time_clean['close_date'] = pd.to_datetime(sp_time_clean['close_date'])
        sp_time_clean['engage_date'] = pd.to_datetime(sp_time_clean['engage_date'])
        
        # Suppression des lignes avec des dates manquantes
        sp_time_clean = sp_time_clean.dropna(subset=['close_date', 'engage_date'])
        
        # Calcul de la durée du deal
        sp_time_clean['deal_duration'] = sp_time_clean['close_date'] - sp_time_clean['engage_date']
        
        # Filtrer les données par 'deal_stage', puis grouper par 'sales_agent' et calculer la durée moyenne des deals
        top5_slower = sp_time_clean[sp_time_clean['deal_stage'] == 'Won'].groupby('sales_agent')['deal_duration'].mean().sort_values(ascending=False).head(5)
        top5_slower_df = top5_slower.reset_index()
        st.line_chart(data=top5_slower_df, x='sales_agent', y='deal_duration')
        # Affichage du graphique
        

    col1,col2=st.columns(2)
    
    with col1:
         #5.	Les agents qui apporte les plus grand  revenus
        st.subheader('Top 5 des agents qui apportent les plus grands revenus')
        data=sp_df_clean[sp_df_clean['deal_stage']=='Won'].groupby('sales_agent')['close_value'].sum().sort_values(ascending=False).head(5)
        data=data.reset_index()
        data.columns = ['Agents', 'Revenus apportés']

        st.dataframe(data,width=400)
        
    with col2:
        #5.	Les agents qui apporte les plus petits  revenus
        st.subheader('Top 5 des agents qui apportent les plus petits revenus')
        data=sp_df_clean[sp_df_clean['deal_stage']=='Won'].groupby('sales_agent')['close_value'].sum().sort_values(ascending=True).head(5)
        data=data.reset_index()
        data.columns = ['Agents', 'Revenus apportés']

        st.dataframe(data,width=400)

    col1,col2=st.columns(2)
    with col1:
        #Les 5 agents qui ont gagné de deal
        st.subheader('Top 5 des agents qui ont gagnés le plus de deals')
        data=sp_df_clean[sp_df_clean['deal_stage']=='Won'].groupby('sales_agent')['deal_stage'].count().sort_values(ascending=False).head(5)
        data=data.reset_index()
        data.columns = ['Agents', 'Nombre de deals gagnés']

        st.dataframe(data,width=400)


    with col2:
        st.subheader('Top 5 des agents qui ont perdus le plus de deals')
        data=sp_df_clean[sp_df_clean['deal_stage']=='Lost'].groupby('sales_agent')['deal_stage'].count().sort_values(ascending=False).head(5)
        data=data.reset_index()
        data.columns = ['Agents', 'Nombre de deals perdus']

        st.dataframe(data,width=400)




elif page==pages[3]:

    col1,col2=st.columns([1,3])
    col1.image("img/logo_sales.png",width=120)
    with col2:
        header_html = "<h3 style='color: #6600ff; font-family: Arial, sans-serif; font-size: 48px;'>Analyse des données du CRM</h3>"

        st.markdown(header_html, unsafe_allow_html=True)

    
    st.header("Analyse du cycle de vente",divider=True)

    #Faire les metrics pour les deals 
    
    total_deals = sales_pipeline_df.shape[0]
    won_deals = sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Won']['opportunity_id'].count()
    
    lost_deals = sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Lost']['opportunity_id'].count() 
    
    engaging_deals = sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Engaging']['opportunity_id'].count()
    
    prospecting_deals = sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Prospecting']['opportunity_id'].count()
    

    

    #schéma du cycle de vente 
    col1, col2, col3, col4 ,col5= st.columns(5)

    col1.metric(label=" Nombre total de deals", value=total_deals)
    col2.metric(label=" Deals gagnés", value=won_deals)
    col3.metric(label=" Deals perdus", value=lost_deals)
    col4.metric(label="Deals en cours", value=engaging_deals)
    col5.metric(label="Prospection de deals", value=prospecting_deals)
    style_metric_cards()
     
    
    
    col1,col2=st.columns(2)
    col1.image("img/cycle.png",width=300)

    with col2:

        sales_pipeline_df['close_date'] = pd.to_datetime(sales_pipeline_df['close_date'])
        sales_pipeline_df['engage_date'] = pd.to_datetime(sales_pipeline_df['engage_date'])
        sales_pipeline_df['deal_duration']=sales_pipeline_df['close_date']-sales_pipeline_df['engage_date']
        sold_faster=sales_pipeline_df[sales_pipeline_df['deal_stage']=='Won'].groupby('product')['deal_duration'].mean().sort_values(ascending=True).reset_index()
        st.line_chart(sold_faster, x='product',y='deal_duration')
        #st.image("img/vitesse_de_vente_produits.png",width=800)


   

    #16.	Calculer la durée moyenne du cycle de vente complet, depuis la phase de prospection jusqu'à la clôture (engage_date - closed_date).
# La durée moyenne pour gagner un deal


    # sales_pipeline_df['close_date'] = pd.to_datetime(sales_pipeline_df['close_date'])
    # sales_pipeline_df['engage_date'] = pd.to_datetime(sales_pipeline_df['engage_date'])
    # sales_pipeline_df['deal_duration']=sales_pipeline_df['close_date']-sales_pipeline_df['engage_date']
    # sales_pipeline_df['deal_duration'].mean()
    # wintime=sales_pipeline_df[sales_pipeline_df['deal_stage']=='Won']['deal_duration'].mean()
    # st.write(f"Durée moyenne des deals gagnés : {wintime}")
  
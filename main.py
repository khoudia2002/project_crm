# Import des librairies 
import pandas as pd 
import streamlit as st
from tools import * 
from csv import *
import plotly.express as px
import matplotlib as plt
from streamlit_extras.metric_cards import style_metric_cards
import altair as alt
from streamlit_extras.chart_container import chart_container

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

pages = ["Accueil","Comprehension du profil des clients ", "Évaluation de la performance des équipes de vente", "Analyse du cycle de vente et des produits"]

page = st.sidebar.radio("Aller vers la page :", pages)


# page = st.sidebar.selectbox(
#     'Aller sur la page',
#     pages
# )
# st.sidebar.title("Filtrer les données")
if page == pages[0] :
    col1,col2=st.columns([1,3])
    col1.image("img/logo_sales.png",width=120)
    #col2.title("Analyse des données du CRM")
    with col2:
        header_html = "<h3 style='color: #6600ff; font-family: Arial, sans-serif; font-size: 48px;'>Analyse des données du CRM</h3>"

        st.markdown(header_html, unsafe_allow_html=True)
# st.sidebar.title("Sommaire")

# pages = ["Contexte du projet", "Exploration des données", "Analyse de données", "Modélisation"]

# page = st.sidebar.radio("Aller vers la page :", pages)

# if page == pages[0] : 

    
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
        st.subheader("  Les secteurs les plus prolifique")
        

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
    col1.subheader("Les 10  clients avec les chiffres d'affaires les plus élevés")
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

    # with col2:
       
    #    st.subheader("Propotion de client par secteur aux USA ")
    #    sector_data=acc_df_clean[acc_df_clean['office_location']=='United States']['sector'].value_counts().reset_index()
    #    sector_data.columns = ['sector', 'count']
    #    fig = px.pie(sector_data, values='count', names='sector', hole=0.5)
    #    st.plotly_chart(fig, use_container_width=True)
   
    	
    bins = range(1978, 2019, 10)
    labels = [f'{start}-{start+4}' for start in bins[:-1]]
    acc_df_clean['year_interval'] = pd.cut(acc_df_clean['year_established'], bins=bins, labels=labels, right=False)
    creation_counts = acc_df_clean['year_interval'].value_counts().sort_index()

    # Convertir les résultats en DataFrame pour Plotly
    creation_counts_df = creation_counts.reset_index()
    creation_counts_df.columns = ['year_interval', 'count']

    # Créer le graphique à barres avec Plotly
    fig = px.bar(creation_counts_df, x='year_interval', y='count',
                color='year_interval',  # Utiliser des couleurs différentes pour chaque intervalle
                title='Nombre de créations d\'entreprises par intervalle d\'années',
                labels={'year_interval': 'Intervalle d\'années', 'count': 'Nombre de créations'},
                color_discrete_sequence=px.colors.qualitative.Plotly)  # Choisir une palette de couleurs

    # Afficher le graphique avec Streamlit
    
    st.plotly_chart(fig)




    # Filtres
    selected_sector = st.sidebar.multiselect(
        "Sélectionner les secteurs",
        options=acc_df_clean['sector'].unique(),
        default=acc_df_clean['sector'].unique()
    )
    
    selected_location = st.sidebar.multiselect(
        "Sélectionner les pays",
        options=acc_df_clean['office_location'].unique(),
        default=acc_df_clean['office_location'].unique()
    )
    
    filtered_acc_df = acc_df_clean[
        (acc_df_clean['sector'].isin(selected_sector)) & 
        (acc_df_clean['office_location'].isin(selected_location))
    ]
    

    col1, col2 = st.columns(2)
    with col1:
        col1.subheader("Les clients selon leur chiffre d'affaires")
        col1.bar_chart(filtered_acc_df[['account', 'revenue']].sort_values(by="revenue", ascending=False).head(10).set_index('account'),color="#6621db")

    with col2: 
        col2.subheader("Proportion des clients selon les secteur")
        client_by_sector = filtered_acc_df['account'].groupby(filtered_acc_df['sector']).count().reset_index()
        fig = px.pie(client_by_sector, values="account", names="sector", hole=0.5)
        st.plotly_chart(fig, use_container_width=True)



    


elif page==pages[2]:
    col1,col2=st.columns([1,3])
    col1.image("img/logo_sales.png",width=120)
    with col2:
        header_html = "<h3 style='color: #6600ff; font-family: Arial, sans-serif; font-size: 48px;'>Analyse des données du CRM</h3>"
        st.markdown(header_html, unsafe_allow_html=True)

    
    st.header("Evaluation de la performance des équipes de vente",divider=True)

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
        st.subheader("Classement des agents par region")
        data=sales_teams_df['sales_agent'].groupby(sales_teams_df['regional_office']).count().reset_index()
        
        fig = px.pie(data, values='sales_agent', names='regional_office', hole=0.5)
                
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        
        # Afficher le sous-titre
        st.subheader("Classement des employés qui effectue les deals le plus rapidement")

        # Conversion des colonnes de dates en datetime
        sp_time_clean['close_date'] = pd.to_datetime(sp_time_clean['close_date'])
        sp_time_clean['engage_date'] = pd.to_datetime(sp_time_clean['engage_date'])

        # Suppression des lignes avec des dates manquantes
        sp_time_clean = sp_time_clean.dropna(subset=['close_date', 'engage_date'])

        # Calcul de la durée du deal
        sp_time_clean['deal_duration'] = sp_time_clean['close_date'] - sp_time_clean['engage_date']

        # Conversion de la durée en nombre de jours
        sp_time_clean['deal_duration_days'] = sp_time_clean['deal_duration'].dt.days

        # Filtrer les données par 'deal_stage', puis grouper par 'sales_agent' et calculer la durée moyenne des deals
        top5_slower = sp_time_clean[sp_time_clean['deal_stage'] == 'Won'].groupby('sales_agent')['deal_duration_days'].mean().sort_values(ascending=False).head(20)
        top5_slower_df = top5_slower.reset_index()

        # Création du line chart avec Streamlit
        st.line_chart(data=top5_slower_df.set_index('sales_agent')['deal_duration_days'])

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

    # Filtres
    selected_agent = st.sidebar.multiselect(
        "Sélectionner les agents",
        options=sales_teams_df['sales_agent'].unique(),
        default=sales_teams_df['sales_agent'].unique()
    )
    
    selected_region = st.sidebar.multiselect(
        "Sélectionner les régions",
        options=sales_teams_df['regional_office'].unique(),
        default=sales_teams_df['regional_office'].unique()
    )
    
    filtered_sales_df = sales_pipeline_df[
        (sales_pipeline_df['sales_agent'].isin(selected_agent)) & 
        (sales_teams_df['regional_office'].isin(selected_region))
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(" les agents selon les régions")
        data = sales_teams_df[sales_teams_df['sales_agent'].isin(selected_agent)].groupby('regional_office')['sales_agent'].count().reset_index()
        fig = px.pie(data, values='sales_agent', names='regional_office', hole=0.5)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Les agents selon leur durées de deals")
        sp_time_clean = sp_time_clean[sp_time_clean['sales_agent'].isin(selected_agent)]
        top5_slower = sp_time_clean[sp_time_clean['deal_stage'] == 'Won'].groupby('sales_agent')['deal_duration_days'].mean().sort_values(ascending=False).head(20)
        
        chart_data = top5_slower.reset_index()

        with chart_container(chart_data):
            st.area_chart(chart_data.set_index('sales_agent'))


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
    # col1, col2, col3, col4 ,col5= st.columns(5)

    # col1.metric(label=" Nombre total de deals", value=total_deals)
    # col2.metric(label=" Deals gagnés", value=won_deals)
    # col3.metric(label=" Deals perdus", value=lost_deals)
    # col4.metric(label="Deals en cours", value=engaging_deals)
    # col5.metric(label="Prospection de deals", value=prospecting_deals)
    # style_metric_cards()
    # import streamlit as st
    
    col1, col2, col3, col4 ,col5= st.columns(5)
    with col1: 
        wch_colour_box = (65, 105, 225)
        wch_colour_font = (0,0,0)
        fontsize = 18
        valign = "left"
        iconname = "fas fa-asterisk"
        sline = "DEALS"
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
        i = total_deals

        htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                    {wch_colour_box[1]}, 
                                                    {wch_colour_box[2]}, 0.75); 
                                color: rgb({wch_colour_font[0]}, 
                                        {wch_colour_font[1]}, 
                                        {wch_colour_font[2]}, 0.75); 
                                font-size: {fontsize}px; 
                                border-radius: 7px; 
                                padding-left: 12px; 
                                padding-top: 18px; 
                                padding-bottom: 18px; 
                                line-height:25px;'>
                                <i class='{iconname} fa-xs'></i> {i}
                                </style><BR><span style='font-size: 14px; 
                                margin-top: 0;'>{sline}</style></span></p>"""

        st.markdown(lnk + htmlstr, unsafe_allow_html=True)
        with col2:
            wch_colour_box = (230, 230, 250)
            wch_colour_font = (0,0,0)
            fontsize = 18
            valign = "left"
            iconname = "fas fa-asterisk"
            sline = "DEALS GAGNES"
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
            i = won_deals

            htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                        {wch_colour_box[1]}, 
                                                        {wch_colour_box[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: {fontsize}px; 
                                    border-radius: 7px; 
                                    padding-left: 12px; 
                                    padding-top: 18px; 
                                    padding-bottom: 18px; 
                                    line-height:25px;'>
                                    <i class='{iconname} fa-xs'></i> {i}
                                    </style><BR><span style='font-size: 14px; 
                                    margin-top: 0;'>{sline}</style></span></p>"""
            st.markdown(lnk + htmlstr, unsafe_allow_html=True)

        with col3:
            wch_colour_box = (173, 216, 230)
            wch_colour_font = (0,0,0)
            fontsize = 18
            valign = "left"
            iconname = "fas fa-asterisk"
            sline = "DEALS PERDUS"
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
            i = lost_deals

            htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                        {wch_colour_box[1]}, 
                                                        {wch_colour_box[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: {fontsize}px; 
                                    border-radius: 7px; 
                                    padding-left: 12px; 
                                    padding-top: 18px; 
                                    padding-bottom: 18px; 
                                    line-height:25px;'>
                                    <i class='{iconname} fa-xs'></i> {i}
                                    </style><BR><span style='font-size: 14px; 
                                    margin-top: 0;'>{sline}</style></span></p>"""
            st.markdown(lnk + htmlstr, unsafe_allow_html=True)

        with col4:
            wch_colour_box = (75, 0, 130)
            wch_colour_font = (0,0,0)
            fontsize = 18
            valign = "left"
            iconname = "fas fa-asterisk"
            sline = "DEALS EN COURS"
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
            i = engaging_deals

            htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                        {wch_colour_box[1]}, 
                                                        {wch_colour_box[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: {fontsize}px; 
                                    border-radius: 7px; 
                                    padding-left: 12px; 
                                    padding-top: 18px; 
                                    padding-bottom: 18px; 
                                    line-height:25px;'>
                                    <i class='{iconname} fa-xs'></i> {i}
                                    </style><BR><span style='font-size: 14px; 
                                    margin-top: 0;'>{sline}</style></span></p>"""
            st.markdown(lnk + htmlstr, unsafe_allow_html=True)


        with col5:
            wch_colour_box = (128, 0, 128)
            wch_colour_font = (0,0,0)
            fontsize = 18
            valign = "left"
            iconname = "fas fa-asterisk"
            sline = "PROSPECTIONS"
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
            i = prospecting_deals

            htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                        {wch_colour_box[1]}, 
                                                        {wch_colour_box[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: {fontsize}px; 
                                    border-radius: 7px; 
                                    padding-left: 12px; 
                                    padding-top: 18px; 
                                    padding-bottom: 18px; 
                                    line-height:25px;'>
                                    <i class='{iconname} fa-xs'></i> {i}
                                    </style><BR><span style='font-size: 14px; 
                                    margin-top: 0;'>{sline}</style></span></p>"""
            st.markdown(lnk + htmlstr, unsafe_allow_html=True)

            
        
    
    col1,col2=st.columns([2,3])
    col1.subheader("Schéma du cycle de vente")
    col1.image("img/cycle.png",width=330)

    with col2:
         # with col1:
        # Conversion des colonnes de dates en datetime
        sales_pipeline_df['close_date'] = pd.to_datetime(sales_pipeline_df['close_date'])
        sales_pipeline_df['engage_date'] = pd.to_datetime(sales_pipeline_df['engage_date'])

            # Calcul de la durée du deal
        sales_pipeline_df['deal_duration'] = sales_pipeline_df['close_date'] - sales_pipeline_df['engage_date']

            # Conversion de la durée en nombre de jours
        sales_pipeline_df['deal_duration_days'] = sales_pipeline_df['deal_duration'].dt.days

            # S'assurer que les produits sont des chaînes de caractères
        sales_pipeline_df['product'] = sales_pipeline_df['product'].astype(str)

            # Filtrer les deals "Won" et calculer la moyenne de la durée du deal par produit
        sold_faster = sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Won'].groupby('product')['deal_duration_days'].mean().sort_values(ascending=True).reset_index()

    #         # Création du line chart avec Altair
    #         chart = alt.Chart(sold_faster).mark_line(point=True).encode(
    #             x='product',
    #             y='deal_duration_days'
    #         ).properties(
    #             title='Durée moyenne de vente des produits'
    #         )
    #         st.altair_chart(chart, use_container_width=True)
        chart_data = sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Won'].groupby('product')['deal_duration_days'].mean().sort_values(ascending=True)

    # Convertir la Series en DataFrame
        chart_data_df = chart_data.reset_index()

        with chart_container(chart_data_df):
            st.write("Durée moyenne de vente des produits")
            st.area_chart(chart_data_df.set_index('product'))
                        




    
     # Assurez-vous que les colonnes de dates sont en format datetime
    sales_pipeline_df['engage_date'] = pd.to_datetime(sales_pipeline_df['engage_date'])
    sales_pipeline_df['close_date'] = pd.to_datetime(sales_pipeline_df['close_date'])

        # Calculer la durée du cycle de vente pour chaque deal
    sales_pipeline_df['cycle_duration'] = (sales_pipeline_df['close_date'] - sales_pipeline_df['engage_date']).dt.days

        # Calculer la durée moyenne du cycle de vente pour tous les deals
     
    average_cycle_duration = sales_pipeline_df['cycle_duration'].mean()

        # Calculer la durée moyenne pour les deals gagnés
    deals_won_df = sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Won']
    average_cycle_duration_won = deals_won_df['cycle_duration'].mean()

        # Calculer la durée moyenne pour les deals perdus
    deals_lost_df = sales_pipeline_df[sales_pipeline_df['deal_stage'] == 'Lost']
    average_cycle_duration_lost = deals_lost_df['cycle_duration'].mean()

        # Afficher les résultats avec Streamlit
    col1, col2, col3 = st.columns(3)

    col1.metric(label="Durée moyenne du cycle de vente", value=f"{average_cycle_duration:.1f} jours")
    col2.metric(label="Durée moyenne des deals gagnés", value=f"{average_cycle_duration_won:.1f} jours")
    col3.metric(label="Durée moyenne des deals perdus", value=f"{average_cycle_duration_lost:.1f} jours")
    style_metric_cards()


        # Filtres
    selected_product = st.sidebar.multiselect(
        "Sélectionner les produits",
        options=sales_pipeline_df['product'].unique(),
        default=sales_pipeline_df['product'].unique()
    )

    selected_deal_stage = st.sidebar.multiselect(
        "Sélectionner les étapes du cycle de vente",
        options=sales_pipeline_df['deal_stage'].unique(),
        default=sales_pipeline_df['deal_stage'].unique()
    )

    filtered_sales_pipeline_df = sales_pipeline_df[
        (sales_pipeline_df['product'].isin(selected_product)) & 
        (sales_pipeline_df['deal_stage'].isin(selected_deal_stage))
    ]

    # Création de deux colonnes pour afficher les graphiques côte à côte
    
    
    
    filtered_sales_pipeline_df['cycle_duration'] = (filtered_sales_pipeline_df['close_date'] - filtered_sales_pipeline_df['engage_date']).dt.days
    average_duration_per_product = filtered_sales_pipeline_df.groupby('product')['cycle_duration'].mean().reset_index()
       
    #PARTIE POUR  LES PRODUITS
    col1,col2=st.columns(2)
    with col1:
        # 1.	Les produits les plus chers 
        st.subheader("Les produits les plus chers ")
        product_price=products_df.sort_values(by='sales_price', ascending=False)
        st.dataframe(product_price)

    with col2:
    # # 2.	Les produits en fonction des séries 
        st.subheader("Les produits en fonction des séries ")
        data=products_df['product'].groupby(products_df['series']).count().reset_index()
        fig = px.pie(data, values='product', names='series', hole=0.5)
        st.plotly_chart(fig, use_container_width=True)




    st.subheader("Durée moyenne de vente des produits")
    fig = alt.Chart(average_duration_per_product).mark_line(point=True).encode(
            x='product',
            y='cycle_duration'
    ).properties(
            title='Average Deal Duration by Product',
            width=600,  # Ajuster la largeur du graphique
            height=400  # Ajuster la hauteur du graphique
    )
    st.altair_chart(fig, use_container_width=True)
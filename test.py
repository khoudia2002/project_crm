import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Analyse des données du CRM",
    page_icon="img/logo_sales.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Chargement des données
@st.cache_data
def load_data():
    # Assurez-vous que les chemins sont corrects
    sales_pipeline_df = pd.read_csv('datasets/sales_pipeline.csv')
    customers_df = pd.read_csv('datasets/accounts.csv')
    return sales_pipeline_df, customers_df

sales_pipeline_df, customers_df = load_data()

# Affichez les colonnes pour vérifier l'existence de 'account_id'
st.write("Colonnes dans le DataFrame customers_df:")
st.write(customers_df.columns)

# Vérifiez si 'account_id' existe avant de l'utiliser
if 'account' in customers_df.columns:
    total_accounts = len(customers_df['account'].unique())
    st.write(f"Nombre total de comptes : {total_accounts}")
else:
    st.write("'account_id' n'existe pas dans customers_df. Veuillez vérifier le nom de la colonne.")



# Calcul des KPIs
total_accounts = len(customers_df['account_id'].unique())
total_product = len(sales_pipeline_df['product'].unique())
total_countries = len(customers_df['country'].unique())
total_agent = len(sales_pipeline_df['agent'].unique())
total_sector = len(customers_df['sector'].unique())

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #f5f5f5; }
        h1, h2, h3, h4, h5, h6 { color: #003366; }
        .stMetric { background-color: #e6f2ff; border-radius: 8px; }
        .sidebar .sidebar-content { background-image: linear-gradient(#f5f5f5, #e0e0e0); }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
pages = ["Accueil", "Compréhension du profil des clients", "Évaluation de la performance des équipes de vente", "Analyse du cycle de vente"]
page = st.sidebar.radio("Aller vers la page :", pages)

# Accueil
if page == pages[0]:
    col1, col2 = st.columns([1, 3])
    col1.image("img/logo_sales.png", width=120)
    with col2:
        st.markdown("<h1>Analyse des données du CRM</h1>", unsafe_allow_html=True)

    st.header("Principaux KPIs")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="Clients", value=total_accounts)
    col2.metric(label="Produits", value=total_product)
    col3.metric(label="Pays", value=total_countries)
    col4.metric(label="Agents commerciaux", value=total_agent)
    col5.metric(label="Secteurs", value=total_sector)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Rentabilité des produits")
        fig1 = px.bar(
            sales_pipeline_df[sales_pipeline_df['deal_stage']=='Won'].groupby('product')['close_value'].sum().sort_values(ascending=False),
            labels={'x': "Produit", 'y': "Valeur du deal"},
            color_discrete_sequence=['#77B5FE']
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Vente des produits")
        fig2 = px.bar(
            sales_pipeline_df[sales_pipeline_df['deal_stage']=='Won']['product'].value_counts().sort_values(ascending=False),
            labels={'x': "Produit", 'y': "Nombre de deals gagnés"},
            color_discrete_sequence=['#D473D4']
        )
        st.plotly_chart(fig2, use_container_width=True)

# Compréhension du profil des clients
elif page == pages[1]:
    st.header("Compréhension du profil des clients")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Répartition des clients par secteur")
        fig3 = px.pie(
            customers_df,
            names='sector',
            title='Secteurs des clients',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader("Répartition des clients par pays")
        fig4 = px.choropleth(
            customers_df,
            locations="country",
            color="sector",
            hover_name="account_name",
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with st.beta_expander("Détails supplémentaires"):
        st.write("Voici des informations plus détaillées sur le profil des clients...")
        st.dataframe(customers_df)

# Évaluation de la performance des équipes de vente
elif page == pages[2]:
    st.header("Évaluation de la performance des équipes de vente")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Performance des agents commerciaux")
        fig5 = px.scatter(
            sales_pipeline_df,
            x="close_value",
            y="agent",
            color="deal_stage",
            size="close_value",
            hover_data=['account_name'],
            title="Performance par agent",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.subheader("Moyenne des deals par agent")
        avg_deals = sales_pipeline_df.groupby('agent')['close_value'].mean().sort_values(ascending=False)
        st.dataframe(avg_deals)

    st.markdown("---")
    
    st.subheader("Répartition des deals par étape")
    fig6 = go.Figure(data=[
        go.Bar(name='Won', x=sales_pipeline_df['agent'], y=sales_pipeline_df[sales_pipeline_df['deal_stage']=='Won']['close_value']),
        go.Bar(name='Lost', x=sales_pipeline_df['agent'], y=sales_pipeline_df[sales_pipeline_df['deal_stage']=='Lost']['close_value'])
    ])
    fig6.update_layout(barmode='stack', title="Répartition des deals par étape")
    st.plotly_chart(fig6, use_container_width=True)

# Analyse du cycle de vente
elif page == pages[3]:
    st.header("Analyse du cycle de vente")

    st.subheader("Durée moyenne des cycles de vente par secteur")
    fig7 = px.box(
        sales_pipeline_df,
        x='sector',
        y='sales_cycle_duration',
        color='sector',
        title="Durée des cycles de vente",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    st.plotly_chart(fig7, use_container_width=True)
    
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Cycle de vente par agent")
        agent_filter = st.selectbox("Sélectionner un agent", options=sales_pipeline_df['agent'].unique())
        agent_df = sales_pipeline_df[sales_pipeline_df['agent'] == agent_filter]
        fig8 = px.histogram(
            agent_df,
            x='sales_cycle_duration',
            nbins=10,
            title=f"Durée du cycle de vente pour {agent_filter}",
            color_discrete_sequence=['#FFA07A']
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        st.subheader("Analyse des tendances")
        trend_df = sales_pipeline_df.groupby('month')['sales_cycle_duration'].mean()
        fig9 = px.line(
            trend_df,
            x=trend_df.index,
            y='sales_cycle_duration',
            title="Tendance de la durée du cycle de vente",
            color_discrete_sequence=['#32CD32']
        )
        st.plotly_chart(fig9, use_container_width=True)

    with st.beta_expander("Exporter les données"):
        st.write("Téléchargez les données analysées au format CSV ou PDF.")
        st.download_button("Télécharger CSV", data=sales_pipeline_df.to_csv().encode('utf-8'), file_name='sales_data.csv', mime='text/csv')
        # Add PDF download functionality as needed

# Fin du code

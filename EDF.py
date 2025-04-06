import streamlit as st
st.set_page_config(layout="wide")
import re

import os
from streamlit_community_navigation_bar import st_navbar
from PIL import Image
from Edfdata import (
    import_excel, import_API, plot_categories, plot_co2, matrice_corr, plot_cmpr,
    plot_boxplot_production, plot_typeenergie, plot_Groupe, plot_evolution_par_pays,
    plot_donut_world_group, plot_donut_france, plot_donut_france_xl
)

from Map import carte
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components



############################################Data et style css pour l'interface contenu et le sidebar######################################################################## 











st.markdown("""
    <style>
    body {
        font-family: 'Serif';
    }
    .stSidebar {
        width: 270px !important;
        background-color: #FFFFFF !important;
    }
    .stSidebar .sidebar-content {
        background-color: #FFFFFF !important;
    }
    div, p, span, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }
    [data-testid="stNavButton"] a {
        color: black !important;
    }
    a, a:visited, a:active, a:hover {
        color: black !important;
        text-decoration: none !important;
    }
    .stApp {
        background-color: #FFFFFF;
    }
    .stTabs [role="tablist"] {
        display: flex;
        gap: 0px;
        background-color: #FFFFFF;
        padding: 10px;
    }
    .stTabs [role="tab"] {
        font-size: 1.8rem !important;
        padding: 0.6rem 1.2rem !important;
        color: white !important;
        border-radius: 5px !important;
        border: none !important;
        transition: all 0.2s ease;
    }
    .stTabs [role="tab"]:hover {
        background-color: #FF6600 !important;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: white !important;
        border: none !important;
    }
    .stTabs [role="tablist"]::after {
        display: none !important;
    }
    .stSidebar div, .stSidebar p, .stSidebar span, .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
        color: white !important;
    }

    /* Style de base pour le conteneur du multiselect */
.stMultiSelect {
    background-color: #0033A0 !important;  /* Bleu EDF pour le conteneur */
    color: white !important;  /* Texte blanc */
    display: inline-block !important;
    border-radius: 5px !important;  /* Arrondir les bords */
    font-size: 1.2rem !important;  /* Taille de la police */
}

/* Style des étiquettes (tags) des années sélectionnées */
.stMultiSelect div[data-baseweb="tag"] {
    background-color: #FF6600 !important;  /* Orange pour les tags */
    color: white !important;  /* Texte blanc */
   
    border: none !important;  /* Supprimer toute bordure */
}

/* Fallback pour cibler directement les spans si nécessaire */
.stMultiSelect div div span {
    background-color: #FF6600 !important;  /* Orange pour les tags */
    color: white !important;  /* Texte blanc */
    
    border: none !important;  /* Supprimer toute bordure */
}






/* Style de base pour le conteneur du selectbox */
.stSelectbox {
    background-color: #0033A0 !important;  /* Bleu EDF pour le conteneur */
    color: white !important;  /* Texte blanc */
    display: inline-block !important;
    border-radius: 5px !important;  /* Arrondir les bords */
    font-size: 1.2rem !important;  /* Taille de la police */
}

/* Style de l'élément sélectionné dans le selectbox */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #FF6600 !important;  /* Orange pour l'élément sélectionné */
    color: white !important;  /* Texte blanc */
    border: none !important;  /* Supprimer toute bordure */
}

/* Fallback pour cibler directement l'élément sélectionné */
.stSelectbox div div span {
    background-color: #FF6600 !important;  /* Orange pour l'élément sélectionné */
    color: white !important;  /* Texte blanc */
    border: none !important;  /* Supprimer toute bordure */
}



/* Changer la couleur de l'élément sélectionné au survol */
.stSelectbox div[data-baseweb="select"] > div:hover {
    background-color: #E65C00 !important;  /* Orange plus foncé au survol */
    color: white !important;
}

/* Fallback pour le survol */
.stSelectbox div div span:hover {
    background-color: #E65C00 !important;  /* Orange plus foncé au survol */
    color: white !important;
}

        
    </style>
""", unsafe_allow_html=True)


# Mapping des emojis
sector_emojis = {
    "Wind": "🌬️",
    "Hydraulic": "💧",
    "Nuclear": "⚛️",
    "Gas": "🔥",
    "Solar": "☀️",
    "Coal": "🪨",
    "Biomass": "🌿",
    "Fioul": "🛢️",
    "Geothermal": "🌋",
    "Marine energy": "🌊",
    "Various": "📦",
    "Other Renewable Energies": "♻️"
}

# Mapping des emojis
souscategories = {
    "Wind": "🌬️",
    "Hydraulique": "💧",
    "Nucléaire": "⚛️",
    "Gaz": "🔥",
    "Solar": "☀️",
    "Charbon": "🪨",
    "Biomass": "🌿",
     "CO2": "🌍💨",
    "Fioul": "🛢️",
    "Geothermal": "🌋",
    "Marine energy": "🌊",
    "Various": "📦",
    "Autres Renouvelables": "♻️"
}


energy_emojis = {
    "Electric": "⚡",
    "Heat": "🔥",
}


# Style EDF compact et professionnel
styles = {
    "nav": {
        "background-color": "#FFFFFF", 
        "padding": "0.5rem 0",
        "position": "fixed",
        "top": "0",
        "width": "100%",
        "z-index": "1000"
    },
    "div": {
        "max-width": "fit-content",
        "margin": "0 auto",
        "display": "flex",
        "gap": "0"  # Supprime l'espace entre les boutons
    },
    "a": {
        "color": "black !important",  
        "font-weight": "800",  # Poids du texte
        "font-size": "0.9rem",
        "padding": "0.7rem 1.2rem",
        "margin": "0",
        "border-radius": "0",
        "transition": "all 0.2s ease",
        "text-decoration": "none"
    },
    "hover": {
        "color": "#FF6600"  # Texte devient orange lors du survol
    },
    "active": {
        "color": "black",  # Change la couleur du texte en orange quand l'onglet est sélectionné
        "font-weight": "800"  # Augmente le poids du texte sélectionné
    }
    
}



# Barre de navigation
page = st_navbar(
    ["ANALYSE EXCEL", "DONNÉES API"],
    selected="ANALYSE EXCEL",
    styles=styles
)

logo_image = Image.open("imges/EDF.png")
logo_resized = logo_image.resize((120, 120))

with st.sidebar:
    col1, col2 = st.columns([3, 3])
    col1.image(logo_resized)


# Compensation pour la navbar fixe
st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

edf = import_excel()






################################################################### Page Analyse Excel ################################################################################################
# Contenu des pages
if page == "ANALYSE EXCEL":
    
     
    years = edf['Année'].unique()
    ## 5 année par defaut 
    default_years = years[:5]
    selected_years = st.sidebar.multiselect(
    "Sélectionner les années",  # Titre de la sélection
    options=years.astype(int),  # Liste des options (années disponibles)
    default=default_years  
)
    latest_year = edf['Année'].max()
    precendante_year = latest_year - 1

# Filtrer le DataFrame pour cette année uniquement
    edf_latest = edf[edf['Année'] == latest_year]
    edf_precedante = edf[edf['Année'] == precendante_year]
    
  

    # Par catégorie
    # fonction pour calculer la producution de chaque type d'energie en valaueur relatice en pourcentage 
    def compute_delta(cat_list):
     val_latest = edf_latest[edf_latest['Sous catégorie'].isin(cat_list)]['Valeur'].sum()
     val_prev = edf_precedante[edf_precedante['Sous catégorie'].isin(cat_list)]['Valeur'].sum()
     delta = val_latest - val_prev
     pct = (delta / val_prev) * 100 if val_prev != 0 else 0
     return val_latest, pct
    

    fossiles = ['Fioul', 'Gaz', 'Charbon']
    renouvelables = ['Autres Renouvelables', 'Hydraulique']
    nucleaire=['Nucléaire']
    co2=['CO2']
    prod_fossile, pct_fossile = compute_delta(fossiles)
    prod_renouv, pct_renouv = compute_delta(renouvelables)
    prod_nucleaire, pct_nucleaire = compute_delta(nucleaire)
    prod_co2,pct_co2=compute_delta(co2)

    def format_delta(pct):
     color = 'green' if pct >= 0 else 'red'
     prefix = '+' if pct >= 0 else '–'
     return f"<span style='color:{color}; font-size: 0.8rem;'>({prefix}{abs(pct):.1f}%)</span>"
    
    # colonnes pour les metrics 
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
     st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem;'>⚛️ Nucleaire</div>
        <div style='font-size: 1.1rem; font-weight: bold;'>{prod_nucleaire:,.0f} %</div>
        {format_delta(pct_nucleaire)}
    </div>
    """, unsafe_allow_html=True)

    with col2:
     st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem;'>🔥 Fossile</div>
        <div style='font-size: 1.1rem; font-weight: bold;'>{prod_fossile:,.0f} %</div>
        {format_delta(pct_fossile)}
    </div>
    """, unsafe_allow_html=True)

    with col3:
     st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem;'>💧 Renouvelable</div>
        <div style='font-size: 1.1rem; font-weight: bold;'>{prod_renouv:,.0f} %</div>
        {format_delta(pct_renouv)}
    </div>
    """, unsafe_allow_html=True)

    with col4:
     st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem;'>🌍💨 CO₂</div>
        <div style='font-size: 1.1rem; font-weight: bold;'>{prod_co2:,.0f} g/kWh</div>
        {format_delta(pct_co2)}
    </div>
    """, unsafe_allow_html=True)
    # sous onglets 


    
    tabs = st.tabs(["Data", "Graphiques"])
    
    edf_filtered = edf[edf['Année'].isin(selected_years)]
    edf_filtered['Année'] = edf_filtered['Année'].astype(int)
    graph_type = st.sidebar.selectbox("Choisissez le type de graphique", ["Production", "Boxplot"])
    annees_dispo = sorted(edf["Année"].unique().astype(int).tolist())
    # selecteur année du donut 
    selected_year_donut = st.sidebar.selectbox("Donut Year", options=annees_dispo, index=len(annees_dispo)-1)
    
    with tabs[0]:  # Onglet "Data"
        # Importer et afficher le tableau des données
        edf = import_excel()
        edf['Sous catégorie'] = edf['Sous catégorie'].map(lambda x: f"{souscategories.get(x, '')} {x}")
          # Affichage du tableau data interactive 
        st.dataframe(edf) 
        
        
    with tabs[1]:  # Onglet "Gra^hiques"
        edf = import_excel()


        if graph_type == "Production":
         fig_categories = plot_categories(edf_filtered)
         st.plotly_chart(fig_categories)  # Affichage du graphique

        

        else:
             fig_boxplot_prod = plot_boxplot_production(edf)
             st.plotly_chart(fig_boxplot_prod)
        

        
        
        fig_co2=plot_co2(edf_filtered)
        fig_cmpr=plot_cmpr(edf_filtered)
        fig_correlation=matrice_corr(edf)
        # Graphique de comparaison de production Fossile,Renouvelable , Nucleaire et émissions CO2
        st.plotly_chart(fig_cmpr)
        
        
        fig_donut_France_xl=plot_donut_france_xl(edf,selected_year_donut)
        col1,col2=st.columns(2)
        with col1:
         # Graphique des émissions CO2
         st.plotly_chart(fig_co2)
        with col2 :
          # Graphiques de Donut France
            st.plotly_chart(fig_donut_France_xl)
        st.plotly_chart(fig_correlation)

    
        
        
       

      
        
        
       
#######################################################################################Onglets Données API#####################################################################
       

elif page == "DONNÉES API":
    ## import des données 
    edf_world = import_API()
    
    pays_dispo = edf_world['Spatial perimeter'].unique().tolist() ## pays disponibles 
    annees_dispo = sorted(edf_world["Année"].unique().astype(int).tolist()) # années disponible 
    selected_year = st.sidebar.selectbox("Sélectionnez une année", options=annees_dispo, index=len(annees_dispo)-1)  # Selecteur année 
    total_prod = edf_world[(edf_world["Année"]== selected_year)& (edf_world['Spatial perimeter']=="World")]["Production"].sum() ## Metrics : total production de edf dans le world  
    prod_year_before = edf_world[(edf_world["Année"] == selected_year - 1)& (edf_world['Spatial perimeter']=="World")]["Production"].sum() # production de l'année derniére 
    delta = total_prod - prod_year_before
    elec = edf_world[(edf_world["Année"] == selected_year)& (edf_world['Spatial perimeter']=="World") & (edf_world["Type of energy"] == "Electric")]["Production"].sum() # Production d'électricité dans le world 
    heat = edf_world[(edf_world["Année"] == selected_year) & (edf_world['Spatial perimeter']=="World") & (edf_world["Type of energy"] == "Heat")]["Production"].sum()   # Production de chaleur dans le world 
    # Nombre de pays où EDF a produit de l'énergie pour l'année sélectionnée
    pays_actifs = edf_world[edf_world["Année"] == selected_year]["Spatial perimeter"].unique() # liste des pays ou EDF est actifs selon le selecteur de l'année 
    pays_utiles = [p for p in pays_actifs if p not in ["World", "France"]]  # pays sans world et sans France

    
    nb_pays_actifs = len(pays_utiles)
    top_pays_year = (
    edf_world[
        (edf_world["Année"] == selected_year) &
        (~edf_world["Spatial perimeter"].isin(["France", "World"]))
    ]
    .groupby("Spatial perimeter")["Production"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .iloc[0]
)

    top_pays_name = top_pays_year["Spatial perimeter"] # top pays ou EDF produit le plus 
    top_pays_prod = top_pays_year["Production"]
    col1, col2, col3,col4,col5 = st.columns(5)


    delta_color = "green" if delta >= 0 else "red"
    delta_prefix = "+" if delta >= 0 else "–"


#  colonnes Metrics de producition EDF 
    with col1:
     st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem;'>🌍 Production mondiale</div>
        <div style='font-size: 1.1rem; font-weight: bold;'>{total_prod:,.0f} GWh</div>
        <div style='font-size: 0.8rem; color: {delta_color} !important;'>
            {delta_prefix}{abs(delta):,.0f} GWh
        </div>
    </div>
    """, unsafe_allow_html=True)

    with col2:
     st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem;'>⚡ Part Électricité</div>
        <div style='font-size: 1.1rem; font-weight: bold;'>{(elec / total_prod * 100):.1f} %</div>
    </div>
    """, unsafe_allow_html=True)

    with col3:
     st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem;'>🔥 Part Chaleur</div>
        <div style='font-size: 1.1rem; font-weight: bold;'>{(heat / total_prod * 100):.1f} %</div>
    </div>
    """, unsafe_allow_html=True)

    with col4:
     st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem;'>🏳️ Pays actifs EDF</div>
        <div style='font-size: 1.1rem; font-weight: bold;'>{nb_pays_actifs}</div>
    </div>
    """, unsafe_allow_html=True)

    with col5:
     st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 0.9rem;'>🏆 {top_pays_name}</div>
        <div style='font-size: 1.1rem; font-weight: bold;'>{top_pays_prod:,.0f} GWh</div>
    </div>
    """, unsafe_allow_html=True)


    
    # Top 3 pays actifs hors France et World
    top_total = (
    edf_world[
        (edf_world["Année"] == selected_year) &
        (~edf_world["Spatial perimeter"].isin(["France", "World"]))
    ]
    .groupby("Spatial perimeter")["Production"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .head(3)
)

    
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = 0  # Default to first tab ("Data")
    # Créer les onglets avec st.tabs
    tabs = st.tabs(["Data", "Graphiques","Carte"])
    with tabs[0]:
        st.session_state.active_tab = 0 
        edf_world = import_API()
        edf_world['Sector'] = edf_world['Sector'].map(lambda x: f"{sector_emojis.get(x, '')} {x}")
        edf_world['Type of energy'] = edf_world['Type of energy'].map(lambda x: f"{energy_emojis.get(x, '')} {x}")
        # Apply custom CSS to force black text in the table

        # Display the dataframe
        st.dataframe(edf_world)
    with tabs[1]:
        st.session_state.active_tab = 1
        # Calculer les pays où EDF produit le plus (total électricité + chaleur)
        top_pays = (edf_world[~edf_world["Spatial perimeter"].isin(["World", "France"])].groupby("Spatial perimeter")["Production"].sum()
        .sort_values(ascending=False).head(3).index.tolist())
        latest_year = edf_world['Année'].max()
        
         # +ajout des pays par deut Canda china beligique 
        default_pays = top_pays + ["Canada", "Belgium","People's Republic of China"]
        # selecteurs  pays 
        pays_selection = st.sidebar.multiselect("Choisissez un ou plusieurs pays", options=pays_dispo, default= default_pays)
        secteurs_dispo = edf_world['Sector'].unique().tolist()
        # selecteur sector 
        secteurs_selection = st.sidebar.multiselect("Choisissez les filières énergétiques", options=secteurs_dispo, default=secteurs_dispo)
        type_energie_options = edf_world["Type of energy"].unique().tolist() # Type de l'énergie 
        type_selection = st.sidebar.selectbox("Sélectionnez le type d'énergie", options=type_energie_options) # selecteurs du type de l'énergie 
        fig_energy_type=plot_typeenergie(edf_world,pays_selection,selected_year, secteurs_selection,type_selection)
        # Graphique de production par pays et type d'energie 
        st.plotly_chart(fig_energy_type)
        # donut  world  
        fig_donut_world=plot_donut_world_group(edf_world, selected_year)
        # DOnut France 
        fig_donut_France=plot_donut_france(edf_world, selected_year)
        col1,col2=st.columns(2)
        with col1:
          st.plotly_chart(fig_donut_world)
        with col2:
          st.plotly_chart(fig_donut_France)



        edf_world['Sector'] = edf_world['Sector'].apply(lambda x: re.sub(r'[^\w\s-]', '', str(x)).strip())
        fig_Groupe=plot_Groupe(edf_world, selected_year, pays_selection)
        ## Grpahqqiue de production par pays et type d'energie 
        st.plotly_chart(fig_Groupe)
        
        type_selection_clean = re.sub(r'[^\w\s-]', '', type_selection).strip()
        edf_world['Type of energy'] = edf_world['Type of energy'].apply(lambda x: re.sub(r'[^\w\s-]', '', str(x)).strip())
        fig_tempr = plot_evolution_par_pays(edf_world, pays_selection)
        ## Onglet Carte 
        st.plotly_chart(fig_tempr)
    with tabs[2]:
     st.session_state.active_tab = 2 
     with st.container():
        html_code, prod_par_pays, df_grouped, country_colors = carte(edf_world, selected_year)
        st.markdown(f"### Carte des productions EDF énergétiques - {selected_year}")
        st.components.v1.html(html_code, height=600)  # Reduce height for testing
        
       

       

############################################################ telecharger pdf de l'analyse ####################################################################################
        






import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import re


# fonction ppour importer le fichier Excel France 
@st.cache_data
def import_excel():
    

    edf = pd.read_excel("data/lelec.xlsx", engine="openpyxl",header=2) # header= 2  pour ignorer les deux premiéres lignes 
    # Netoyage de données
    edf = edf.dropna(axis=0, how='all') # Supression de lignes vides 
    edf = edf.dropna(axis=1, how='all') # Supression de colonnes vides 
    edf=edf[~edf['Catégorie'].isin(['Déchets radioactifs'])] # Supprission de lignes avec catégorie = Déchet radioactifs
    edf=edf.drop(columns=['Perimètre juridique','Unité'])  # Supression des colonnes Perimetre juridique et UNité 
    ## edf[edf.duplicated()]  ##  pour voir les lignes duppliquée 
    edf = edf.drop_duplicates() ## suppression  des lignes duppliquées

    edf['Année'] = pd.to_numeric(edf['Année'], errors='coerce').astype('Int64')  # convertir l'anné en entier 

    
    

    return edf

# fonction pour importer le fihcier API world

@st.cache_data
def import_API():
    edf_world = pd.read_excel("data/Edf_world.xlsx", engine="openpyxl")
    # suppression des colonnes en français 
    edf_world = edf_world.drop(columns=["Type d'énergie", "Périmètre juridique", "Périmètre spatial", "Filière", "Méthode de consolidation"])

    return edf_world

# Fonction pour créer une table pivot pour explorer les tendances par sous-catégorie
@st.cache_data
def plot_categories(edf):

   edf_grouped = edf.groupby(['Année', 'Sous catégorie'])['Valeur'].sum().reset_index()
   edf_grouped['Année'].unique().astype(int)
# Création d'un graphique interactif avec Plotly
   fig_categories = px.line(edf_grouped, 
              x="Année", 
              y="Valeur", 
              color="Sous catégorie", 
              title="Évolution des tendances par année et sous-catégorie",
              labels={"Année": "Année", "Valeur": "Valeur", "Sous catégorie": "Sous-catégorie"},
              markers=True)  # Afficher des points pour chaque année

# Personnalisation des étiquettes et des axes
   fig_categories.update_layout(
        xaxis_title="Année",
        yaxis_title="Valeur",
        title_font=dict(size=20, color="black"),
        xaxis=dict(
            type='category',  # Essential
            tickmode='array',
            tickvals=sorted(edf_grouped['Année'].unique()),  # Valeurs exactes
            title_font=dict(size=14, color="blue"),
            tickangle=45  # Meilleure lisibilité
        ),
        yaxis=dict(title_font=dict(size=14, color="blue")),
        legend_title="Sous catégorie",
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
  
   


   
   return fig_categories

# Creation d'un graphique Line CO2 

def plot_co2(edf):
      df_co2 = edf[edf['Sous catégorie'] == 'CO2']  # Filtrer les lignes où la sous-catégorie est 'CO2'
      df_co2_grouped = df_co2.groupby(['Année'])['Valeur'].sum().reset_index()
      df_co2_grouped['Année'].unique().astype(int)

      fig_co2 = px.line(df_co2_grouped, 
              x='Année', 
              y='Valeur', 
              title="Évolution des émissions de CO2 au fil des années",
              labels={"Année": "Année", "Valeur": "Émissions de CO2 (en tonnes)"}, 
              markers=True)  # Ajouter des points pour chaque année

# Personnalisation du graphique (facultatif)
      fig_co2.update_layout(
    title="Évolution des émissions de CO2 au fil des années",  # Titre du graphique
    title_font=dict(size=20, color="black"),  # Titre du graphique en noir
     xaxis=dict(
            type='category',  # Essential
            tickmode='array',
            tickvals=sorted(df_co2_grouped['Année'].unique()),  # Valeurs exactes
            title_font=dict(size=14, color="blue"),
            tickangle=45  # Meilleure lisibilité
        ),
    yaxis=dict(title="Émissions de CO2 (en tonnes)", title_font=dict(size=16, color="blue")),  # Axe Y en bleu
    plot_bgcolor="white",  # Fond du graphique en blanc
    paper_bgcolor="white"  # Fond général du graphique
)

# Afficher le graphique dans Streamlit
      return fig_co2


# graphique du boxplot 
@st.cache_data
def plot_boxplot_production(edf):
    # Filtrer les données pour les sources d'énergie (exclure les émissions de CO2)
    df_filières_prod = edf[edf['Catégorie'] == 'Source d\'énergie d\'électricité fournie']

    # Création  d'un boxplot pour la production d'énergie par filière
    fig_boxplot_prod = px.box(df_filières_prod, 
                              x='Sous catégorie',  # Filières de production
                              y='Valeur',  # valeurs de production d'énergie
                              color='Sous catégorie',  # Couleurs  sous-catégorie
                              title="Distribution de la production d'énergie par filière", 
                              labels={"Sous catégorie": "Filière de production", "Valeur": "Production d'énergie (en MWh)"})
    
    # Personnalisation du graphique
    fig_boxplot_prod.update_layout(
        xaxis_title="Filières de production",  
        yaxis_title="Production d'énergie (en MWh)", 
        plot_bgcolor="white",  
        paper_bgcolor="white"  
    )
    
    return fig_boxplot_prod

@st.cache_data
# Matrice de corrélation 
def matrice_corr(edf):
    df_co2 = edf[edf['Sous catégorie'] == 'CO2']  # Filtrer les lignes où la sous-catégorie est 'CO2'
    df_co2_grouped = df_co2.groupby(['Année'])['Valeur'].sum().reset_index()
    filières = edf['Sous catégorie'].unique().tolist()
    edf_filières = edf[edf['Sous catégorie'].isin(filières)]
    edf_filières_grouped = edf_filières.groupby(['Année', 'Sous catégorie'])['Valeur'].sum().unstack(fill_value=0)
    df_corr = pd.merge(df_co2_grouped, edf_filières_grouped, on='Année')
    df_corr = df_corr.drop(columns=['Année', 'Valeur'])
    correlation_matrix = df_corr.corr()
    custom_brownish_scale = [
    [0.0, 'white'],  # blanc (corrélation ≈ 0)
    [0.25, '#f7e8df'],  # presque blanc
    [0.5, '#eec4b3'],    # rose très clair / beige
    [0.75, '#a65e2e'],  # brun moyen
    [1.0, '#2c1005']     #brun très foncé (forte corrélation négative)
    
    
    
    ]

    fig_correlation = px.imshow(correlation_matrix, 
                text_auto=True,  # Afficher les valeurs dans chaque cellule
                color_continuous_scale=custom_brownish_scale,  # Palette de couleurs
                title="Matrice de corrélation interactive",  # Titre du graphique
                labels=dict(x="Variables", y="Variables"))  # Labels des axes

# Personnalisation 
    fig_correlation.update_layout(
     xaxis_title="Variables",  # Titre pour l'axe X
     yaxis_title="Variables",  # Titre pour l'axe Y
     title_font=dict(size=20, color="black"),  # Titre en noir
     width=1200,  # Largeur du graphique
     height=600,  # Hauteur du graphique
     margin=dict(l=50, r=50, t=50, b=50)  # Marges autour du graphique
)


    return fig_correlation



# graphique de comparaision entre chaque filiéres fossile renouvelable Nuc avec une line CO2 
@st.cache_data
def plot_cmpr(edf):
    # Séparation des données entre filières fossiles et renouvelables
    fossiles = ['Fioul', 'Gaz', 'Charbon']
    renouvelables = ['Autres renouvelables', 'Hydraulique']
    nucleaire=['Nucléaire']
    co2=['CO2']

# Filtage des données pour chaque groupe
    edf_fossiles = edf[edf['Sous catégorie'].isin(fossiles)]
    edf_renouvelables = edf[edf['Sous catégorie'].isin(renouvelables)]
    edf_nucleaire = edf[edf['Sous catégorie'].isin(nucleaire)]
    edf_co2 = edf[edf['Sous catégorie'].isin(co2)]
    prod_fossiles = edf_fossiles.groupby(['Année'])['Valeur'].sum()
    prod_renouvelables = edf_renouvelables.groupby(['Année'])['Valeur'].sum()
    prod_nucleaire=edf_nucleaire.groupby(['Année'])['Valeur'].sum()
    prod_co2=edf_co2.groupby(['Année'])['Valeur'].sum()

# Fusionnage des deux DataFrames pour avoir les deux groupes côte à côte
    df_comparaison = pd.DataFrame({
    'Année': prod_fossiles.index.astype(int),
    'Filières Fossiles': prod_fossiles.values,
    'Filières Renouvelables': prod_renouvelables.values,
    'Filiéres Nucléaire': prod_nucleaire.values,
    'CO2': prod_co2.values
}) 
    # Création du graphique en barres
    df_comparaison.set_index('Année').plot(kind='bar', figsize=(12, 6), color=['yellow', 'skyblue','red','orange'])

  #  # Création d'un graphique combiné (barres pour les filières et émissions CO2
    fig_cmr = go.Figure()

    # Ajout des barres pour les filières
    fig_cmr.add_trace(go.Bar(
        x=df_comparaison['Année'].astype(int),
        y=df_comparaison['Filières Fossiles'],
        name='Filières Fossiles',
        marker_color= '#FF6600'
    ))

    fig_cmr.add_trace(go.Bar(
        x=df_comparaison['Année'].astype(int),
        y=df_comparaison['Filières Renouvelables'],
        name='Filières Renouvelables',
        marker_color='skyblue'
    ))

    fig_cmr.add_trace(go.Bar(
        x=df_comparaison['Année'].unique().astype(int),
        y=df_comparaison['Filiéres Nucléaire'],
        name='Filières Nucléaire',
        marker_color='yellow'
    ))

    # Ajout de la ligne pour les émissions de CO2
    fig_cmr.add_trace(go.Scatter(
        x=df_comparaison['Année'].astype(int),
        y=df_comparaison['CO2'],
        mode='lines+markers',
        name='CO2',
        line=dict(color='black', width=3),  # CO2 en ligne noire
        marker=dict(color='black', size=8)  # Points noirs pour CO2
    ))

    # Personnalisation de la mise en page
    fig_cmr.update_layout(
        title="Comparaison de la production d'électricité fossile vs renouvelable vs CO2 (par année)",
        xaxis_title="Année",
        yaxis_title="Production (en MWh) / Émissions de CO2 (en tonnes)",
        title_font=dict(size=20, color="black"),
        xaxis=dict(tickangle=45),  # Rotation des étiquettes sur l'axe X pour une meilleure lisibilité
        plot_bgcolor="white",  # Fond du graphique blanc
        paper_bgcolor="white",  # Fond général du graphique
        showlegend=True,  # Afficher la légende
        legend_title="Filières",
        margin=dict(l=50, r=50, t=50, b=50),  # Marges pour éviter que les textes se chevauchent
        bargap=0.5,  # Réduit l'espacement entre les barres
        bargroupgap=0  # Réduit l'espacement entre les groupes de barres
    )

    return fig_cmr


# Graphiques Donut de france Fichier Excel France 
@st.cache_data
def plot_donut_france_xl(edf, selected_year_donut):
    fossiles_keywords = ['Charbon', 'Gaz', 'Fioul']
    renouvelables_keywords = [ 'Hydraulique', 'Autre Renouvelables']
    nucleaire_keywords = ['Nucléaire']

    ## fonction pour classifier les filiéres 
    def classify_sector(sector):
        sector = str(sector).lower()
        if any(key.lower() in sector for key in fossiles_keywords):
            return "Fossile"
        elif any(key.lower() in sector for key in renouvelables_keywords):
            return "Renouvelable"
        elif any(key.lower() in sector for key in nucleaire_keywords):
            return "Nucléaire"
        else:
            return "Various"

   
    df_filtered = edf[
        (edf["Année"] == selected_year_donut) &
        (edf["Perimètre spatial"] == "France")  # fichier 1 Excel France
    ].copy()

    df_filtered["Groupe"] = df_filtered["Sous catégorie"].apply(classify_sector)

    df_grouped = df_filtered.groupby("Groupe")["Valeur"].sum().reset_index() 

    if df_grouped.empty:
        st.warning(f"Aucune donnée disponible pour l'année {selected_year_donut}")
        return go.Figure()

    fig_donut_France_xl= px.pie(
        df_grouped,
        names="Groupe",
        values="Valeur",
        hole=0.4,
        title=f"Répartition  de la production en France par groupe ({selected_year_donut})",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_donut_France_xl.update_traces(textinfo="percent+label")

    return fig_donut_France_xl





########################################################################################################################### Onglet 2 API : World ####################################""



# graphique  de visualisations des secteurs filtrabale (pays , année , Sector, Type de l'energy Chaleur ou electrique  )
@st.cache_data
def plot_typeenergie(edf_world,pays_selection,selected_year, secteurs_selection,type_selection):

  
# Filtrage des données pour ce graphique
   df_type_filtered = edf_world[
    (edf_world["Année"] == selected_year) &
    (edf_world["Spatial perimeter"].isin(pays_selection)) &
    (edf_world["Type of energy"] == type_selection)&
    (edf_world["Sector"].isin(secteurs_selection))
]

# Vérification et affichage
   if df_type_filtered.empty:
    st.warning("Aucune donnée disponible pour ce filtre.")
   else:
    fig_energy_type = px.bar(
        df_type_filtered,
        x="Spatial perimeter",
        y="Production",
        color="Sector",
        title=f"Production d'énergie {type_selection} pour l'année {selected_year}",
        labels={"Production": "Production (GWh)", "Spatial perimeter": "Pays"},
        barmode="group"
    )
    
    fig_energy_type.update_layout(  # PUpdate layout 
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_font=dict(size=20),
        xaxis_tickangle=45,
        xaxis_title="Pays",
        yaxis_title="Production (GWh)",
        legend_title_text="Filière",
        margin=dict(l=40, r=40, t=60, b=40),
        bargap=0,  # Réduit l'espacement entre les barres
        bargroupgap=0  # Réduit l'espacement entre les groupes de barres
    )

    return fig_energy_type
   
# graphique pour le type de sector Renouvelable - Fossile Nucléaire, ou Various filtrable selon l'année et les pays 
@st.cache_data
def plot_Groupe(edf_world, selected_year, pays_selection):
    fossiles_keywords = ['Coal', 'Gas', 'Fioul']
    renouvelables_keywords = ['Wind', 'Hydraulic', 'Solar', 'Biomass', 'Geothermal', 'Marine energy', 'Renewable']
    nucleaire_keywords = ['Nuclear']

    def classify_sector(sector):
        sector = str(sector).lower()
        if any(key.lower() in sector for key in fossiles_keywords):
            return "Fossile"
        elif any(key.lower() in sector for key in renouvelables_keywords):
            return "Renouvelable"
        elif any(key.lower() in sector for key in nucleaire_keywords):
            return "Nucléaire"
        else:
            return "Autre"

    # Filtrer les données
    df_filtered = edf_world[
        (edf_world["Année"] == selected_year) &
        (edf_world["Spatial perimeter"].isin(pays_selection))
    ].copy()

    df_filtered["Groupe"] = df_filtered["Sector"].apply(classify_sector)

    # Grouper les données
    df_grouped = df_filtered.groupby(["Spatial perimeter", "Groupe"])["Production"].sum().reset_index()

    # Réorganiser pour barres groupées
    df_pivot = df_grouped.pivot(index="Spatial perimeter", columns="Groupe", values="Production").fillna(0)

    # Créer le graphique
    fig_Groupe = go.Figure()
    for groupe in ["Fossile", "Renouvelable", "Nucléaire"]:
        if groupe in df_pivot.columns:
            fig_Groupe.add_trace(go.Bar(
                x=df_pivot.index,
                y=df_pivot[groupe],
                name=groupe
            ))

    fig_Groupe.update_layout(
        title=f"Production par type d'énergie pour l'année {selected_year}",
        barmode='group',
        xaxis_title="Pays",
        yaxis_title="Production (GWh)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_font=dict(size=20, color="black"),
        bargap=0,  # Réduit l'espacement entre les barres
        bargroupgap=0  # Réduit l'espacement entre les groupes de barres
    )

    return fig_Groupe

# evolution du type de l'energy par année (filtrable par année et le type d'énergie)
@st.cache_data
def plot_evolution_par_pays(edf_world, pays_selection):
    # Nettoyage
    edf_world['Type of energy'] = edf_world['Type of energy'].apply(lambda x: re.sub(r'[^\w\s-]', '', str(x)).strip())
    edf_world['Sector'] = edf_world['Sector'].apply(lambda x: re.sub(r'[^\w\s-]', '', str(x)).strip())
    
    # Filtrage
    df_filtered = edf_world[edf_world["Spatial perimeter"].isin(pays_selection)]

    # 👉 Agréger la production par Année, Type d'énergie et Pays
    df_grouped = df_filtered.groupby(['Année', 'Type of energy', 'Spatial perimeter'])['Production'].sum().reset_index()

    # Fusion type énergie + pays pour une courbe par combinaison
    df_grouped["Pays_Type"] = df_grouped["Spatial perimeter"] + " - " + df_grouped["Type of energy"]
    annees_uniques = sorted(df_grouped["Année"].dropna().unique())


    fig_tempr = px.line(
        df_grouped,
        x="Année",
        
        y="Production",
        color="Pays_Type",
        markers=True,
        title="Évolution de la production par type d'énergie et pays",
        labels={
            "Année": "Année",
            "Production": "Production (GWh)",
            "Pays_Type": "Pays - Type d'énergie"
        },
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    fig_tempr.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_font=dict(size=20),
        xaxis=dict(
            tickangle=45,
            tickmode="array",
            tickvals=annees_uniques,  # Valeurs entières uniquement
            title="Année"
        )
    )


    return fig_tempr



# Graphique pour afficher le type de sector dans un donut World 
@st.cache_data
def plot_donut_world_group(edf_world, selected_year):
    fossiles_keywords = ['Coal', 'Gas', 'Fioul']
    renouvelables_keywords = ['Wind', 'Hydraulic', 'Solar', 'Biomass', 'Geothermal', 'Marine', 'Renewable']
    nucleaire_keywords = ['Nuclear']

    def classify_sector(sector):
        sector = str(sector).lower()
        if any(key.lower() in sector for key in fossiles_keywords):
            return "Fossile"
        elif any(key.lower() in sector for key in renouvelables_keywords):
            return "Renouvelable"
        elif any(key.lower() in sector for key in nucleaire_keywords):
            return "Nucléaire"
        else:
            return "Various"

    # 🔧 On filtre seulement les données de "World"
    df_filtered = edf_world[
        (edf_world["Année"] == selected_year) &
        (edf_world["Spatial perimeter"] == "World")
    ].copy()

    df_filtered["Groupe"] = df_filtered["Sector"].apply(classify_sector)

    df_grouped = df_filtered.groupby("Groupe")["Production"].sum().reset_index()

    if df_grouped.empty:
        st.warning(f"Aucune donnée disponible pour l'année {selected_year}")
        return go.Figure()

    fig_donut_world = px.pie(
        df_grouped,
        names="Groupe", 
        values="Production",
        hole=0.4,
        title=f"Répartition mondiale de la production par groupe ({selected_year})",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_donut_world.update_traces(textinfo="percent+label")

    return fig_donut_world

# Graphique pour afficher le type de sector dans un donut France
@st.cache_data 
def plot_donut_france(edf_world, selected_year):
    fossiles_keywords = ['Coal', 'Gas', 'Fioul']
    renouvelables_keywords = ['Wind', 'Hydraulic', 'Solar', 'Biomass', 'Geothermal', 'Marine', 'Renewable']
    nucleaire_keywords = ['Nuclear']


    def classify_sector(sector):
        sector = str(sector).lower()
        if any(key.lower() in sector for key in fossiles_keywords):
            return "Fossile"
        elif any(key.lower() in sector for key in renouvelables_keywords):
            return "Renouvelable"
        elif any(key.lower() in sector for key in nucleaire_keywords):
            return "Nucléaire"
        else:
            return "Various"

    # 🔧 On filtre seulement les données de France
    df_filtered = edf_world[
        (edf_world["Année"] == selected_year) &
        (edf_world["Spatial perimeter"] == "France")
    ].copy()

    df_filtered["Groupe"] = df_filtered["Sector"].apply(classify_sector)

    df_grouped = df_filtered.groupby("Groupe")["Production"].sum().reset_index()

    if df_grouped.empty:
        st.warning(f"Aucune donnée disponible pour l'année {selected_year}")
        return go.Figure()

    fig_donut_France= px.pie(
        df_grouped,
        names="Groupe",
        values="Production",
        hole=0.4,
        title=f"Répartition  de la production en France par groupe ({selected_year})",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_donut_France.update_traces(textinfo="percent+label")

    return fig_donut_France

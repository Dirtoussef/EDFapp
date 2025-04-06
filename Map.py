import pandas as pd
import requests
import streamlit as st
import pycountry




@st.cache_data
def import_API():
    edf_world = pd.read_excel("data/Edf_world.xlsx", engine="openpyxl")
    edf_world = edf_world.drop(columns=[
        "Type d'énergie", "Périmètre juridique", "Périmètre spatial", 
        "Filière", "Méthode de consolidation"
    ])
    return edf_world

edf_world = import_API()

# selecteur Année 

selected_year = st.selectbox("Choisissez une année", sorted(edf_world["Année"].unique()))


# function pour modifier le nom de la chine parce que ça se detecte pas sur le geojson
def harmonize_country_names(df):
    df["Spatial perimeter"] = df["Spatial perimeter"].replace({
        "People's Republic of China": "China"
    })
    return df



# detection des pays 
def get_iso_code(name):
    manual_mapping = {
        "People's Republic of China": "cn",
        "United States of America": "us",
        "United Kingdom": "gb",
        "South Africa": "za",
        "Germany": "de",
        "Belgium": "be",
        "Brazil": "br",
        "Canada": "ca",
        "Spain": "es",
        "France": "fr",
        "Greece": "gr",
        "India": "in",
        "Israel": "il",
        "Italy": "it",
        "Mexico": "mx",
        "Poland": "pl",
        "Switzerland": "ch",
        "Vietnam": "vn",
        "Netherlands": "nl",
        "Chile": "cl",
        "Laos": "la",
        "Morocco": "ma",
        "United Arab Emirates": "ae",
        "Egypt": "eg",
        "Portugal": "pt",
        "Turkey": "tr",
        "Czech Republic": "cz",
        "Austria": "at",
        "Hungary": "hu",
        "Slovakia": "sk",
        "Norway": "no",
        "Sweden": "se",
        "Finland": "fi",
        "Denmark": "dk",
        "Ireland": "ie",
        "Various countries": None,
        "World": None
    }

    name_lower = name.lower()
    for key, value in manual_mapping.items():
        if key.lower() == name_lower:
            return value
    try:
        return pycountry.countries.search_fuzzy(name)[0].alpha_2.lower()
    except LookupError:
        return None
@st.cache_data  # caching 
def carte(edf_world, selected_year):
    df_annee = edf_world[edf_world["Année"] == selected_year]
    df_annee = df_annee[~df_annee["Spatial perimeter"].isin(["World", "Various countries"])]
    df_annee = harmonize_country_names(df_annee)
    edf_world = harmonize_country_names(edf_world)
    prod_par_pays = df_annee.groupby("Spatial perimeter")["Production"].sum().to_dict()
    
    fossiles_keywords = ['Coal', 'Gas', 'Fioul']
    renouvelables_keywords = ['Wind', 'Hydraulic', 'Solar', 'Biomass', 'Geothermal', 'Marine', 'Renewable']
    nucleaire_keywords = ['Nuclear']

    
    def classify_sector(sector):  # pour classifier le secteurs
        sector = str(sector).lower()
        if any(key.lower() in sector for key in fossiles_keywords):
            return "Fossile"
        elif any(key.lower() in sector for key in renouvelables_keywords):
            return "Renouvelable"
        elif any(key.lower() in sector for key in nucleaire_keywords):
            return "Nucléaire"
        else:
            return "various"

    # Filtrer les données
    df_filtered = edf_world[
        (edf_world["Année"] == selected_year)
    ].copy()





    df_filtered["Groupe"] = df_filtered["Sector"].apply(classify_sector)

    df_grouped_raw = df_filtered.groupby(["Spatial perimeter", "Groupe"])["Production"].sum() #  sommede productiongrouper par pays et par secteurs
    # injection dan sle dictionnaire 
    grouped_data = {}
    for (country, group), value in df_grouped_raw.items():
        if country not in grouped_data:
            grouped_data[country] = {}
        grouped_data[country][group] = float(value)  # Convertir en float pour JavaScript

    edf_countries = list(prod_par_pays.keys())

    
    


    edf_countries = list(prod_par_pays.keys())

    palette = [
        "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
        "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ab",
    ]
    country_colors = {country: palette[i % len(palette)] for i, country in enumerate(edf_countries)}

    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        countries_geojson = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de chargement GeoJSON : {e}")
        st.stop()

    iso_map = {country: get_iso_code(country) for country in edf_countries}

    html_code = f"""
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

    <div id="map" style="width: 100vw; height: 90vh; margin: 0;"></div>

    <script>
        const emojiMap = {{
            "Renouvelable": "🌿",
            "Fossile": "🛢️",
            "Nucléaire": "⚛️",
            "various": "🌐"
        }};

        var map = L.map('map').setView([25, 0], 2);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap'
        }}).addTo(map);

        var countriesData = {countries_geojson};
        var productionData = {prod_par_pays};
        var groupedData = {grouped_data};
        var countryColors = {country_colors};
        var isoMap = {iso_map};

        function getColor(name) {{
            return countryColors[name] || "#e0e0e0";
        }}

        function style(feature) {{
            var name = feature.properties.name;
            return {{
                fillColor: getColor(name),
                weight: 1,
                opacity: 1,
                color: '#ffffff',
                fillOpacity: countryColors[name] ? 0.7 : 0.1
            }};
        }}

        function highlightFeature(e) {{
            var layer = e.target;
            var name = layer.feature.properties.name;
            var totalProd = productionData[name];
            var groupData = groupedData[name];
            var isoCode = isoMap[name] || name.toLowerCase();

            if (countryColors[name] && totalProd) {{
                layer.setStyle({{
                    weight: 2,
                    color: '#ffffff',
                    fillOpacity: 0.9
                }});

                var popupContent = "<div style='border-radius:10px; padding:10px; background:#fff; box-shadow:0 0 10px rgba(0,0,0,0.2); text-align:center;'>"
                    + "<img src='https://flagcdn.com/48x36/" + isoCode + ".png' style='margin-bottom:5px;'><br>"
                    + "<strong>Pays :</strong> " + name + "<br>"
                    + "<strong>Production totale :</strong> " + totalProd.toFixed(2) + " GWh<br>"
                    + "<strong>Répartition :</strong><br>";


                if (groupData) {{
                    for (var group in groupData) {{
                        if (groupData[group] > 0) {{
                            popupContent += (emojiMap[group] || "") + " " + group + " : " + groupData[group].toFixed(2) + " GWh<br>";
                        }}
                    }}
                }} else {{
                    popupContent += "Aucune donnée détaillée disponible";
                }}

                popupContent += "</div>";

                layer.bindPopup(popupContent).openPopup();
            }}
        }}

        function resetHighlight(e) {{
            geojson.resetStyle(e.target);
            e.target.closePopup();
        }}

        function onEachFeature(feature, layer) {{
            layer.on({{
                mouseover: highlightFeature,
                mouseout: resetHighlight
            }});
        }}

        var geojson = L.geoJson(countriesData, {{
            style: style,
            onEachFeature: onEachFeature
        }}).addTo(map);
    </script>
    """
    return html_code, prod_par_pays,grouped_data, country_colors


html_code, prod_par_pays,grouped_data, country_colors = carte(edf_world, selected_year)




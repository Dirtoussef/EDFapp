# EDFapp

![Logo EDF](imges/EDF.png)
# ⚡ EDF - Dashboard de production énergétique

Ce projet est une application interactive développée avec **Streamlit** permettant de visualiser les données de production énergétique en France et dans le monde, par filière (fossile, renouvelable, nucléaire.. ), avec des données issues d’un fichier Excel et d’une API.

---

## 🧰 Fonctionnalités


- 📈 **Métriques dynamiques** en haut de l'application pour afficher la production totale et le type d'énergie produite, avec l'évolution en pourcentage
- 📂 **Exploration interactive** des bases de données :
  - Fichier Excel France (`lelec.xlsx`)
  - Fichier API Monde (`Edf_world.xlsx`)
- 📊 **Visualisations riches et filtrables** :
  - Courbes, barplots, boxplots et matrice de corrélation
  - Filtrage par **année**, **pays** et **secteur**  **Type de Graphique** **Type d'énergie** 
  - Comparaison des filières : **renouvelables**, **fossiles**, **nucléaire**
- 🌍 **Comparaison France vs Monde** sur la production énergétique et les émissions de CO₂
- 🗺️ **Carte interactive personnalisée** :
  - Affichage de la production par pays
  - Répartition par type d’énergie (**Renouvelable**, **Fossile**, **Nucléaire**, **Various**)
  - Filtrage par année 

## 📁 Structure du projet

EDF/ ├── components/ # Modules Python (interface, cartes, visualisations) │ ├── EDF.py │ ├── Edfdata.py │ ├── Map.py │ └── carte_edf_style_emaps.html │ ├── data/ # Données Excel (non versionnées) │ ├── lelec.xlsx │ └── Edf_world.xlsx │ ├── img/ # Logos et captures d’écran │ └── EDF.png │ ├── temp_images/ # Images temporaires pour les PDF ├── .gitignore ├── requirements.txt └── README.md


## 🛠️ Technologies utilisées

### 📦 Backend / Data

- [Python 3.x](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Openpyxl](https://openpyxl.readthedocs.io/) – pour lire les fichiers Excel
- [PyCountry](https://pypi.org/project/pycountry/) – pour la détection des pays
- [Requests](https://docs.python-requests.org/) – pour les appels API
- [FPDF](https://pyfpdf.readthedocs.io/) – pour l’export PDF

### 📊 Visualisation

- [Streamlit](https://streamlit.io/) – interface web interactive
- [Plotly](https://plotly.com/python/) – pour les courbes, barplots et donuts
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/) – pour les boxplots et corrélations

### 🗺️ Cartographie

- [Leaflet.js](https://leafletjs.com/) – affichage de la carte interactive personnalisée (via HTML/JS injecté dans Streamlit)
- [GeoJSON](https://geojson.org/) – pour les contours de pays

### 🌐 Web & autres

- [Jinja2](https://jinja.palletsprojects.com/) – pour les templates HTML
- [GitPython](https://github.com/gitpython-developers/GitPython) – versioning






## 🚀 Lancer le projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/Dirtoussef/EDFapp.git
cd EDF
```
### 2. Créer et activer un environnement virtuel

```bash
python -m venv edf_env
.\edf_env\Scripts\activate
```

###  3. Installer les dépendances

```bash
pip install -r requirements.txt
```


###  4. Lancer l'application Streamlit
```bash
streamlit run components/EDF.py
```


## 🧪 Utilisation de l'application

L'application dispose d'une **barre latérale** permettant de filtrer les résultats et se compose de plusieurs **onglets** ayant chacun une fonctionnalité spécifique.

> Tous les onglets partagent également des métriques statiques affichant la production totale et la répartition par type d’énergie ainsi que d'autre métriques.

---
☑️ **Sidebar interactive**  
### Onglet 1 : Fichier Excel France


L'onglet principal permet d’avoir une vue d’ensemble sur les indicateurs globaux. On y retrouve :

- 📄 Visualisation et filtrage des données issues du fichier `lelec.xlsx`
- Possibilité de filtrer par **année** et **type de graphique** (Courbe ou Boxplot)
- 📊 Métriques dynamiques : production totale, part de renouvelable, fossile, nucléaire…
- 🔁 Évolution par rapport à l’année précédente
- 📈 Graphiques interactifs : Courbes, Barplots, Boxplots, Matrice de corrélation, Donut

---
Démonstration Gif:

![Démo de l'application – France](imges/demo1.gif)

---

### Onglet 2 : Données API (Monde)

🌍 Données issues du fichier `Edf_world.xlsx`, alimenté par une API.

- 📄 Tableau interactif filtrable par :
  - **Année**
  - **Pays**
  - **Filière**
  - **Type d'énergie**
- 📊 Métriques dynamiques :
  - Production totale
  - Part d’énergie et de chaleur
  - Nombre de pays où EDF est actif
  - Top pays producteurs
- 📈 Visualisations interactives : Courbes, Barplots, Donuts
- 🗺️ **Carte mondiale interactive** :
  - Filtrable par année
  - Affiche la production et la


---

Démonstration Gif:

![Démo de l'application – France](imges/demo2.gif)

---




## 👤 Auteur

Développé par **Youssef Dir**  
📫 [youssefdir37@gmail.com](mailto:youssefdir37@gmail.com)  
📍 Paris – 2025  
🔗 [LinkedIn](https://www.linkedin.com/in/youssef-dir-798469160/) 



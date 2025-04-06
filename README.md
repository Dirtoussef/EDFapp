# EDFapp

![Logo EDF](img/EDF.png)
# ⚡ EDF - Dashboard de production énergétique

Ce projet est une application interactive développée avec **Streamlit** permettant de visualiser les données de production électrique en France et dans le monde, par filière (fossile, renouvelable, nucléaire), avec des données issues d’un fichier Excel et d’une API.

---

## 🧰 Fonctionnalités


- 📈 **Métriques dynamiques** en haut de l'application pour afficher la production totale et le type d'énergie produite, avec l'évolution en pourcentage
- 📂 **Exploration interactive** des bases de données :
  - Fichier Excel France (`lelec.xlsx`)
  - Fichier API Monde (`Edf_world.xlsx`)
- 📊 **Visualisations riches et filtrables** :
  - Courbes, barplots, boxplots et matrice de corrélation
  - Filtrage par **année**, **pays** et **secteur d'activité**
  - Comparaison des filières : **renouvelables**, **fossiles**, **nucléaire**
- 🌍 **Comparaison France vs Monde** sur la production énergétique et les émissions de CO₂
- 🗺️ **Carte interactive personnalisée** :
  - Affichage de la production par pays
  - Répartition par type d’énergie (**Renouvelable**, **Fossile**, **Nucléaire**, **Various**)
  - Filtrage par année 

## 📁 Structure du projet

EDF/ ├── components/ # Modules Python (interface, cartes, visualisations) │ ├── EDF.py │ ├── Edfdata.py │ ├── Map.py │ └── carte_edf_style_emaps.html │ ├── data/ # Données Excel (non versionnées) │ ├── lelec.xlsx │ └── Edf_world.xlsx │ ├── img/ # Logos et captures d’écran │ └── EDF.png │ ├── temp_images/ # Images temporaires pour les PDF ├── .gitignore ├── requirements.txt └── README.md


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


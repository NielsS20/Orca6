import streamlit as st
import pandas as pd
import requests

st.title("Lead-Generierungs-Dashboard für Industriemontagen")

# Ersetze mit deinem NewsAPI-Key
API_KEY = "721edb11114a40119016623e7236156d"

# Reduziertes festes Set an Keywords (Top 20 für bessere Queries; erweiterbar via Input)
default_keywords = [
    "Fabrikverlagerung", "Anlagenerweiterung", "Maschineninstallation", "Fabrikabbau", 
    "Maschinenmontage", "Fabrikumzug", "Maschinenabbau", "Maschinenverlagerung",
    "Anlagenverlagerung", "Standortvorbereitung",
    "factory relocation", "plant expansion", "machine installation", "factory dismantling", 
    "machinery assembly", "factory move", "machine dismantling", "machine relocation",
    "equipment relocation", "site preparation"
]

# Regionen (fest: Europa/Asien)
regions = ["Europa", "Asien"]

# Funktion zum Aufteilen der Keywords in Batches und Mergen der Ergebnisse
def fetch_news_in_batches(query_keywords, selected_regions, batch_size=5):
    if not API_KEY or API_KEY == "dein_newsapi_key_hier_einfuegen":
        st.error("Bitte einen gültigen NewsAPI-Key in app.py einfügen!")
        return pd.DataFrame()
    
    all_leads = []
    debug_info = []  # Für Debugging
    
    # Keywords in Batches aufteilen
    for i in range(0, len(query_keywords), batch_size):
        batch_keywords = query_keywords[i:i + batch_size]
        if not batch_keywords:
            continue
        query = f"({' OR '.join(batch_keywords)})"
        
        if len(query) > 500:
            st.warning(f"Batch-Query zu lang ({len(query)} Zeichen) – überspringe Batch.")
            continue
        
        url = f"https://newsapi.org/v2/everything?q={query}&to=2025-12-31&language=de,en&apiKey={API_KEY}&sortBy=publishedAt&pageSize=20"
        response = requests.get(url)
        if response.status_code !=

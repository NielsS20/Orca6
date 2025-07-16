import streamlit as st
import pandas as pd
import requests

st.title("Lead-Generierungs-Dashboard für Industriemontagen")

# Ersetze mit deinem NewsAPI-Key (kostenlos bei newsapi.org holen)
API_KEY = "721edb11114a40119016623e7236156d"

# Erweitertes festes Set an Keywords (auf Deutsch und Englisch, basierend auf Branchenbegriffen)
default_keywords = [
    "Fabrikverlagerung", "Anlagenerweiterung", "Maschineninstallation", "Fabrikabbau", 
    "Industrielle Relokation", "Maschinenmontage", "Anlagenstilllegung", "Fabrikumzug", 
    "Produktionslinienaufbau", "Maschinenabbau", "Demontage-Dienste", "Maschinenverlagerung",
    "Schwerlasttransport", "Elektrodemontage", "Mechanische Demontage", "Anlagenverlagerung",
    "Produktionslinienverlagerung", "Industrielle Anlagen", "Mechanische Wartung", 
    "Maschinenentfernung", "Schwergutbewegung", "Standortvorbereitung", "Rigging-Dienste",
    "factory relocation", "plant expansion", "machine installation", "factory dismantling", 
    "industrial relocation", "machinery assembly", "plant shutdown", "factory move", 
    "production line setup", "machine dismantling", "decommissioning services", "machine relocation",
    "machinery moving", "electrical decommissioning", "mechanical decommissioning", "equipment relocation",
    "production line relocation", "industrial installations", "mechanical maintenance", 
    "machine removal", "heavy equipment move", "site preparation", "rigging services"
]

# Regionen (fest: Europa/Asien)
regions = ["Europa", "Asien"]

# Funktion zum Aufteilen der Keywords in Batches und Mergen der Ergebnisse
def fetch_news_in_batches(query_keywords, selected_regions, batch_size=10):
    if not API_KEY or API_KEY == "dein_newsapi_key_hier_einfuegen":
        st.error("Bitte einen gültigen NewsAPI-Key in app.py einfügen!")
        return pd.DataFrame()
    
    all_leads = []
    region_query = f"({' OR '.join(selected_regions)})"
    
    # Keywords in Batches aufteilen
    for i in range(0, len(query_keywords), batch_size):
        batch_keywords = query_keywords[i:i + batch_size]
        if not batch_keywords:
            continue
        keyword_query = f"({' OR '.join(batch_keywords)})"
        query = f"{keyword_query} AND {region_query}"
        
        # Überprüfe Query-Länge (sicherheitshalber)
        if len(query) > 500:
            st.warning(f"Batch-Query ist immer noch zu lang ({len(query)} Zeichen). Reduziere Keywords.")
            continue
        
        url = f"https://newsapi.org/v2/everything?q={query}&language=de,en&apiKey={API_KEY}&sortBy=publishedAt&pageSize=20"
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"API-Fehler in Batch: {response.text}")
            continue
        
        articles = response.json().get('articles', [])
        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('description', '')).lower()
            matching_regions = [r for r in selected_regions if r.lower() in content]
            if matching_regions:
                all_leads.append({
                    'Region': ', '.join(matching_regions) or 'Unbekannt',
                    'Company': article['source']['name'],
                    'Event': article['title'],
                    'Source': article['url'],
                    'Language': 'Deutsch' if 'de' in article.get('language', 'en') else 'English',
                    'Potential Contacts': 'Simuliert: Operations Manager (linkedin.com/in/beispiel); Procurement Director (linkedin.com/in/beispiel2) - Integriere LinkedIn API für echte Kontakte.'
                })
    
    # Duplikate entfernen (basierend auf Source-URL)
    df = pd.DataFrame(all_leads).drop_duplicates(subset=['Source'])
    return df

# User-Inputs
selected_regions = st.multiselect("Regionen wählen", regions, default=regions)
custom_keywords = st.text_input("Zusätzliche Keywords (kommagetrennt hinzufügen)", "")
all_keywords = default_keywords + [k.strip() for k in custom_keywords.split(',') if k.strip()]

if st.button("Leads generieren"):
    df = fetch_news_in_batches(all_keywords, selected_regions)
    if not df.empty:
        st.markdown("### Generierte Leads")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Keine relevanten Leads gefunden. Probiere andere Keywords oder überprüfe den API-Key.")

# Export-Option
if 'df' in locals() and not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Leads als CSV herunterladen", csv, "leads.csv", "text/csv")

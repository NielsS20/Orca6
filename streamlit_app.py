import streamlit as st
import pandas as pd
import requests

st.title("Lead-Generierungs-Dashboard für Industriemontagen")

# Ersetze mit deinem NewsAPI-Key
API_KEY = "721edb11114a40119016623e7236156d"  # Dein Key hier eingefügt

# Optimisiertes Set an Keywords (fokussiert auf trefferträchtige Begriffe)
default_keywords = [
    "Fabrikverlagerung", "Anlagenerweiterung", "Fabrikumzug", "Maschinenverlagerung",
    "factory relocation", "plant expansion", "factory move", "machine relocation",
    "equipment relocation"
]

# Regionen (fest: Europa/Asien)
regions = ["Europa", "Asien"]

# Funktion zum Aufteilen der Keywords in Batches und Mergen der Ergebnisse
def fetch_news_in_batches(query_keywords, selected_regions, batch_size=1):  # 1 pro Batch für einfache Queries
    if not API_KEY or API_KEY == "dein_newsapi_key_hier_einfuegen":
        st.error("Bitte einen gültigen NewsAPI-Key in app.py einfügen!")
        return pd.DataFrame()
    
    all_leads = []
    debug_info = []  # Für Debugging
    
    # Keywords in Batches aufteilen (hier einzeln)
    for i in range(0, len(query_keywords), batch_size):
        batch_keywords = query_keywords[i:i + batch_size]
        if not batch_keywords:
            continue
        query = f"({' OR '.join(batch_keywords)})"
        
        if len(query) > 500:
            st.warning(f"Batch-Query zu lang ({len(query)} Zeichen) – überspringe Batch.")
            continue
        
        url = f"https://newsapi.org/v2/everything?q={query}&language=de,en&apiKey={API_KEY}&sortBy=publishedAt&pageSize=20"
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"API-Fehler in Batch: {response.text}")
            continue
        
        articles = response.json().get('articles', [])
        debug_info.append(f"Batch '{query}': {len(articles)} Articles gefunden")
        
        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('description', '')).lower()
            matching_regions = [r for r in selected_regions if r.lower() in content]
            if matching_regions or not selected_regions:  # Filter nur, wenn Regionen ausgewählt
                all_leads.append({
                    'Region': ', '.join(matching_regions) or 'Alle',
                    'Company': article['source']['name'],
                    'Event': article['title'],
                    'Source': article['url'],
                    'Language': 'Deutsch' if 'de' in article.get('language', 'en') else 'English',
                    'Potential Contacts': 'Simuliert: Operations Manager (linkedin.com/in/beispiel); Procurement Director (linkedin.com/in/beispiel2) - Integriere LinkedIn API für echte Kontakte.'
                })
    
    # Duplikate entfernen
    df = pd.DataFrame(all_leads).drop_duplicates(subset=['Source'])
    
    # Debugging-Ausgabe
    st.info("Debug-Info: " + "; ".join(debug_info))
    return df

# User-Inputs
selected_regions = st.multiselect("Regionen wählen (deaktiviere für breitere Suche)", regions, default=[])
custom_keywords = st.text_input("Zusätzliche Keywords (kommagetrennt hinzufügen)", "")
all_keywords = default_keywords + [k.strip() for k in custom_keywords.split(',') if k.strip()]

if st.button("Leads generieren"):
    df = fetch_news_in_batches(all_keywords, selected_regions)
    if not df.empty:
        st.markdown("### Generierte Leads")
        st.dataframe(df, use_container_width=True)
    else:
        # Fallback: Versuche ohne Regionen
        st.warning("Keine Leads mit Regionen gefunden. Versuche Fallback ohne Regionen...")
        fallback_df = fetch_news_in_batches(all_keywords, [])
        if not fallback_df.empty:
            st.markdown("### Fallback-Leads (ohne Regionsfilter)")
            st.dataframe(fallback_df, use_container_width=True)
        else:
            st.error("Immer noch keine Leads. Teste manuell: https://newsapi.org/v2/everything?q=factory+relocation&apiKey=DEIN_KEY")

# Export-Option
if 'df' in locals() and not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Leads als CSV herunterladen", csv, "leads.csv", "text/csv")

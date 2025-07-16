import streamlit as st
import pandas as pd
import requests

st.title("Lead-Generierungs-Dashboard für Industriemontagen")

# Ersetze mit deinem NewsAPI-Key (kostenlos bei newsapi.org holen)
API_KEY = "dein_newsapi_key_hier_einfuegen"

# Standard-Keywords und Regionen (Europa/Asien, Deutsch/Englisch)
default_keywords = ["Fabrikverlagerung", "factory relocation", "Fabrikerweiterung", "plant expansion", "Maschinenabbau", "machine dismantling"]
regions = ["Europa", "Asien"]

def fetch_news(query_keywords, selected_regions):
    if not API_KEY or API_KEY == "dein_newsapi_key_hier_einfuegen":
        st.error("Bitte einen gültigen NewsAPI-Key in app.py einfügen!")
        return pd.DataFrame()
    
    url = f"https://newsapi.org/v2/everything?q={' OR '.join(query_keywords)}&language=de,en&apiKey={API_KEY}&sortBy=publishedAt&pageSize=20"
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"API-Fehler: {response.text}")
        return pd.DataFrame()
    
    articles = response.json().get('articles', [])
    leads = []
    for article in articles:
        content = (article.get('title', '') + ' ' + article.get('description', '')).lower()
        matching_regions = [r for r in selected_regions if r.lower() in content]
        if matching_regions:
            leads.append({
                'Region': ', '.join(matching_regions) or 'Unbekannt',
                'Company': article['source']['name'],
                'Event': article['title'],
                'Source': article['url'],
                'Language': 'Deutsch' if 'de' in article.get('language', 'en') else 'English',
                'Potential Contacts': 'Simuliert: Operations Manager (linkedin.com/in/beispiel); Procurement Director (linkedin.com/in/beispiel2) - Integriere LinkedIn API für echte Kontakte.'
            })
    return pd.DataFrame(leads)

# User-Inputs
selected_regions = st.multiselect("Regionen wählen", regions, default=regions)
custom_keywords = st.text_input("Zusätzliche Keywords (kommagetrennt)", "")
all_keywords = default_keywords + [k.strip() for k in custom_keywords.split(',') if k.strip()]

if st.button("Leads generieren"):
    df = fetch_news(all_keywords, selected_regions)
    if not df.empty:
        st.markdown("### Generierte Leads")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Keine relevanten Leads gefunden. Probiere andere Keywords oder überprüfe den API-Key.")

# Export-Option
if 'df' in locals() and not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Leads als CSV herunterladen", csv, "leads.csv", "text/csv")

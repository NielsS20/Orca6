import streamlit as st
import pandas as pd
import feedparser  # Für RSS-Parsing (pip install feedparser)

st.title("Lead-Generierungs-Dashboard für Industriemontagen – Mit Google News RSS")

# Optimisiertes Set an Keywords (fokussiert auf trefferträchtige Begriffe)
default_keywords = [
    "Fabrikverlagerung", "Anlagenerweiterung", "Fabrikumzug", "Maschinenverlagerung",
    "factory relocation", "plant expansion", "factory move", "machine relocation",
    "equipment relocation"
]

# Regionen (fest: Europa/Asien)
regions = ["Europa", "Asien"]

def fetch_news_from_rss(query_keywords, selected_regions):
    all_leads = []
    debug_info = []  # Für Debugging
    
    for keyword in query_keywords:
        # RSS-Query bauen (für Englisch/Deutsch, mit Regionen)
        region_str = " ".join(selected_regions) if selected_regions else ""
        query = f"{keyword} {region_str} 2025"
        rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=de-DE&gl=DE&ceid=DE:de"  # Deutsch-fokussiert; für Englisch &hl=en-US&gl=US
        
        feed = feedparser.parse(rss_url)
        num_entries = len(feed.entries)
        debug_info.append(f"Keyword '{keyword}': {num_entries} Articles gefunden")
        
        for entry in feed.entries:
            content = (entry.get('title', '') + ' ' + entry.get('summary', '')).lower()
            matching_regions = [r for r in selected_regions if r.lower() in content]
            if matching_regions or not selected_regions:
                all_leads.append({
                    'Region': ', '.join(matching_regions) or 'Alle',
                    'Company': entry.get('source', {}).get('title', 'Unbekannt'),
                    'Event': entry.title,
                    'Source': entry.link,
                    'Language': 'Deutsch' if 'de' in rss_url else 'English',
                    'Potential Contacts': 'Simuliert: Operations Manager (linkedin.com/in/beispiel); Procurement Director (linkedin.com/in/beispiel2) - Integriere LinkedIn API für echte Kontakte.'
                })
    
    # Duplikate entfernen
    df = pd.DataFrame(all_leads).drop_duplicates(subset=['Source'])
    
    # Debugging-Ausgabe
    st.info("Debug-Info: " + "; ".join(debug_info))
    return df

# User-Inputs
selected_regions = st.multiselect("Regionen wählen (deaktiviere für breitere Suche)", regions, default=regions)
custom_keywords = st.text_input("Zusätzliche Keywords (kommagetrennt hinzufügen)", "")
all_keywords = default_keywords + [k.strip() for k in custom_keywords.split(',') if k.strip()]

if st.button("Leads generieren"):
    df = fetch_news_from_rss(all_keywords, selected_regions)
    if not df.empty:
        st.markdown("### Generierte Leads")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Keine Leads gefunden. Passe Keywords an oder deaktiviere Regionen.")

# Export-Option
if 'df' in locals() and not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Leads als CSV herunterladen", csv, "leads.csv", "text/csv")

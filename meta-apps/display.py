import streamlit as st
import pandas as pd
import random

# CSV-Daten laden
csv_data = pd.read_csv("testneu2.csv", sep=";")
st.dataframe(csv_data)

# Initialisiere Session State Keys
if "selected_game" not in st.session_state:
    game_titles = list(csv_data["title"].dropna())
    st.session_state.selected_game = random.choice(game_titles)
if "selected_fach" not in st.session_state:
    st.session_state.selected_fach = ""

# Callback-Funktionen, die den jeweils anderen Wert zurücksetzen
def game_changed():
    st.session_state.selected_fach = ""

def fach_changed():
    st.session_state.selected_game = ""

spalten = [
    "title", "image", "meta_store", "entwickler", "beschreibung", "unterricht", "stichpunkte",
    "usk", "klassenstufe", "kosten", "internet", "sprachen", "didaktische_hinweise1", "didaktische_hinweise2", "didaktische_hinweise3",
    "platzbedarf", "in_app_kaeufe", "speicherplatz", "quelle", "kompfort", "triggerwarnung",
    "nutzungshinweise", "aktueller_stand", "meta_id"
]

# Funktion für den gemeinsamen Layout-Code
def display_app_layout(data):
    st.title(data.get("title", "Kein Titel"))
    
    o1, o2 = st.columns(2)
    o1.image(data.get("image", ""), caption=f"Quelle: [Meta Store]({data.get('meta_store','')}) / [Entwickler]({data.get('entwickler','')})")
    o2.markdown(f"#### Beschreibung\n{data.get('beschreibung','')}")
    o2.link_button("📼 Trailer", "https://scontent-fra5-2.oculuscdn.com/v/t64.7195-25/39035397_979242124239986_3074018985684072980_n.mp4?_nc_cat=1&ccb=1-7&_nc_sid=b20b63&_nc_ohc=UiEcg5dDe3QQ7kNvgHIpgvB&_nc_oc=AdihuPyre669peLIt-nIciWsuHquCYX8t83ahUN1hYAhrTlgpGAutDqzsFeOOcQnpEkCRaBMOnpWnCC1X9li42lA&_nc_zt=28&_nc_ht=scontent-fra5-2.oculuscdn.com&_nc_gid=AiNbdiX3JTTWjd_Ig0aDHH3&oh=00_AYA4cENOGJnGUMdCDk_VNJem6rl5iL9wvQVs6_Sr8MUBog&oe=67B6AAC1", use_container_width=True, type="secondary")
        
    f1, f2 = st.columns(2)
    f1.markdown(f"<div style='font-size:20px'><b>Unterricht</b><br>{data.get('unterricht','')}</div>", unsafe_allow_html=True)
    f2.markdown(f"<div style='font-size:20px'><b>Stichpunkte</b><br>{data.get('stichpunkte','')}</div>", unsafe_allow_html=True)
    
    st.write("")
    with st.expander("Weitere Informationen"):
        a, b, c, d = st.columns(4)
        a.metric("USK", f"{data.get('usk','')}", border=True)
        b.metric("Klassenstufe", f"{data.get('klassenstufe','')}", border=True)
        c.metric("Kosten", f"{data.get('kosten','')}", border=True)
        d.metric("Internet", f"{data.get('internet','')}", border=True)
    
        st.caption("Sprachen")
        st.write(data.get("sprachen", ""))
    
        st.divider()
        st.header("Didaktische Hinweise")
        st.markdown(f"""
        {data.get('didaktische_hinweise1','')}   
        
        {data.get('didaktische_hinweise2','')}   
        
        {data.get('didaktische_hinweise3','')}
        """)
        
        st.header("Kompetenzen")
        st.write("Hier könnten die Kompetenzen stehen.")
        st.link_button("Weitere Materialien im Bildungsportal RLP", "https://streamlit.io/gallery", use_container_width=True, type="primary")
        
        st.divider()
        st.header("Beratung und Verleih")
        
        kmz1, kmz2, kmz3 = st.columns(3)
        kmz1.link_button("KMZ1", "https://streamlit.io/gallery", use_container_width=True)
        kmz2.link_button("KMZ2", "https://streamlit.io/gallery", use_container_width=True)
        kmz3.link_button("KMZ3", "https://streamlit.io/gallery", use_container_width=True)

        st.divider()
        st.header("Nutzungshinweise")
        st.metric("Platzbedarf", data.get("platzbedarf", ""), border=True)
    
        n1, n2, n3 = st.columns(3)
        n1.metric("In-App-Käufe", f"{data.get('in_app_kaeufe','')}", border=True)
        n2.metric("Speicherplatz", f"{data.get('speicherplatz','')}", border=True)
        n3.metric("Quelle", f"{data.get('quelle','')}", border=True)
    
        a1, b1 = st.columns(2)
        a1.metric("Komfort", f"{data.get('kompfort','')}", border=True)
        b1.metric("Triggerwarnung", f"{data.get('triggerwarnung','')}", border=True)
    
        st.write(f"{data.get('nutzungshinweise','')}")
    
        st.divider()
        st.write(f"Aktualisiert: {data.get('aktueller_stand','')}")
        st.write(f"ID: {data.get('meta_id','')}")

f1, f2 = st.columns(2)

# Spiele auswählen (Optionen-Liste um ein leeres Element erweitern)
spiel_titel = [""] + list(csv_data["title"].dropna())
selected_game = f1.selectbox(
    "Spiele", 
    spiel_titel, 
    key="selected_game", 
    on_change=game_changed
)

# Fächer auswählen (Optionen-Liste um ein leeres Element erweitern)
unterricht_strings = csv_data["unterricht"].dropna()  # NaN-Werte ignorieren
unterricht_list = [fach.strip() for unterricht in unterricht_strings for fach in unterricht.split(",")]
unterricht_list = sorted(set(unterricht_list))
unterricht_list = [""] + unterricht_list
selected_fach = f2.selectbox(
    "Fächer", 
    unterricht_list, 
    key="selected_fach", 
    on_change=fach_changed
)

if st.session_state.selected_game != "":
    selected_row = csv_data[csv_data["title"] == st.session_state.selected_game].squeeze()
    if not selected_row.empty:
        display_app_layout(selected_row.to_dict())
elif st.session_state.selected_fach != "":
    selected_rows = csv_data[csv_data["unterricht"].str.contains(st.session_state.selected_fach, na=False)]
    # Ausgabe aller Spiele, die zu dem ausgewählten Fach passen:
    for index, row in selected_rows.iterrows():
        display_app_layout(row.to_dict())

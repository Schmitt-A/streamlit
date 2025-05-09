import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="Meta Quest - Apps für den Bildungsbereich", layout="wide")

#Passwort zum Bearbeiten der Datenbank
password = f"{st.secrets.editor_password}"

# MySQL-Verbindungsinformationen
def get_db_connection():
    return mysql.connector.connect(
        host=f"{st.secrets.db_host}",
        user=f"{st.secrets.db_user}",
        password=f"{st.secrets.db_password}",        
        database=f"{st.secrets.db_name}" 
    )

# Daten aus der Datenbank abrufen
def fetch_apps():
    conn = get_db_connection()
    query = "SELECT * FROM Apps"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Daten in die Datenbank schreiben
def update_apps(df):
    conn = get_db_connection()
    cursor = conn.cursor()
    columns = [
        "ID", "ErfDatum", "Name", "USK", "Preis", "Sprache", "Internet",
        "Schlagworte", "Klasse", "Kategorie", "Handout", "Videos",
        "Nutzungshinweise", "MotionSickness", "Triggerwarnung", "Kommentar",
        "KMZ", "MaterialLink", "MetaLink", "Sonstiges"
    ]
    query = """
        REPLACE INTO Apps (
            ID, ErfDatum, Name, USK, Preis, Sprache, Internet, Schlagworte, Klasse, 
            Kategorie, Handout, Videos, Nutzungshinweise, MotionSickness, Triggerwarnung, 
            Kommentar, KMZ, MaterialLink, MetaLink, Sonstiges
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for _, row in df.iterrows():
        values = []
        for col in columns:
            wert = row[col]
            if pd.isnull(wert):
                wert = None
            values.append(wert)
        cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()


# Streamlit UI
def main():
    st.title("Meta Quest - Anwendungen für den Bildungsbereich")

    # Prüfen ob der User eingeloggt ist
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    try:
        df = fetch_apps()

        # Umwandlung der Preis-Spalte in einen numerischen Typ
        df[df.columns[4]] = pd.to_numeric(df[df.columns[4]], errors="coerce")
        
        # Konvertiere Handout und Video in boolean
        df[df.columns[10]] = df[df.columns[10]].astype(bool)
        df[df.columns[11]] = df[df.columns[11]].astype(bool)
        
        column_config = {
            df.columns[1]: st.column_config.DateColumn("Erfassungsdatum", format="YYYY-MM-DD"),
            df.columns[3]: st.column_config.NumberColumn("USK", step=1),
            df.columns[4]: st.column_config.NumberColumn("Preis", format="%.2f €", step=0.01),
            df.columns[5]: st.column_config.SelectboxColumn("Sprache", options=["DE", "EN", "SP"]),
            df.columns[6]: st.column_config.SelectboxColumn("Internet", options=["Offline", "Online"]),
            df.columns[8]: st.column_config.SelectboxColumn("Klasse", options=["GS", "OS", "Sek1", "Sek2", "GS/OS", "OS/Sek1", "Sek1/Sek2"]),
            df.columns[9]: st.column_config.SelectboxColumn("Kategorie", options=["Lernanwendung","Immersion und Interaktion", "Kreativität", "interaktive Geschichten", "Filmbildung", "Berufsorientierung"]),
            df.columns[10]: st.column_config.CheckboxColumn("Handout"),
            df.columns[11]: st.column_config.CheckboxColumn("Video"),
            df.columns[12]: st.column_config.SelectboxColumn("Nutzungshinweise", options=["Roomscale, Stationär (+)", "Roomscale (+), Stationär", "Stationär", "Roomscale"]),
            df.columns[13]: st.column_config.SelectboxColumn("Motion Sickness", options=["Gering", "Mittel", "Hoch"]),
            df.columns[14]: st.column_config.SelectboxColumn("Triggerwarnung", options=["Keine", "Gering", "Mittel", "Hoch"]),
            df.columns[16]: st.column_config.SelectboxColumn("KMZ", options=["ALT", "AZW", "BNA", "BIR", "BIT", "COC", "DER", "GMH", "KSL", "KOB", "KUS", "NWD", "LUD", "MAY", "MZS", "MZB", "KNW", "REN", "RLK", "SPE", "SWP", "SÜW", "TRI", "TSA", "WOR"]),
            df.columns[17]: st.column_config.LinkColumn("Material", display_text="🔗 Link"),
            df.columns[18]: st.column_config.LinkColumn("Meta Store", display_text="🔗 Link")
        }
        
        # Falls der User eingeloggt ist, wird der Dateneditor angezeigt
        if st.session_state["logged_in"]:
            
            # Button zum Abmelden
            if st.button("Abmelden"):
                st.session_state["logged_in"] = False
                st.rerun()
            
            # Neue Spalte zum Löschen hinzufügen (alle Zeilen standardmäßig nicht zu löschen)
            df["Löschen"] = False
            # Die Lösch-Spalte in der Column config konfigurieren
            column_config["Löschen"] = st.column_config.CheckboxColumn("Löschen")
        
            edited_df = st.data_editor(df, column_config=column_config, num_rows="dynamic")
            if st.button("Änderungen speichern"):
                update_apps(edited_df)
                st.success("Daten erfolgreich aktualisiert!")
                st.info("Bitte lade die Seite manuell neu, um die Änderungen zu sehen.")
        else:
            # Passwort-Eingabe
            password_input = st.text_input("Bitte Passwort eingeben:", type="password")
            if st.button("Anmelden"):
                if password_input == password:
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Falsches Passwort!")
                    
            # Datensatz anzeigen
            st.data_editor(df, disabled=True, column_config=column_config, num_rows="dynamic", hide_index=True)
                
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Daten: {e}")

if __name__ == "__main__":
    main()

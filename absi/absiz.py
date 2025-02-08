#Streamlit
import streamlit as st

#JSON
import requests
import json

#Daten für ABSIz, KiGGS und Destatis abrufen
url_absiz = "https://raw.githubusercontent.com/Schmitt-A/streamlit/refs/heads/main/absi/absiz.json"
response_absiz = requests.get(url_absiz)
data_absiz = response_absiz.json()

url_kiggs = "https://raw.githubusercontent.com/Schmitt-A/streamlit/refs/heads/main/absi/KiGGS_2007.json"
response_kiggs = requests.get(url_kiggs)
kiggs = response_kiggs.json()

url_destatis = "https://raw.githubusercontent.com/Schmitt-A/streamlit/refs/heads/main/absi/destatis-koerperma%C3%9Fe-2021.json"
response_destatis = requests.get(url_destatis)
destatis = response_destatis.json()

url_bmi = "https://raw.githubusercontent.com/Schmitt-A/streamlit/refs/heads/main/absi/BMI.json"
response_bmi = requests.get(url_bmi)
bmi_kategorien = response_bmi.json()


#Risikostufen ABSIz
#https://en.wikipedia.org/wiki/Body_shape_index
risiko_stufen = [
    (-10, -0.868, "Sehr gering", 
     "Ein sehr niedriger ABSIz-Wert deutet auf eine besonders günstige Fettverteilung hin, vor allem im Bauchbereich. "
     "Dies entspricht einem sehr niedrigen Risiko für kardiovaskuläre und metabolische Erkrankungen. "
     "Zudem weist er auf eine optimale Balance zwischen Taille und Körpergewicht hin."),
     
    (-0.868, -0.272, "Gering", 
     "Ein ABSIz-Wert in diesem Bereich zeigt, dass die Fettverteilung relativ günstig ist. "
     "Das Gesundheitsrisiko, insbesondere für Herz-Kreislauf- und Stoffwechselerkrankungen, bleibt niedrig. "
     "Dennoch ist eine regelmäßige Überprüfung der Gesundheitsparameter empfehlenswert."),
     
    (-0.272, 0.229, "Durchschnitt", 
     "Ein durchschnittlicher ABSIz-Wert signalisiert eine normale Verteilung des Körperfetts in Relation zum Gewicht. "
     "Das damit einhergehende Gesundheitsrisiko wird als moderat eingeschätzt. "
     "Es empfiehlt sich, einen gesunden Lebensstil beizubehalten, um langfristig das Risiko zu minimieren."),
     
    (0.229, 0.798, "Hoch", 
     "Ein ABSIz-Wert in diesem Bereich weist auf eine ungünstigere Fettverteilung hin, insbesondere mit erhöhter Ansammlung von viszeralem Fett. "
     "Dies kann zu einem erhöhten Risiko für kardiovaskuläre und metabolische Erkrankungen führen. "
     "Es ist ratsam, Maßnahmen zur Verbesserung der Körperzusammensetzung und zur Reduktion des Bauchfetts zu ergreifen."),
     
    (0.798, 10, "Sehr hoch", 
     "Ein sehr hoher ABSIz-Wert deutet auf eine deutlich ungünstige Fettverteilung hin, die ein erhebliches Gesundheitsrisiko signalisiert. "
     "In dieser Risikogruppe ist das Risiko für ernsthafte kardiovaskuläre und metabolische Erkrankungen signifikant erhöht. "
     "Dringend sollte ärztlicher Rat eingeholt und eine umfassende Risikoreduktion angestrebt werden.")
]




#Berechnung des ABSI-Z Wertes
def berechne_absi_z(taille, gewicht, groesse, mean_absiz, std_absiz):
    groesse = groesse / 100
    taille = taille / 100
    bmi = gewicht / (groesse ** 2)
    absi = taille / (bmi ** (2/3) * groesse ** (1/2))
    
    absi_z = (absi - mean_absiz) / std_absiz
    return bmi, absi, absi_z




st.markdown("""
# ABSIz *und* BMI
### Body-Shape-Index  und Body-Mass-Index  
""")
st.divider()
taille = st.number_input("Taillenumfang in cm:", step = 1)
gewicht = st.number_input("Gewicht in kg:", step = 1)
groesse = st.number_input("Größe in cm:", step = 1)
alter = st.number_input("Alter in Jahren:", step=1)
geschlecht = st.radio(
    "Biologisches Geschlecht:",
    ["weiblich", "männlich"],
    index=None,
)

#Differezen zu KiGGS und Destatis
#WENN ALTER UND GESCHLECHT ANGEGEBEN
if (alter is not 0) and (geschlecht is not None) and (taille is not 0) and (gewicht is not 0) and (groesse is not 0):
    
    #WENN ALTER < 18 --> KIGGS
    if alter < 18:
        statistische_quelle = "KiGGS - Körpermaße bei Kindern und Jugendlichen in Deutschland 2007"
        #WENN KIGGS IS NOT None
        if kiggs.get(f"{alter}").get(f"{geschlecht}").get("Taillenumfang") is not None:
            kiggs_taille = kiggs.get(f"{alter}").get(f"{geschlecht}").get("Taillenumfang").get("MW")
            if (kiggs_taille < taille):
                taille_diff = - abs(kiggs_taille - taille)
                taille_diff = round(taille_diff, 2)
                taille_diff = f"{taille_diff} cm"
            else:
                taille_diff = abs(taille - kiggs_taille)
                taille_diff = round(taille_diff, 2)
                taille_diff = f"{taille_diff} cm"
            
            if kiggs_taille == taille:
                taille_diff = ""
        else:
            taille_diff = ""
        
        kiggs_koerpergewicht = kiggs.get(f"{alter}").get(f"{geschlecht}").get("Körpergewicht").get("MW")       
        if kiggs_koerpergewicht is not None:  
            if gewicht is not 0:  
                if kiggs_koerpergewicht < gewicht:
                    gewicht_diff = - abs(kiggs_koerpergewicht - gewicht)
                    gewicht_diff = round(gewicht_diff, 2)
                    gewicht_diff = f"{gewicht_diff} kg"
                else:
                    gewicht_diff = abs(kiggs_koerpergewicht)
                    gewicht_diff = round(gewicht_diff, 2)
                    gewicht_diff = f"{gewicht_diff} kg"
                    
                if kiggs_koerpergewicht == gewicht:
                    gewicht_diff = ""
        else:
            gewicht_diff = ""
        
        kiggs_körpergröße = kiggs.get(f"{alter}").get(f"{geschlecht}").get("Körpergröße").get("MW")
        if kiggs_körpergröße is not None:
            if groesse is not 0:  
                if kiggs_körpergröße < groesse:
                    groesse_diff = - abs(kiggs_körpergröße - groesse)
                    groesse_diff = round(groesse_diff, 2)
                    groesse_diff = f"{groesse_diff} cm" 
                else:
                    groesse_diff = abs(groesse - kiggs_körpergröße)
                    groesse_diff = round(groesse_diff, 2)
                    groesse_diff = f"{groesse_diff} cm" 
                
                if kiggs_körpergröße == groesse:
                    groesse_diff = ""
        else:
            groesse_diff = ""
        
        kiggs_bmi = kiggs_körpergröße / (kiggs_körpergröße ** 2)
    
    if alter > 17:
        statistische_quelle = "Destatis - Körpermaße der Bevölkerung nach Altersgruppen 2021"
        
        destatis_koerpergewicht = destatis.get(f"{alter}").get(f"{geschlecht}").get("Körpergewicht")
        if destatis_koerpergewicht is not None:
            if destatis_koerpergewicht < gewicht:
                gewicht_diff = - abs(destatis_koerpergewicht - gewicht)
                gewicht_diff = round(gewicht_diff, 2)
                gewicht_diff = f"{gewicht_diff} kg"
            else:
                gewicht_diff = abs(gewicht - destatis_koerpergewicht)
                gewicht_diff = round(gewicht_diff, 2)
                gewicht_diff = f"{gewicht_diff} kg"
            
            if destatis_koerpergewicht == gewicht:
                gewicht_diff = "" 
        
        destatis_koerpergröße = destatis.get(f"{alter}").get(f"{geschlecht}").get("Körpergröße")
        if destatis_koerpergröße is not None:
            if destatis_koerpergröße < groesse:
                groesse_diff = - abs(destatis_koerpergröße - groesse)
                groesse_diff = round(groesse_diff, 2)
                groesse_diff = f"{groesse_diff} cm"
            else:
                groesse_diff = abs(groesse - destatis_koerpergröße)
                groesse_diff = round(groesse_diff, 2)
                groesse_diff = f"{groesse_diff} cm"
            
            if destatis_koerpergröße == groesse:
                groesse_diff = ""
        
        #Keine Daten für Taille vorhanden
        taille_diff = ""   
        
        

    #ABSIz (mean_absiz / std_absiz) Daten abrufen
    mean_absiz = data_absiz.get(f"{alter}").get(f"{geschlecht}").get("smoothed_absi_mean")
    std_absiz = data_absiz.get(f"{alter}").get(f"{geschlecht}").get("smoothed_absi_std")
    

if (taille and gewicht and groesse and alter != 0) and (geschlecht != None):
    col1, col2, col3 = st.columns(3)
    col1.metric("Taillenumfang", f"{taille} cm", f"{taille_diff}")
    col2.metric("Gewicht", f"{gewicht} kg", f"{gewicht_diff}")
    col3.metric("Größe", f"{groesse} cm", f"{groesse_diff}")

if (alter is not 0) and (geschlecht is not None) and (taille is not 0) and (gewicht is not 0) and (groesse is not 0):
    st.write(f"""
    Statistische Quelle: {statistische_quelle}  
    *Indikatoren unter den jeweiligen Kategorien zeigen die Differenz zum Durchschnittswert der entsprechenden Population.*
    """)

if alter != 0 and geschlecht != None:
    ncol1 ,ncol2 = st.columns(2)
    ncol1.metric("Alter", f"{alter}", "")
    ncol2.metric("Geschlecht", f"{geschlecht}", "")

bcol1, bcol2, bcol3 = st.columns(3)

if bcol2.button("ABSIz und BMI berechnen", type="primary"):
    bmi, absi_wert, absi_z_wert = berechne_absi_z(taille, gewicht, groesse, mean_absiz, std_absiz)
    st.subheader("ABSIz:")
    st.latex(r"ABSI = \frac{\text{Taillenumfang}}{\text{BMI}^{\frac{2}{3}} \times \sqrt{\text{Körpergröße}}}")
    st.latex(f"ABSI = \\frac{{{taille/100}\\,m}}{{({round(bmi, 3)}\\,kg/m^2)^{{\\frac{{2}}{{3}}}} \\times \\sqrt{{{groesse/100}\\,m}}}} = {round(absi_wert, 3)}")

    st.divider()
    
    st.latex(r"ABSIz = \frac{ABSI - ABSI_{\text{mean}}(Alter, Geschlecht)}{ABSI_{\text{std}}(Alter, Geschlecht)}")    
    st.latex(f"ABSIz = \\frac{{{round(absi_wert, 3)} - {round(mean_absiz, 3)}}}{{{round(std_absiz, 3)}}} = {round(absi_z_wert, 3)}")    
    
    for untergrenze, obergrenze, risiko, hinweis in risiko_stufen:
        if untergrenze < absi_z_wert < obergrenze:
            
            if risiko_stufen.index((untergrenze, obergrenze, risiko, hinweis)) == 0:
                #Doppelte Leerzeichen für Umbruch
                st.success(f"""
                *Risiko*: **{risiko}** *({round(absi_z_wert, 3)})*  
                *Hinweis*: {hinweis}  
                """)
            
            if risiko_stufen.index((untergrenze, obergrenze, risiko, hinweis)) == 1:
                st.success(f"""
                *Risiko*: **{risiko}** *({round(absi_z_wert, 3)})*  
                *Hinweis*: {hinweis}  
                """)
            
            if risiko_stufen.index((untergrenze, obergrenze, risiko, hinweis)) == 2:
                st.info(f"""
                *Risiko*: **{risiko}** *({round(absi_z_wert, 3)})*  
                *Hinweis*: {hinweis}  
                """)
            
            if risiko_stufen.index((untergrenze, obergrenze, risiko, hinweis)) == 3:    
                st.error(f"""
                *Risiko*: **{risiko}** *({round(absi_z_wert, 3)})*  
                *Hinweis*: {hinweis}  
                """)
                
            if risiko_stufen.index((untergrenze, obergrenze, risiko, hinweis)) == 4:    
                st.error(f"""
                *Risiko*: **{risiko}** *({round(absi_z_wert, 3)})*  
                *Hinweis*: {hinweis}  
                """)
    
    st.divider()
            
    st.subheader("BMI:")
    st.latex(r"BMI = \frac{Gewicht}{Größe^2}")
    st.latex(f"BMI = \\frac{{{gewicht}\\,kg}}{{({groesse/100}\\,m)^2}} = {round(bmi, 2)}")    
    
    #st write BMI from kiggs or destatis
    if alter < 18:
        st.error(f"""
        Bei Kindern und Jugendlichen erfolgt die BMI-Bewertung anhand  
        von alters- und geschlechtsspezifischen Wachstumstabellen, sodass  
        der exakte Referenzwert je nach Population variieren kann.  
        Somit ist die Interpretation des BMI-Wertes bei Kindern und Jugendlichen  
        nicht mit der bei Erwachsenen vergleichbar.  
        KiGGS-Durchschnittswert für den BMI: {round(kiggs_bmi,2)} *(für das entspreche Alter und Geschlecht)*
        """)

    if alter > 17:
        bmi_destatis = destatis.get(f"{alter}").get(f"{geschlecht}").get("Body-Mass-Index")
        
        
        for kategorie in bmi_kategorien:
            if kategorie["min"] < bmi < kategorie["max"]:
                st.error(f"""
                Kategorie: **{kategorie["category"]}**  
                *Pathophysiologie:* {kategorie["pathophysiology"]}  
                *Diagnostik:* {kategorie["diagnostics"]}  
                *Therapiestrategien:* {kategorie["therapy"]}  
                Destatis-Durchschnittswert für den BMI: {round(bmi_destatis, 2)} *(für das entspreche Alter und Geschlecht)*  
                """)

popover = st.popover("🔗 Quellen")

popover.link_button("🔗 Destatis - Körpermaße der Bevölkerung nach Altersgruppen 2021", "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/Gesundheitszustand-Relevantes-Verhalten/Tabellen/liste-koerpermasse.html")
popover.link_button("🔗 KiGGS - Körpermaße bei Kindern und Jugendlichen in Deutschland 2007", "https://edoc.rki.de/bitstream/handle/176904/421/23a6P5aAcd06.pdf?sequence=1&isAllowed=y")
popover.link_button("🔗 A New Body Shape Index Predicts Mortality Hazard Independently of Body Mass Index", "https://doi.org/10.1371/journal.pone.0039504")
popover.link_button("🔗 ABSIz - Body Shape Index Risikostufen", "https://en.wikipedia.org/wiki/Body_shape_index")
popover.link_button("🔗 BMI - Body Mass Index Kategorien", "https://de.wikipedia.org/wiki/Body-Mass-Index")

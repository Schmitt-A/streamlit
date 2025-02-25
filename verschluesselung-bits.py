import streamlit as st

def KODIEREN(text, schlüssel):
    binärreihe = ""
    for buchstabe in text:
        binär = bin(ord(buchstabe))[2:].zfill(8)
        binärreihe = binärreihe + binär   
    
    verschluesseltebinärreihe = ""
    for i in range(len(binärreihe)):
        if binärreihe[i] == schlüssel[i % len(schlüssel)]:
            verschluesseltebinärreihe = verschluesseltebinärreihe + "0"
        else:
            verschluesseltebinärreihe = verschluesseltebinärreihe + "1"
            
    return binärreihe, verschluesseltebinärreihe 


def DEKODIEREN(binärreihe, schlüssel):
    text = ""
    for i in range(len(binärreihe) // 8):
        byte = binärreihe[i*8 : i*8+8]
        byte = int(byte, 2)
        byte = chr(byte)
        text = text + byte
    
    entschluesseltertext = ""
    for i in range(len(binärreihe)):
        if binärreihe[i] == schlüssel[i % len(schlüssel)]:
            entschluesseltertext = entschluesseltertext + "0"
        else:
            entschluesseltertext = entschluesseltertext + "1"
    
    text_ent = ""
    for i in range(len(entschluesseltertext) // 8):
        byte_ent = entschluesseltertext[i*8 : i*8+8]
        byte_ent = int(byte_ent, 2)
        byte_ent = chr(byte_ent)
        text_ent = text_ent + byte_ent
    
    return text, entschluesseltertext, text_ent  


# Streamlit App Oberfläche
st.title("Bitverschlüsselung App")

mode = st.radio("Wählen Sie den Modus:", ("Verschlüsseln", "Entschlüsseln"))

if mode == "Verschlüsseln":
    st.header("Verschlüsselung")
    input_text = st.text_input("Geben Sie den zu verschlüsselnden Text ein:", value="Hallo")
    schlüssel_input = st.text_input("Geben Sie den Schlüssel ein:", value="00001011")
    
    if st.button("Verschlüsseln"):
        binaer, verschluesselt = KODIEREN(input_text, schlüssel_input)
        st.write("Binärrepräsentation:", binaer)
        st.write("Verschlüsselte Binärrepräsentation:", verschluesselt)

elif mode == "Entschlüsseln":
    st.header("Entschlüsselung")
    binaer_input = st.text_input("Geben Sie die Binärreihe ein, die entschlüsselt werden soll:", value="0100001101101010011001110110011101100100")
    schlüssel_input = st.text_input("Geben Sie den Schlüssel ein:", value="00001011")
    
    if st.button("Entschlüsseln"):
        original_text, entschlüsselter_binär, entschlüsselter_text = DEKODIEREN(binaer_input, schlüssel_input)
        st.write("Erst dekodierter Text:", original_text)
        st.write("Entschlüsselte Binärreihe:", entschlüsselter_binär)
        st.write("Entschlüsselter Text:", entschlüsselter_text)

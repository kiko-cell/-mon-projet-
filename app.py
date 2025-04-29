import pandas as pd
import streamlit as st
import datetime

# Titre
st.title("Suivi des Vérifications des Instruments")

# Charger les données
df = pd.read_csv("instruments.csv")

# Calculer les jours restants
today = datetime.date.today()
df['Date_prochaine_verification'] = pd.to_datetime(df['Date_prochaine_verification']).dt.date
df['Jours_restants'] = (df['Date_prochaine_verification'] - today).apply(lambda x: x.days)

# Définir si conforme ou non
df['Etat'] = df['Jours_restants'].apply(lambda x: 'Non conforme' if x < 0 else 'Conforme')

# Fonction pour colorier les lignes
def colorer_lignes(row):
    if row['Jours_restants'] < 0:
        return ['background-color: red'] * len(row)
    elif row['Jours_restants'] <= 30:
        return ['background-color: orange'] * len(row)
    elif row['Jours_restants'] <= 60:
        return ['background-color: yellow'] * len(row)
    else:
        return ['background-color: lightgreen'] * len(row)

# Afficher le tableau stylé
st.dataframe(df.style.apply(colorer_lignes, axis=1))

# Formulaire pour ajouter un nouvel instrument
st.subheader("Ajouter un nouvel instrument")
with st.form(key='add_instrument_form'):
    nom = st.text_input("Nom de l'instrument")
    date_dernier_verif = st.date_input("Date de dernière vérification")
    date_prochaine_verif = st.date_input("Date de prochaine vérification")
    
    submit_button = st.form_submit_button("Ajouter Instrument")
    
    if submit_button:
        # Ajouter la nouvelle ligne dans le dataframe
        new_row = {'Nom': nom, 'Date_derniere_verification': date_dernier_verif, 'Date_prochaine_verification': date_prochaine_verif}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Sauvegarder la nouvelle ligne dans le CSV
        df.to_csv("instruments.csv", index=False)
        
        # Afficher le message de confirmation
        st.success("Instrument ajouté avec succès!")

        # Réafficher le tableau avec la nouvelle ligne
        st.dataframe(df.style.apply(colorer_lignes, axis=1))

# Supprimer un instrument
st.subheader("Supprimer un instrument")
instrument_a_supprimer = st.selectbox("Sélectionner un instrument à supprimer", df['Nom'].unique())

if st.button("Supprimer"):
    df = df[df['Nom'] != instrument_a_supprimer]
    df.to_csv("instruments.csv", index=False)
    st.success(f"L'instrument '{instrument_a_supprimer}' a été supprimé avec succès.")
    st.dataframe(df.style.apply(colorer_lignes, axis=1))

# Mettre à jour un instrument
st.subheader("Mettre à jour un instrument")
instrument_a_mettre_a_jour = st.selectbox("Sélectionner un instrument à mettre à jour", df['Nom'].unique())

if instrument_a_mettre_a_jour:
    # Récupérer les informations de l'instrument
    instrument_info = df[df['Nom'] == instrument_a_mettre_a_jour].iloc[0]
    
    # Formulaire de mise à jour
    with st.form(key='update_instrument_form'):
        nom_nouveau = st.text_input("Nom de l'instrument", value=instrument_info['Nom'])
        date_dernier_verif_nouvelle = st.date_input("Date de dernière vérification", value=instrument_info['Date_derniere_verification'])
        date_prochaine_verif_nouvelle = st.date_input("Date de prochaine vérification", value=instrument_info['Date_prochaine_verification'])
        
        submit_update_button = st.form_submit_button("Mettre à jour l'instrument")
        
        if submit_update_button:
            # Mettre à jour le DataFrame
            df.loc[df['Nom'] == instrument_a_mettre_a_jour, 'Nom'] = nom_nouveau
            df.loc[df['Nom'] == instrument_a_mettre_a_jour, 'Date_derniere_verification'] = date_dernier_verif_nouvelle
            df.loc[df['Nom'] == instrument_a_mettre_a_jour, 'Date_prochaine_verification'] = date_prochaine_verif_nouvelle
            
            # Sauvegarder les modifications dans le CSV
            df.to_csv("instruments.csv", index=False)
            st.success(f"L'instrument '{nom_nouveau}' a été mis à jour avec succès.")
            st.dataframe(df.style.apply(colorer_lignes, axis=1))

# Notification si une date approche
proches = df[df['Jours_restants'] <= 30]
if not proches.empty:
    st.warning("⚠️ Attention ! Certains instruments doivent être vérifiés bientôt.")

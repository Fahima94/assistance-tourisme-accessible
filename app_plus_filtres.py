
import streamlit as st
import sqlite3
import pandas as pd

# Connexion à la base SQLite
conn = sqlite3.connect("assistance_tourisme.db")

st.set_page_config(page_title="Assistance Accessible Tourisme", page_icon="♿")
st.title("🧳 Analyse de l'Assistance Accessible dans les Sites Touristiques")

# Sélection d'un lieu touristique
lieux = pd.read_sql("SELECT DISTINCT lieu_touristique FROM demandes_assistance", conn)
choix_lieu = st.selectbox("📍 Choisissez un lieu touristique :", lieux["lieu_touristique"])

# Sélection d'un type de handicap
handicaps = pd.read_sql("SELECT DISTINCT type_handicap FROM demandes_assistance", conn)
choix_handicap = st.selectbox("♿ Filtrer par type de handicap :", handicaps["type_handicap"])

# Requête SQL selon la sélection
query = '''
SELECT *
FROM demandes_assistance
WHERE lieu_touristique = ?
AND type_handicap = ?
'''
df_filtre = pd.read_sql(query, conn, params=(choix_lieu, choix_handicap))

# Agrégation pour le graphe
df_graph = df_filtre.groupby("type_assistance").size().reset_index(name="nb")

# Affichage du graphique
st.subheader(f"📊 Types d’assistance demandés à {choix_lieu} ({choix_handicap})")
st.bar_chart(df_graph.set_index("type_assistance"))

# Télécharger les données filtrées
csv = df_filtre.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Télécharger les données filtrées",
    data=csv,
    file_name="donnees_filtrees.csv",
    mime="text/csv"
)

conn.close()

# import streamlit as st

# ZONES = ["Abidjan", "Bouaké", "Korhogo", "Yamoussoukro"]
# ROTATIONS = {
#     "R1": "Maïs → Niébé → Maïs",
#     "R2": "Riz → Arachide → Riz",
#     "R3": "Manioc → Maïs → Arachide",
# }
# SCENARIOS = {"sec": "Année sèche", "normal": "Année normale", "humide": "Année humide"}
# CRITERES = {
#     "eau": ("Eau (disponibilité, /100)", "modélisé"),
#     "sol": ("Sol (santé, /100)", "indirect"),
#     "rendement": ("Rendement attendu (t/ha)", "modélisé"),
#     "risque": ("Risque (/100, plus bas = mieux)", "indirect"),
# }
# BASE = {
#     "R1": {"eau": 70, "sol": 80, "rendement": 2.1, "risque": 30},
#     "R2": {"eau": 45, "sol": 60, "rendement": 3.2, "risque": 50},
#     "R3": {"eau": 60, "sol": 70, "rendement": 2.6, "risque": 40},
# }
# FACTEUR = {"sec": 0.8, "normal": 1.0, "humide": 1.1}


# def get_results(zone, rotation_id, scenario):
#     """DONNÉES FACTICES. À remplacer par l'appel à l'API."""
#     f = FACTEUR[scenario]
#     out = {}
#     for critere, valeur in BASE[rotation_id].items():
#         v = valeur / f if critere == "risque" else valeur * f
#         out[critere] = {"valeur": round(v, 1), "bas": round(v * 0.85, 1), "haut": round(v * 1.15, 1)}
#     return out


# st.set_page_config(page_title="African Crop Yield Intelligence", layout="wide")
# st.title("Comparer deux rotations culturales")
# st.warning("Données factices pour la maquette. Ces données décrivent le contexte d'une zone, pas l'état d'une parcelle.")

# zone = st.sidebar.selectbox("Zone", ZONES)
# scenario = st.sidebar.radio("Scénario climatique", list(SCENARIOS), format_func=SCENARIOS.get)

# col_a, col_b = st.columns(2)
# for col, defaut in ((col_a, "R1"), (col_b, "R2")):
#     with col:
#         rid = st.selectbox("Rotation", list(ROTATIONS), index=list(ROTATIONS).index(defaut),
#                            format_func=ROTATIONS.get, key=f"rot_{defaut}")
#         res = get_results(zone, rid, scenario)
#         for critere, (titre, nature) in CRITERES.items():
#             r = res[critere]
#             st.metric(titre, r["valeur"])
#             st.caption(f"Intervalle : {r['bas']} à {r['haut']} · Nature : {nature}")


import altair as alt
import pandas as pd
import streamlit as st

ZONES = ["Abidjan", "Bouaké", "Korhogo", "Yamoussoukro"]
ROTATIONS = {
    "R1": "Maïs → Niébé → Maïs",
    "R2": "Riz → Arachide → Riz",
    "R3": "Manioc → Maïs → Arachide",
}
SCENARIOS = {"sec": "Année sèche", "normal": "Année normale", "humide": "Année humide"}
CRITERES = {
    "eau": ("Eau (disponibilité, /100)", "modélisé"),
    "sol": ("Sol (santé, /100)", "indirect"),
    "rendement": ("Rendement attendu (t/ha)", "modélisé"),
    "risque": ("Risque (/100, plus bas = mieux)", "indirect"),
}
BASE = {
    "R1": {"eau": 70, "sol": 80, "rendement": 2.1, "risque": 30},
    "R2": {"eau": 45, "sol": 60, "rendement": 3.2, "risque": 50},
    "R3": {"eau": 60, "sol": 70, "rendement": 2.6, "risque": 40},
}
FACTEUR = {"sec": 0.8, "normal": 1.0, "humide": 1.1}


def get_results(zone, rotation_id, scenario):
    """DONNÉES FACTICES. À remplacer par l'appel à l'API."""
    f = FACTEUR[scenario]
    out = {}
    for critere, valeur in BASE[rotation_id].items():
        v = valeur / f if critere == "risque" else valeur * f
        out[critere] = {"valeur": round(v, 1), "bas": round(v * 0.85, 1), "haut": round(v * 1.15, 1)}
    return out


st.set_page_config(page_title="African Crop Yield Intelligence", layout="wide")
st.title("Comparer deux rotations culturales")
st.warning("Données factices pour la maquette. Ces données décrivent le contexte d'une zone, pas l'état d'une parcelle.")

zone = st.sidebar.selectbox("Zone", ZONES)
scenario = st.sidebar.radio("Scénario climatique", list(SCENARIOS), format_func=SCENARIOS.get)

col_a, col_b = st.columns(2)
choix = []
for col, defaut, lettre in ((col_a, "R1", "A"), (col_b, "R2", "B")):
    with col:
        rid = st.selectbox("Rotation", list(ROTATIONS), index=list(ROTATIONS).index(defaut),
                           format_func=ROTATIONS.get, key=f"rot_{defaut}")
        res = get_results(zone, rid, scenario)
        choix.append((f"{lettre} : {ROTATIONS[rid]}", res))
        for critere, (titre, nature) in CRITERES.items():
            r = res[critere]
            st.metric(titre, r["valeur"])
            st.caption(f"Intervalle : {r['bas']} à {r['haut']} · Nature : {nature}")

st.divider()
st.subheader("Comparaison par critère")
st.caption("Les barres orange montrent l'intervalle d'incertitude. Chaque critère est présenté séparément, sans score unique.")

lignes = []
for libelle, res in choix:
    for critere, r in res.items():
        lignes.append({"critere": critere, "rotation": libelle,
                       "valeur": r["valeur"], "bas": r["bas"], "haut": r["haut"]})
df = pd.DataFrame(lignes)

colonnes = st.columns(2)
for i, (critere, (titre, nature)) in enumerate(CRITERES.items()):
    sub = df[df["critere"] == critere]
    base = alt.Chart(sub).encode(
        x=alt.X("rotation:N", title=None, axis=alt.Axis(labelAngle=0, labelLimit=220))
    )
    barres = base.mark_bar().encode(
        y=alt.Y("valeur:Q", title=None),
        color=alt.Color("rotation:N", legend=None),
    )
    erreurs = base.mark_errorbar(ticks=True, color="#ff9f1c").encode(
        y=alt.Y("bas:Q"), y2="haut:Q"
    )
    graphique = (barres + erreurs).properties(title=f"{titre} · {nature}", height=260)
    colonnes[i % 2].altair_chart(graphique)




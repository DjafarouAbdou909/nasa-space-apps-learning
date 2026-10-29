from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
FICHIERS = {
    "Abidjan": "power_abidjan_daily_1981_2025.csv",
    "Bouaké": "power_bouake_daily_1981_2025.csv",
    "Korhogo": "power_korhogo_daily_1981_2025.csv",
    "Yamoussoukro": "power_yamoussoukro_daily_1981_2025.csv",
}
MOIS = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]


@st.cache_data
def charger(zone):
    df = pd.read_csv(DATA_DIR / FICHIERS[zone], skiprows=26, na_values=[-999, -999.0])
    df["date"] = pd.to_datetime(df["YEAR"] * 1000 + df["DOY"], format="%Y%j")
    df["mois"] = df["date"].dt.month
    return df[["YEAR", "mois", "T2M", "PRECTOTCORR"]]


def afficher_climat(zone):
    st.divider()
    st.subheader(f"Climat historique : {zone}")
    st.markdown(
        ":blue-badge[modélisé] NASA POWER (MERRA-2), 1981-2025. "
        "Un pixel fait environ 0,5 × 0,625°, donc ces données décrivent le contexte "
        "de la zone, pas l'état d'une parcelle."
    )
    df = charger(zone)

    # Pluie mensuelle moyenne et mois secs (définition de Bagnouls-Gaussen)
    pluie_mois = df.groupby(["YEAR", "mois"])["PRECTOTCORR"].sum(min_count=25).reset_index()
    mensuel = pd.DataFrame({
        "mois": MOIS,
        "pluie": pluie_mois.groupby("mois")["PRECTOTCORR"].mean().values,
        "temp": df.groupby("mois")["T2M"].mean().values,
    })
    mensuel["seuil"] = 2 * mensuel["temp"]
    mensuel["saison"] = (mensuel["pluie"] < mensuel["seuil"]).map({True: "mois sec", False: "mois humide"})

    base = alt.Chart(mensuel).encode(x=alt.X("mois:N", sort=MOIS, title=None, axis=alt.Axis(labelAngle=0)))
    barres = base.mark_bar().encode(
        y=alt.Y("pluie:Q", title="Pluie moyenne (mm/mois)"),
        color=alt.Color("saison:N", title=None,
                        scale=alt.Scale(domain=["mois humide", "mois sec"], range=["#3498db", "#f1c40f"])),
    )
    ligne = base.mark_line(color="#e74c3c", point=True).encode(y="seuil:Q")
    st.altair_chart((barres + ligne).properties(height=300, title="Pluie mensuelle moyenne et seuil de sécheresse (ligne rouge)"))

    secs = mensuel[mensuel["saison"] == "mois sec"]["mois"].tolist()
    st.metric("Mois secs par an (en moyenne)", len(secs))
    st.caption("Mois secs : " + (", ".join(secs) if secs else "aucun"))

    # Pluie annuelle et années sèches
    annuel = df.groupby("YEAR").agg(pluie=("PRECTOTCORR", "sum"), jours=("PRECTOTCORR", "count")).reset_index()
    annuel = annuel[annuel["jours"] >= 360]
    moyenne = annuel["pluie"].mean()
    courbe = alt.Chart(annuel).mark_line(point=True).encode(
        x=alt.X("YEAR:O", title=None, axis=alt.Axis(labelAngle=-45, values=list(range(1981, 2026, 5)))),
        y=alt.Y("pluie:Q", title="Pluie annuelle (mm)"),
    )
    repere = alt.Chart(pd.DataFrame({"m": [moyenne]})).mark_rule(color="#e74c3c", strokeDash=[6, 4]).encode(y="m:Q")
    st.altair_chart((courbe + repere).properties(height=260, title="Pluie annuelle (tirets rouges : moyenne 1981-2025)"))

    seches = annuel.nsmallest(5, "pluie")
    st.caption("Années les plus sèches : " + ", ".join(f"{int(a)} ({p:.0f} mm)" for a, p in zip(seches["YEAR"], seches["pluie"])))

    with st.expander("Définitions et sources"):
        st.markdown(
            "- **Source** : NASA POWER, données journalières, paramètres `PRECTOTCORR` (pluie) et `T2M` (température à 2 m), 1981-2025.\n"
            "- **Mois sec** : mois où la pluie moyenne (mm) est inférieure à 2 × la température moyenne (°C) (définition de Bagnouls-Gaussen). À valider avec les Data Scientists.\n"
            "- **Années sèches** : les 5 années à la plus faible pluie annuelle. Seuil provisoire.\n"
            "- Les années avec moins de 360 jours valides sont exclues."
        )
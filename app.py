import streamlit as st
import pandas as pd
import json
import os
import random

# Configurare stil Admin
st.set_page_config(page_title="The Multiplier Pro", page_icon="📈", layout="wide")

DB_FILE = "baza_multiplier_vizite.json"

# --- FUNCTII BAZA DE DATE (CONTOR OO) ---
def incarca_vizite():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {"vizite": 0}
    return {"vizite": 0}

def salveaza_vizite(date):
    with open(DB_FILE, "w") as f: json.dump(date, f)

date_sistem = incarca_vizite()

if 'v' not in st.session_state:
    date_sistem["vizite"] = date_sistem.get("vizite", 0) + 1
    salveaza_vizite(date_sistem)
    st.session_state['v'] = True

# --- TITLU ȘI CONTOR OO ---
st.title("📈 The Multiplier Pro")
st.markdown(
    f"""
    <div style='text-align: right; margin-top: -55px;'>
        <span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>
            OO: {date_sistem.get('vizite', 0)}
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)
st.markdown("### *\"The magic of compounding is the 8th wonder of the world.\"*")
st.write("---")

# --- INPUTURI ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    st.subheader("🚀 Scenariul 1: Dublare Zilnică")
    suma_start = st.number_input("Suma de start (ex: 1 leu):", value=1.0, step=0.1)
    zile_simulare = st.slider("Număr de zile de dublare:", 1, 31, 30)

with col_in2:
    st.subheader("💰 Scenariul 2: Economisire Fixă")
    suma_zilnica = st.number_input("Cât pui deoparte zilnic (fix):", value=10.0, step=5.0)

# --- LOGICA DE CALCUL ---
date_simulare = []
valoare_dublare = suma_start
valoare_acumulata_fix = 0

for zi in range(1, zile_simulare + 1):
    valoare_acumulata_fix += suma_zilnica
    date_simulare.append({
        "Ziua": zi,
        "Suma Dublată": round(valoare_dublare, 2),
        "Suma Fixă": round(valoare_acumulata_fix, 2)
    })
    valoare_dublare *= 2 

df = pd.DataFrame(date_simulare)

# --- AFIȘARE REZULTATE CHEIE ---
st.divider()
c1, c2, c3 = st.columns(3)

val_finala = df.iloc[-1]
c1.metric(f"Ziua {zile_simulare} (Dublare)", f"{val_finala['Suma Dublată']:,} lei")
c2.metric(f"Ziua {zile_simulare} (Fix)", f"{val_finala['Suma Fixă']:,} lei")
c3.metric("Multiplicator", f"x{int(val_finala['Suma Dublată'] / suma_start):,}")

# --- GRAFICUL EXPLOZIEI ---
st.divider()
st.subheader("📊 Vizualizarea Puterii Compuse (Compounding)")
st.line_chart(df.set_index("Ziua")[["Suma Dublată"]], color="#22d3ee")

# --- TABELUL DE EVOLUȚIE (Zi, Săptămână, Lună) ---
st.divider()
st.subheader("📅 Evoluția Detaliată pe Intervalele Tale")

def formatare_intervale(row):
    zi = row["Ziua"]
    if zi == 1: return "🚀 Start"
    if zi == 7: return "📅 1 Săptămână"
    if zi == 14: return "📅 2 Săptămâni"
    if zi == 21: return "📅 3 Săptămâni"
    if zi == 30: return "🏆 1 Lună"
    return f"Ziua {zi}"

df["Perioada"] = df.apply(formatare_intervale, axis=1)
st.dataframe(df[["Perioada", "Suma Dublată", "Suma Fixă"]], use_container_width=True)

# --- MESAJ ADMIN ---
st.info("💡 Observă cum în primele 20 de zile nu se întâmplă mare lucru, dar în ultimele 5 zile suma explodează exponențial!")

st.divider()
st.caption("Creat de Cristian | Protocol OO-V9 | Hardware i5 Cloud Deploy")

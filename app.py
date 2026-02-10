import streamlit as st
import pandas as pd

# Configurare stil Admin
st.set_page_config(page_title="The Multiplier Pro", page_icon="📈", layout="wide")

# --- TITLU ȘI FILOZOFIE ---
st.title("📈 The Multiplier Pro")
st.markdown("### *\"The magic of compounding is the 8th wonder of the world.\"*")
st.write("---")

# --- INPUTURI ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    st.subheader("🚀 Scenariul 1: Dublare Zilnică")
    suma_start = st.number_input("Suma de start (ex: 1 leu):", value=1.0, step=0.5)
    zile_simulare = st.slider("Număr de zile:", 1, 31, 30)

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
    valoare_dublare *= 2 # Aici se întâmplă magia dublării

df = pd.DataFrame(date_simulare)

# --- AFIȘARE REZULTATE CHEIE ---
st.divider()
c1, c2, c3 = st.columns(3)

val_finala = date_grafic = df.iloc[-1]
c1.metric(f"Ziua {zile_simulare} (Dublare)", f"{val_finala['Suma Dublată']:,} lei")
c2.metric(f"Ziua {zile_simulare} (Fix)", f"{val_finala['Suma Fixă']:,} lei")
c3.metric("Multiplicator", f"x{int(val_finala['Suma Dublată'] / suma_start):,}")

# --- GRAFICUL EXPLOZIEI ---
st.divider()
st.subheader("📊 Vizualizarea Puterii Compuse")
st.line_chart(df.set_index("Ziua")[["Suma Dublată"]], color="#ff4b4b")

# --- TABELUL DE EVOLUȚIE (Zi, Săptămână, Lună) ---
st.divider()
st.subheader("📅 Evoluția Detaliată")

# Marcăm intervalele cerute de tine
def formatare_intervale(row):
    zi = row["Ziua"]
    if zi == 1: return "Start"
    if zi == 7: return "1 Săptămână"
    if zi == 14: return "2 Săptămâni"
    if zi == 21: return "3 Săptămâni"
    if zi == 30: return "1 Lună"
    return f"Ziua {zi}"

df["Perioada"] = df.apply(formatare_intervale, axis=1)
st.dataframe(df[["Perioada", "Suma Dublată", "Suma Fixă"]], use_container_width=True)

# --- MESAJ ADMIN ---
st.info("💡 Observă cum în primele 20 de zile nu se întâmplă mare lucru, dar în ultimele 5 zile suma explodează. Asta e răbdarea de Admin!")

st.divider()
st.caption("Creat de Cristian | OO Protocol | The Compound Effect Simulator")
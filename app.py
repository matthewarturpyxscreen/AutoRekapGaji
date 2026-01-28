import streamlit as st
import pandas as pd

from parser_griyatekno import parse_griyatekno_log
from payroll import hitung_status

st.set_page_config("Sistem Absen & Gaji", layout="wide")
st.title("📊 Sistem Absensi & Payroll")

uploaded_file = st.file_uploader("Upload File Excel Fingerprint", type=["xls", "xlsx"])

if uploaded_file:
    df = parse_griyatekno_log(uploaded_file)

    statuses = df.apply(hitung_status, axis=1, result_type="expand")
    df["status"], df["potongan"], df["lembur_jam"] = statuses[0], statuses[1], statuses[2]

    st.subheader("📋 Data Absensi")
    st.dataframe(df)

    st.subheader("💰 Rekap Potongan")
    st.metric("Total Potongan", f"Rp {df['potongan'].sum():,.0f}")

    st.subheader("⏱️ Total Lembur")
    st.metric("Total Jam Lembur", f"{df['lembur_jam'].sum()} jam")

    st.download_button(
        "⬇️ Download Rekap Excel",
        data=df.to_excel(index=False),
        file_name="rekap_absensi.xlsx"
    )

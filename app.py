import streamlit as st
import pandas as pd
import tempfile
import os

from parser_griyatekno import parse_griyatekno_log
from payroll import hitung_status
from rekap import rekap_bulanan
from slip_gaji import generate_slip_gaji

st.set_page_config("Sistem Absen & Gaji", layout="wide")
st.title("📊 Sistem Absensi & Payroll")

uploaded_file = st.file_uploader(
    "Upload File Excel Fingerprint",
    type=["xls", "xlsx"]
)

if uploaded_file:
    # ===============================
    # PARSE & HITUNG ABSENSI
    # ===============================
    df = parse_griyatekno_log(uploaded_file)

    statuses = df.apply(hitung_status, axis=1, result_type="expand")
    df["status"], df["potongan"], df["lembur_jam"] = (
        statuses[0], statuses[1], statuses[2]
    )

    # ===============================
    # TAMPILKAN DATA HARIAN
    # ===============================
    st.subheader("📋 Data Absensi Harian")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Ringkasan")
    col1, col2 = st.columns(2)
    col1.metric(
        "💰 Total Potongan",
        f"Rp {df['potongan'].sum():,.0f}"
    )
    col2.metric(
        "⏱️ Total Jam Lembur",
        f"{df['lembur_jam'].sum()} jam"
    )

    # ===============================
    # REKAP BULANAN
    # ===============================
    st.subheader("📅 Rekap Bulanan per Karyawan")
    rekap = rekap_bulanan(df)
    st.dataframe(rekap, use_container_width=True)

    # ===============================
    # SLIP GAJI
    # ===============================
    st.subheader("🧾 Slip Gaji")

    selected = st.selectbox(
        "Pilih Karyawan",
        rekap["nama"]
    )

    if st.button("Generate Slip Gaji"):
        row = rekap[rekap["nama"] == selected].iloc[0]

        slip_data = {
            "Nama": row["nama"],
            "Total Hadir": row["total_hadir"],
            "Total Telat": row["total_telat"],
            "Total Potongan": f"Rp {row['total_potongan']:,}",
            "Total Lembur (Jam)": row["total_lembur_jam"]
        }

        tmp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )
        generate_slip_gaji(slip_data, tmp.name)

        with open(tmp.name, "rb") as f:
            st.download_button(
                "⬇️ Download Slip Gaji PDF",
                f,
                file_name=f"slip_gaji_{selected}.pdf"
            )

    # ===============================
    # DOWNLOAD EXCEL
    # ===============================
    st.download_button(
        "⬇️ Download Rekap Absensi (Excel)",
        data=df.to_excel(index=False),
        file_name="rekap_absensi.xlsx"
    )

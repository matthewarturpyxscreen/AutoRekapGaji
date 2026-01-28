import streamlit as st
import pandas as pd
import tempfile
import io
from datetime import datetime

from parser_griyatekno import parse_griyatekno_log
from payroll import hitung_status
from rekap import rekap_bulanan
from slip_gaji import generate_slip_gaji

# =========================
# CONFIG
# =========================
st.set_page_config("Sistem Absen & Gaji", layout="wide")
st.title("📊 Sistem Absensi & Payroll")

uploaded_file = st.file_uploader(
    "📂 Upload File Excel Fingerprint",
    type=["xls", "xlsx"]
)

if uploaded_file:
    # =========================
    # PARSE & HITUNG
    # =========================
    df = parse_griyatekno_log(uploaded_file)

    statuses = df.apply(hitung_status, axis=1, result_type="expand")
    df["status"], df["potongan"], df["lembur_jam"] = (
        statuses[0],
        statuses[1],
        statuses[2],
    )

    # =========================
    # TAMPILAN DATA
    # =========================
    st.subheader("📋 Data Absensi")
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("💸 Total Potongan", f"Rp {df['potongan'].sum():,.0f}")
    col2.metric("⏱️ Total Jam Lembur", f"{df['lembur_jam'].sum()} jam")

    # =========================
    # REKAP BULANAN
    # =========================
    st.subheader("📅 Rekap Bulanan per Karyawan")
    rekap = rekap_bulanan(df)

    bulan_list = rekap["bulan"].unique()
    bulan_terpilih = st.selectbox("Pilih Bulan", bulan_list)

    rekap_filter = rekap[rekap["bulan"] == bulan_terpilih]


# =========================
# PILIH KARYAWAN
# =========================
selected = st.selectbox(
    "👤 Pilih Karyawan",
    rekap["nama"].unique()
)

# filter bulan berdasarkan karyawan
bulan_opsi = rekap[rekap["nama"] == selected]["bulan"].unique()

bulan = st.selectbox(
    "🗓️ Bulan",
    bulan_opsi
)

    # =========================
    # GENERATE SLIP
    # =========================
    if st.button("🧾 Generate Slip Gaji"):
        row = rekap[
            (rekap["nama"] == selected) &
            (rekap["bulan"] == bulan)
        ].iloc[0]

        slip_data = {
            "nama": row["nama"],
            "bulan": row["bulan"],
            "total_hadir": row["total_hadir"],
            "total_telat": row["total_telat"],
            "total_potongan": row["total_potongan"],
            "total_lembur_jam": row["total_lembur_jam"],
        }

        # =========================
        # PDF
        # =========================
        tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        generate_slip_gaji(slip_data, tmp_pdf.name)

        with open(tmp_pdf.name, "rb") as f:
            st.download_button(
                "⬇️ Download Slip Gaji (PDF)",
                data=f,
                file_name=f"Slip_Gaji_{selected}_{bulan}.pdf",
                mime="application/pdf"
            )

        # =========================
        # EXCEL (FIX ERROR)
        # =========================
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            "⬇️ Download Rekap Absensi (Excel)",
            data=buffer,
            file_name=f"Rekap_Absensi_{bulan}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

import streamlit as st
import pandas as pd
import tempfile
import io

from parser_griyatekno import parse_griyatekno_log
from payroll import hitung_status
from rekap import rekap_periode
from slip_gaji import generate_slip_gaji

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Sistem Absensi", layout="wide")
st.title("📊 Sistem Absensi")

uploaded_file = st.file_uploader(
    "📂 Upload File Excel Fingerprint",
    type=["xls", "xlsx"]
)

if uploaded_file is not None:
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
    # TAMPILAN DATA ABSENSI
    # =========================
    st.subheader("📋 Data Absensi")
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("💸 Total Potongan", f"Rp {df['potongan'].sum():,.0f}")
    col2.metric("⏱️ Total Jam Lembur", f"{df['lembur_jam'].sum():.2f} jam")

    # =========================
    # REKAP PERIODE
    # =========================
    st.subheader("📅 Rekap Absensi per Karyawan")
    rekap = rekap_periode(df)

    st.dataframe(rekap, use_container_width=True)

    # =========================
    # FILTER PERIODE & KARYAWAN
    # =========================
    periode_list = rekap["periode"].unique()
    periode = st.selectbox("🗓️ Pilih Periode", periode_list)

    nama_list = rekap[rekap["periode"] == periode]["nama"].unique()
    selected = st.selectbox("👤 Pilih Karyawan", nama_list)

    # =========================
    # GENERATE SLIP ABSENSI
    # =========================
    if st.button("🧾 Generate Slip Absensi"):
        data_filter = rekap[
            (rekap["nama"] == selected) &
            (rekap["periode"] == periode)
        ]

        if data_filter.empty:
            st.warning("Data tidak ditemukan.")
        else:
            row = data_filter.iloc[0]

            slip_data = {
                "nama": row["nama"],
                "periode": row["periode"],
                "total_hadir": row["total_hadir"],
                "total_telat": row["total_telat"],
                "total_potongan": row["total_potongan"],
                "total_lembur_jam": row["total_lembur_jam"],
            }

            tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            generate_slip_gaji(slip_data, tmp_pdf.name)

            with open(tmp_pdf.name, "rb") as f:
                st.download_button(
                    "⬇️ Download Slip Absensi (PDF)",
                    data=f,
                    file_name=f"Slip_Absensi_{selected}_{periode}.pdf",
                    mime="application/pdf"
                )

    # =========================
    # DOWNLOAD EXCEL REKAP
    # =========================
    buffer = io.BytesIO()
    rekap.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button(
        "⬇️ Download Rekap Absensi (Excel)",
        data=buffer,
        file_name=f"Rekap_Absensi_{periode}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

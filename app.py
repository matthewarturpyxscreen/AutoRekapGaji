import streamlit as st
import pandas as pd
import io

from parser_griyatekno import parse_griyatekno_log
from payroll import hitung_status
from rekap import rekap_bulanan
from slip_gaji import generate_slip_gaji

st.set_page_config("Sistem Absensi & Gaji", layout="wide")
st.title("📊 Sistem Absensi & Payroll")

GAJI_POKOK = 5_000_000

uploaded = st.file_uploader("Upload File Fingerprint", ["xls", "xlsx"])

if uploaded:
    df = parse_griyatekno_log(uploaded)

    df[["status", "potongan", "lembur_jam", "lembur_rp"]] = df.apply(
        hitung_status, axis=1, result_type="expand"
    )

    rekap = rekap_bulanan(df)

    st.subheader("📅 Rekap Bulanan per Karyawan")

    bulan_pilih = st.selectbox(
        "Pilih Bulan",
        sorted(rekap["bulan"].unique())
    )

    rekap_bulan = rekap[rekap["bulan"] == bulan_pilih]

    nama_pilih = st.selectbox(
        "Pilih Karyawan (ketik untuk cari)",
        sorted(rekap_bulan["nama"].unique())
    )

    row = rekap_bulan[rekap_bulan["nama"] == nama_pilih].iloc[0]

    gaji_bersih = (
        GAJI_POKOK
        - row["total_potongan"]
        + row["total_lembur_rp"]
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Hadir", row["total_hadir"])
    col2.metric("Telat", row["total_telat"])
    col3.metric("Lembur (Rp)", f"Rp {row['total_lembur_rp']:,}")
    col4.metric("Gaji Bersih", f"Rp {gaji_bersih:,}")

    if st.button("📄 Generate Slip Gaji"):
        slip = {
            "Nama": nama_pilih,
            "Bulan": bulan_pilih,
            "Gaji Pokok": f"Rp {GAJI_POKOK:,}",
            "Potongan": f"Rp {row['total_potongan']:,}",
            "Lembur": f"Rp {row['total_lembur_rp']:,}",
            "Gaji Bersih": f"Rp {gaji_bersih:,}",
        }

        pdf = generate_slip_gaji(slip)
        with open(pdf, "rb") as f:
            st.download_button(
                "⬇️ Download Slip Gaji (PDF)",
                f,
                file_name=f"Slip_Gaji_{nama_pilih}_{bulan_pilih}.pdf"
            )

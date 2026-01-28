import streamlit as st
import pandas as pd

from parser_griyatekno import parse_griyatekno_log
from payroll import hitung_status
from rekap import rekap_bulanan
from slip_gaji import generate_slip_gaji

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Sistem Absensi & Payroll",
    layout="wide"
)

st.title("📊 Sistem Absensi & Payroll")

GAJI_POKOK = 5_000_000

# =============================
# UPLOAD FILE
# =============================
uploaded = st.file_uploader(
    "📂 Upload File Fingerprint (Excel)",
    ["xls", "xlsx"]
)

if not uploaded:
    st.info("⬆️ Silakan upload file fingerprint terlebih dahulu")
    st.stop()

# =============================
# PARSE DATA
# =============================
df = parse_griyatekno_log(uploaded)

if df.empty:
    st.error("❌ Data kosong / format file tidak dikenali")
    st.stop()

# normalisasi nama (WAJIB biar match)
df["nama"] = df["nama"].astype(str).str.strip().str.upper()

# =============================
# HITUNG STATUS HARIAN
# =============================
df[["status", "potongan", "lembur_jam", "lembur_rp"]] = df.apply(
    hitung_status,
    axis=1,
    result_type="expand"
)

# =============================
# REKAP BULANAN
# =============================
rekap = rekap_bulanan(df)

if rekap.empty:
    st.error("❌ Rekap bulanan kosong")
    st.stop()

# =============================
# PILIH BULAN
# =============================
st.subheader("📅 Rekap Bulanan per Karyawan")

rekap["bulan_label"] = rekap["bulan"].dt.strftime("%B %Y")

bulan_pilih = st.selectbox(
    "Pilih Bulan",
    sorted(rekap["bulan_label"].unique())
)

rekap_bulan = rekap[rekap["bulan_label"] == bulan_pilih]

if rekap_bulan.empty:
    st.warning("⚠️ Tidak ada data di bulan ini")
    st.stop()

# =============================
# PILIH KARYAWAN (SEARCHABLE)
# =============================
nama_pilih = st.selectbox(
    "Pilih Karyawan (ketik untuk cari)",
    sorted(rekap_bulan["nama"].unique())
)

data_nama = rekap_bulan[rekap_bulan["nama"] == nama_pilih]

if data_nama.empty:
    st.warning("⚠️ Data karyawan tidak ditemukan")
    st.stop()

row = data_nama.iloc[0]

# =============================
# HITUNG GAJI
# =============================
gaji_bersih = (
    GAJI_POKOK
    - row["total_potongan"]
    + row["total_lembur_rp"]
)

# =============================
# DASHBOARD METRIC
# =============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("✅ Hadir", int(row["total_hadir"]))
col2.metric("⏰ Telat", int(row["total_telat"]))
col3.metric("💰 Lembur", f"Rp {int(row['total_lembur_rp']):,}")
col4.metric("💵 Gaji Bersih", f"Rp {int(gaji_bersih):,}")

# =============================
# SLIP GAJI
# =============================
st.divider()

if st.button("📄 Generate Slip Gaji", use_container_width=True):
    slip = {
        "Nama": nama_pilih,
        "Bulan": bulan_pilih,
        "Gaji Pokok": GAJI_POKOK,
        "Total Hadir": int(row["total_hadir"]),
        "Total Telat": int(row["total_telat"]),
        "Potongan": int(row["total_potongan"]),
        "Lembur (Rp)": int(row["total_lembur_rp"]),
        "Gaji Bersih": int(gaji_bersih),
    }

    pdf_path = generate_slip_gaji(slip)

    with open(pdf_path, "rb") as f:
        st.download_button(
            "⬇️ Download Slip Gaji (PDF)",
            f,
            file_name=f"Slip_Gaji_{nama_pilih}_{bulan_pilih}.pdf",
            mime="application/pdf"
        )

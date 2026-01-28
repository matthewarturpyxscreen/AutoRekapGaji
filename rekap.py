import pandas as pd

def rekap_bulanan(df):
    df = df.copy()

    # pastikan tanggal valid
    df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")

    # kolom bulan
    df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")

    # ===== PAKSA KOLOM NUMERIC (INI KUNCI FIX) =====
    for col in ["potongan", "lembur_jam", "lembur_rp"]:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # status harus string
    df["status"] = df["status"].astype(str)

    rekap = (
        df.groupby(["nama", "bulan"], as_index=False)
        .agg(
            total_hadir=("status", lambda x: (x == "HADIR").sum()),
            total_telat=("status", lambda x: (x == "TELAT").sum()),
            total_potongan=("potongan", "sum"),
            total_lembur_jam=("lembur_jam", "sum"),
            total_lembur_rp=("lembur_rp", "sum"),
        )
    )

    return rekap

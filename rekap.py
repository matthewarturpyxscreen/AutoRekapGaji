import pandas as pd

def rekap_periode(df):
    df = df.copy()

    df["periode"] = (
        df["periode_awal"].dt.strftime("%d %B %Y") +
        " – " +
        df["periode_akhir"].dt.strftime("%d %B %Y")
    )

    rekap = (
        df.groupby(["nama", "periode"])
        .agg(
            total_hadir=("status", lambda x: (x == "HADIR").sum()),
            total_telat=("status", lambda x: (x == "TELAT").sum()),
            total_potongan=("potongan", "sum"),
            total_lembur_jam=("lembur_jam", "sum"),
        )
        .reset_index()
    )

    return rekap

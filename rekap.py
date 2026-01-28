import pandas as pd

def rekap_bulanan(df):
    return df.groupby(["pin", "nama"]).agg(
        total_hadir=("status", lambda x: (x == "HADIR").sum()),
        total_telat=("status", lambda x: (x == "TELAT").sum()),
        total_potongan=("potongan", "sum"),
        total_lembur_jam=("lembur_jam", "sum")
    ).reset_index()

def rekap_bulanan(df):
    df = df.copy()

    # pastikan kolom tanggal ada
    df["tanggal"] = pd.to_datetime(df["tanggal"])

    # bikin kolom bulan
    df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")

    rekap = (
        df.groupby(["nama", "bulan"])
        .agg(
            total_hadir=("status", lambda x: (x == "HADIR").sum()),
            total_telat=("status", lambda x: (x == "TELAT").sum()),
            total_potongan=("potongan", "sum"),
            total_lembur_jam=("lembur_jam", "sum"),
        )
        .reset_index()
    )

    return rekap

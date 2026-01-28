import pandas as pd
import re
from datetime import datetime, time

def parse_jam(cell):
    if not isinstance(cell, str):
        return None

    match = re.search(r"(\d{1,2}):(\d{2})", cell)
    if not match:
        return None

    jam = int(match.group(1))
    menit = int(match.group(2))

    if 0 <= jam <= 23 and 0 <= menit <= 59:
        return time(jam, menit)

    return None


def parse_griyatekno_log(uploaded_file):
    df = pd.read_excel(uploaded_file, sheet_name="Log", header=None)

    data = []
    periode_awal = datetime(2025, 12, 21)

    current_nama = None
    current_hari = None

    for _, row in df.iterrows():
        row_list = row.tolist()

        # detect nama
        if "Nama :" in row_list:
            idx = row_list.index("Nama :")
            current_nama = row_list[idx + 1]

        # detect hari (AMAN)
        for cell in row_list:
            if isinstance(cell, (int, float)):
                if pd.notna(cell) and 1 <= int(cell) <= 31:
                    current_hari = int(cell)

        # detect jam (SUPER KEBAL)
        for cell in row_list:
            jam = parse_jam(cell)
            if jam is None:
                continue

            if current_nama is None or current_hari is None:
                continue

            tahun = periode_awal.year
            bulan = periode_awal.month
            if current_hari < periode_awal.day:
                bulan += 1
                if bulan == 13:
                    bulan = 1
                    tahun += 1

            tanggal = datetime(tahun, bulan, current_hari)

            data.append({
                "nama": current_nama,
                "tanggal": tanggal,
                "jam": jam
            })

    df_log = pd.DataFrame(data)

    df_log = (
        df_log.groupby(["nama", "tanggal"])
        .agg(
            jam_masuk=("jam", "min"),
            jam_pulang=("jam", "max")
        )
        .reset_index()
    )

    return df_log

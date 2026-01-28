import pandas as pd
import re
from datetime import datetime

def parse_griyatekno_log(file):
    df = pd.read_excel(file, sheet_name="Log", header=None)

    results = []
    current_user = None
    current_dates = []
    start_date = None
    end_date = None

    for _, row in df.iterrows():
        row_str = " ".join([str(x) for x in row if pd.notna(x)])

        # === DETEKSI PERIODE ===
        if "Periode" in row_str:
            start_date, end_date = parse_periode(row_str)

        # === HEADER USER ===
        elif "No :" in row_str and "Nama :" in row_str:
            pin = re.search(r"No\s*:\s*(\d+)", row_str)
            nama = re.search(r"Nama\s*:\s*(.+?)\s+Dept", row_str)

            if pin and nama:
                current_user = {
                    "pin": pin.group(1),
                    "nama": nama.group(1).strip()
                }

        # === BARIS HARI ===
        elif all(isinstance(x, (int, float)) for x in row if pd.notna(x)):
            current_dates = [int(x) for x in row if pd.notna(x)]

        # === JAM ABSEN ===
        elif current_user and current_dates and start_date:
            col_idx = 0
            for cell in row:
                if pd.notna(cell) and isinstance(cell, str):
                    times = cell.split("\n")
                    masuk = times[0]
                    pulang = times[1] if len(times) > 1 else None

                    day = current_dates[col_idx]

                    # 🔥 HITUNG TANGGAL REAL
                    tanggal = start_date.replace(day=day)
                    if tanggal < start_date:
                        tanggal = tanggal.replace(month=start_date.month + 1)
                        if tanggal.month == 13:
                            tanggal = tanggal.replace(month=1, year=tanggal.year + 1)

                    results.append({
                        "pin": current_user["pin"],
                        "nama": current_user["nama"],
                        "tanggal": tanggal,
                        "jam_masuk": masuk,
                        "jam_pulang": pulang
                    })
                col_idx += 1

    return pd.DataFrame(results)


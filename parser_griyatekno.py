import pandas as pd
import re
from datetime import datetime

def parse_periode(text):
    """
    Contoh:
    Periode : 2025/12/21 ~ 01/20 ( PYXSCREEN )
    """
    m = re.search(r"(\d{4})/(\d{2})/(\d{2})\s*~\s*(\d{2})/(\d{2})", text)
    if not m:
        return None, None

    start_year = int(m.group(1))
    start_month = int(m.group(2))
    start_day = int(m.group(3))

    end_month = int(m.group(4))
    end_day = int(m.group(5))

    end_year = start_year + 1 if end_month < start_month else start_year

    start_date = datetime(start_year, start_month, start_day)
    end_date = datetime(end_year, end_month, end_day)

    return start_date, end_date

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

                    tanggal = start_date.replace(day=day)
                    if tanggal < start_date:
                        month = start_date.month + 1
                        year = start_date.year
                        if month == 13:
                            month = 1
                            year += 1
                        tanggal = tanggal.replace(month=month, year=year)

                    results.append({
                        "pin": current_user["pin"],
                        "nama": current_user["nama"],
                        "tanggal": tanggal,
                        "jam_masuk": masuk,
                        "jam_pulang": pulang
                    })
                col_idx += 1

    return pd.DataFrame(results)

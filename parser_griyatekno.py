import pandas as pd
from datetime import datetime, time

def parse_griyatekno_log(uploaded_file):
    xls = pd.ExcelFile(uploaded_file)
    rows = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)

        nama = None
        tanggal = None

        for _, row in df.iterrows():
            for cell in row:
                # =====================
                # NAMA
                # =====================
                if isinstance(cell, str) and cell.isupper() and len(cell) > 3:
                    nama = cell.strip()
                    continue

                # =====================
                # TANGGAL (1–31)
                # =====================
                if isinstance(cell, (int, float)) and 1 <= cell <= 31:
                    tanggal = int(cell)
                    continue

                # =====================
                # JAM
                # =====================
                if isinstance(cell, str) and ":" in cell:
                    try:
                        jam = datetime.strptime(cell.strip(), "%H:%M").time()
                    except:
                        continue

                    if nama and tanggal:
                        rows.append({
                            "nama": nama,
                            "tanggal": tanggal,
                            "jam": jam
                        })

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # tanggal final → pakai BULAN & TAHUN FILE
    today = datetime.today()
    df["tanggal"] = pd.to_datetime(
        df["tanggal"].astype(str)
        + f"-{today.month}-{today.year}",
        format="%d-%m-%Y"
    )

    return df

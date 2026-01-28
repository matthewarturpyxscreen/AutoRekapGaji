from datetime import datetime
from shifts import get_shift

POTONGAN_TELAT = 50000

def to_time(t):
    return datetime.strptime(t, "%H:%M").time() if t else None

def hitung_status(row):
    shift = get_shift(row.get("shift", "SHIFT_PAGI"))

    masuk = to_time(row["jam_masuk"])
    pulang = to_time(row["jam_pulang"])

    status = "HADIR"
    potongan = 0
    lembur_jam = 0

    if not masuk:
        return "ALFA", POTONGAN_TELAT, 0

    if masuk > shift["batas_telat"]:
        status = "TELAT"
        potongan = POTONGAN_TELAT

    if pulang and pulang >= shift["lembur_mulai"]:
        lembur_jam = (
            datetime.combine(datetime.today(), pulang) -
            datetime.combine(datetime.today(), shift["lembur_mulai"])
        ).seconds / 3600

    return status, potongan, round(lembur_jam, 2)

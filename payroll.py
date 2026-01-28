from datetime import datetime, time

JAM_MASUK = time(9, 0)
BATAS_TELAT = time(9, 30)
JAM_PULANG = time(17, 0)
ISTIRAHAT_START = time(12, 0)
ISTIRAHAT_END = time(13, 0)
LEMBUR_START = time(18, 0)

POTONGAN_TELAT = 50000

def to_time(t):
    return datetime.strptime(t, "%H:%M").time() if t else None

def hitung_status(row):
    masuk = to_time(row["jam_masuk"])
    pulang = to_time(row["jam_pulang"])

    status = "HADIR"
    potongan = 0
    lembur_jam = 0

    if not masuk:
        status = "ALFA"
        potongan = POTONGAN_TELAT
        return status, potongan, lembur_jam

    # TELAT
    if masuk > BATAS_TELAT:
        status = "TELAT"
        potongan = POTONGAN_TELAT

    # LEMBUR
    if pulang and pulang >= LEMBUR_START:
        lembur_jam = (
            datetime.combine(datetime.today(), pulang)
            - datetime.combine(datetime.today(), LEMBUR_START)
        ).seconds / 3600

    return status, potongan, round(lembur_jam, 2)

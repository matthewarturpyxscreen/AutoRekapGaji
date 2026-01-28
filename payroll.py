from datetime import time

JAM_MASUK = time(9, 0)
BATAS_TELAT = time(9, 30)
JAM_PULANG = time(17, 0)
JAM_LEMBUR = time(18, 0)

POTONGAN_TELAT = 50_000
LEMBUR_PER_JAM = 25_000

def hitung_status(row):
    jam_masuk = row["jam_masuk"]
    jam_pulang = row["jam_pulang"]

    telat = jam_masuk > BATAS_TELAT
    potongan = POTONGAN_TELAT if telat else 0

    lembur_jam = 0
    lembur_rp = 0
    if jam_pulang >= JAM_LEMBUR:
        lembur_jam = jam_pulang.hour - 18
        lembur_rp = lembur_jam * LEMBUR_PER_JAM

    status = "TELAT" if telat else "HADIR"
    return status, potongan, lembur_jam, lembur_rp


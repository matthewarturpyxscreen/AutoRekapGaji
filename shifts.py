from datetime import time

SHIFTS = {
    "SHIFT_PAGI": {
        "masuk": time(9, 0),
        "batas_telat": time(9, 30),
        "pulang": time(17, 0),
        "lembur_mulai": time(18, 0)
    },
    "SHIFT_SIANG": {
        "masuk": time(13, 0),
        "batas_telat": time(13, 30),
        "pulang": time(21, 0),
        "lembur_mulai": time(22, 0)
    }
}

def get_shift(shift_name):
    return SHIFTS.get(shift_name, SHIFTS["SHIFT_PAGI"])

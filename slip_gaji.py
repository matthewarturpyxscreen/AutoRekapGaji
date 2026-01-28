from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_slip_gaji(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "SLIP GAJI KARYAWAN")

    y -= 40
    c.setFont("Helvetica", 11)
    for key, value in data.items():
        c.drawString(50, y, f"{key} : {value}")
        y -= 20

    c.save()

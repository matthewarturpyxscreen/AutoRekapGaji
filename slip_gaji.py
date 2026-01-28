from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER

def generate_slip_gaji(data, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    text_style = styles["Normal"]

    y = height - 2 * cm

    # =========================
    # TITLE
    # =========================
    title = Paragraph("SLIP GAJI KARYAWAN", title_style)
    title.wrap(width, height)
    title.drawOn(c, 0, y)
    y -= 2 * cm

    # =========================
    # ISI
    # =========================
    items = [
        ("Nama", data["nama"]),
        ("Bulan", data["bulan"]),
        ("Total Hadir", f'{data["total_hadir"]} hari'),
        ("Total Telat", f'{data["total_telat"]} hari'),
        ("Total Potongan", f'Rp {data["total_potongan"]:,}'),
        ("Total Lembur", f'{data["total_lembur_jam"]} jam'),
    ]

    for label, value in items:
        p = Paragraph(f"<b>{label}</b> : {value}", text_style)
        p.wrap(width - 4 * cm, height)
        p.drawOn(c, 2 * cm, y)
        y -= 1 * cm

    # =========================
    # FOOTER
    # =========================
    c.line(2 * cm, y - 1 * cm, width - 2 * cm, y - 1 * cm)
    c.drawString(2 * cm, y - 2 * cm, "HRD")
    c.drawRightString(width - 2 * cm, y - 2 * cm, "Karyawan")

    c.showPage()
    c.save()

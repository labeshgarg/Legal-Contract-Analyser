from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_report(filename: str, clauses: list, output_dir="uploads") -> str:
    output_path = os.path.join(output_dir, f"{filename}_report.pdf")
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    y = height - 50
    line_height = 14

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"📄 Contract Risk Report: {filename}")
    y -= 30

    for i, clause in enumerate(clauses):
        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Clause {i+1} — Type: {clause['type'].upper()} | Risk: {clause['risk_score']}")
        y -= line_height

        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Summary: {clause['summary']}")
        y -= line_height * 2

        c.drawString(50, y, "Original:")
        y -= line_height
        for line in clause['text'].split("\n"):
            c.drawString(60, y, line[:100])
            y -= line_height

        if clause.get("suggestion"):
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(50, y, "🔁 Suggested Redline:")
            y -= line_height
            for line in clause['suggestion'].split("\n"):
                c.drawString(60, y, line[:100])
                y -= line_height

        y -= 25  # gap between clauses

    c.save()
    return output_path

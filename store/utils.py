from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io


# This function takes an existing PDF file and "stamps" a
# watermark (buyer's name + phone) onto every page.
def add_watermark(input_path, output_path, watermark_text):

    # Step A: create a temporary one-page PDF containing just
    # the watermark text, using reportlab
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 10)
    c.setFillGray(0.5, 0.5)  # light gray so it doesn't block the content
    c.drawString(50, 20, watermark_text)
    c.save()
    buffer.seek(0)

    # Step B: load that watermark as a PDF "page" we can stamp with
    watermark_pdf = PdfReader(buffer)
    watermark_page = watermark_pdf.pages[0]

    # Step C: open the original mudhakkira PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Step D: merge the watermark onto every page of the original
    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    # Step E: save the final watermarked PDF to a new file
    with open(output_path, "wb") as f:
        writer.write(f)
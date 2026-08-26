import fitz  # PyMuPDF
from docx import Document


# -----------------------------------
# Extract text from PDF
# -----------------------------------
def extract_pdf_text(file_path):

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        page_text = page.get_text("text")
        text += page_text + "\n"

    pdf.close()

    # Remove extra blank spaces
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    # -----------------------------
    # Debugging (Temporary)
    # -----------------------------
    print("\n========== PDF TEXT ==========\n")
    print(text)
    print("\n==============================\n")

    return text


# -----------------------------------
# Extract text from DOCX
# -----------------------------------
def extract_docx_text(file_path):

    document = Document(file_path)

    text = ""

    for para in document.paragraphs:

        if para.text.strip():
            text += para.text.strip() + "\n"

    # -----------------------------
    # Debugging (Temporary)
    # -----------------------------
    print("\n========== DOCX TEXT ==========\n")
    print(text)
    print("\n===============================\n")

    return text
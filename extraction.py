# extraction.py
import re
import pdfplumber

def extract_pdf_text(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text

def preprocess_text(text):
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip() != ""]
    return "\n".join(cleaned_lines)

def extract_sections(text, markers=["Projects", "Education", "Skills", "Achievements"]):
    sections = {}
    pattern = r"^(?P<section>" + "|".join(markers) + r")\s*$"

    lines = text.splitlines()
    current_section = "Header"
    sections[current_section] = []

    for line in lines:
        if re.match(pattern, line.strip(), re.IGNORECASE):
            current_section = line.strip()
            sections[current_section] = []
        else:
            sections[current_section].append(line)

    for key in sections:
        sections[key] = "\n".join(sections[key])

    return sections

# You can also add additional functions like extract_header_details, extract_projects, etc.

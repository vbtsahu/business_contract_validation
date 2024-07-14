import os
from flask import Flask, request, render_template, redirect, url_for
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import spacy
import difflib

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Business contract template
template_text = """
BUSINESS CONTRACT

This Contract (the "Contract") is made and entered into on this [Date], by and between:

Party A:
Name: [Party A's Full Name]
Address: [Party A's Address]
Contact Information: [Party A's Contact Information]

AND

Party B:
Name: [Party B's Full Name]
Address: [Party B's Address]
Contact Information: [Party B's Contact Information]

WHEREAS, Party A requires [Description of Service], and Party B agrees to provide such services under the terms and conditions outlined herein. Party B agrees to deliver the following services: [Detailed Description of Services to be Provided]. Party A agrees to pay Party B [Description of Payment Terms, Amounts, and Schedule]. This Contract will commence on [Start Date] and will continue until [End Date], or until the services have been satisfactorily completed.

Both parties agree to maintain confidentiality regarding all information exchanged during the course of this contract. This Contract may be terminated by either party upon [Number] days written notice. In the event of termination, Party B shall be compensated for all services performed up to the date of termination. Each party agrees to indemnify and hold harmless the other party from any claims, liabilities, damages, and expenses arising out of or in connection with the performance of this Contract.

This Contract constitutes the entire agreement between the parties and supersedes all prior agreements, understandings, and representations. Amendments to this Contract may only be made in writing and signed by both parties. If any provision of this Contract is found to be invalid or unenforceable, the remaining provisions will continue in full force and effect. This Contract shall be governed by the laws of the State of [State Name]. All notices required hereunder shall be in writing and deemed given when delivered in person, by email, or by certified mail to the addresses provided above.

IN WITNESS WHEREOF, the parties hereto have executed this Contract as of the day and year first above written.

Party A:

[Party A's Full Name]

Party B:

[Party B's Full Name]
"""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        if filename.endswith('.pdf'):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            text = extract_text_from_pdf(file_path)
        
        else:
            return "Unsupported file format"

        important_contents = extract_important_contents(text)
        highlighted_contract = highlight_contract_terms(text)
        entities = extract_entities(text)
        return render_template('results.html', important_contents=important_contents, highlighted_contract=highlighted_contract, entities=entities)

    return render_template('upload.html')

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text



def extract_important_contents(contract_text):
    template_lines = template_text.splitlines()
    contract_lines = contract_text.splitlines()
    differ = difflib.Differ()
    diff = list(differ.compare(template_lines, contract_lines))

    highlighted_text = []
    for line in diff:
        if line.startswith("- "):
            highlighted_text.append(f'<span class="highlight-red">{line[2:]}</span>')
        elif line.startswith("+ "):
            highlighted_text.append(f'<span class="highlight-green">{line[2:]}</span>')
        else:
            highlighted_text.append(line[2:])

    return "\n".join(highlighted_text)

def highlight_contract_terms(contract_text):
    terms_to_highlight = ["party", "agreement", "confidentiality", "Party A", "Party B"]
    highlighted_text = contract_text

    for term in terms_to_highlight:
        highlighted_text = highlighted_text.replace(term, f'<span class="highlight-blue">{term}</span>')
        highlighted_text = highlighted_text.replace(term.capitalize(), f'<span class="highlight-blue">{term.capitalize()}</span>')

    return highlighted_text


def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

if __name__ == '__main__':
    app.run(debug=True)

# business_contract_validation
python -m venv venv

venv\Scripts\activate

pip install Flask PyMuPDF pillow pytesseract pdf2image spacy
python -m spacy download en_core_web_sm

pip freeze > requirements.txt

flask run

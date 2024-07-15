# business_contract_validation

We can run the project with the commands mentioned here and test with the pdf files given in uploads folder.

organize the files like this
business_contract_validation/
|
|--templates/
|  |--results.html
|  |--upload.html
|
|--app.py
|--requirements.txt
------------------------------

python -m venv venv

venv\Scripts\activate

pip install Flask PyMuPDF pillow pytesseract pdf2image spacy
python -m spacy download en_core_web_sm

pip freeze > requirements.txt

flask run

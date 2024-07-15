# business_contract_validation

We can run the project with the commands mentioned here and test with the pdf files given in uploads folder. And Can see the presentation and report of the project in documentations folder 

organize the files like this
business_contract_validation/templates/results.html
business_contract_validation/templates/upload.html
business_contract_validation/app.py
business_contract_validation/requirements.txt


python -m venv venv

venv\Scripts\activate

pip install Flask PyMuPDF pillow pytesseract pdf2image spacy
python -m spacy download en_core_web_sm

pip freeze > requirements.txt

flask run

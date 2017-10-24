from flask import Flask, jsonify, request
from flask.ext.api import status
from flask_cors import CORS
from io import BytesIO

from engine.pdf_parser import PdfParser
from rest.models import db, Document, Content
from rest.constants import DATABASE_URL, ADDED_SUCCESS, NO_EXIST_MSG, JsonField

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % DATABASE_URL
db.init_app(app)


@app.route("/documents", methods=['GET', 'POST'])
def documents_list():
    if request.method == 'POST':
        file = request.files['file']
        parser = PdfParser(BytesIO(file.read()))
        file_content = parser.extract_pdf()
        pages = len(file_content.keys())
        pages_content = []
        for page_number, content in file_content.items():
            pages_content.append(Content(page_number=page_number, content=content))
        doc = Document(filename=file.filename, pages=pages, contents=pages_content)
        db.session.add(doc)
        db.session.add_all(pages_content)
        db.session.commit()
        print(ADDED_SUCCESS % file.filename)
        return jsonify({JsonField.Document: doc.as_dict()}), status.HTTP_200_OK
    else:
        documents = Document.query.order_by(Document.id).all()
        documents = [elem.as_dict() for elem in documents]
        return jsonify({JsonField.Document: documents}), status.HTTP_200_OK


@app.route("/documents/<document_id>/<page_number>", methods=['GET'])
def get_page(document_id, page_number):
    page_content = Content.query.filter_by(document_id=document_id, page_number=page_number).first()
    if page_content is None:
        return jsonify({JsonField.Details: {JsonField.Content: NO_EXIST_MSG}}), status.HTTP_404_NOT_FOUND
    doc = Document.query.filter_by(id=document_id).first()
    details = page_content.as_dict()
    details['pages'] = doc.pages
    return jsonify({JsonField.Document: details}), status.HTTP_200_OK

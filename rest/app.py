from flask import Flask, jsonify, request
from flask_cors import CORS
from io import BytesIO
from engine.pdf_parser import PdfParser
from rest.models import db, Document, Content

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database/database.db"
db.init_app(app)


@app.route("/documents", methods=['GET'])
def get_documents():
    documents = Document.query.order_by(Document.id).all()
    documents = [elem.as_dict() for elem in documents]
    return jsonify({'documents': documents})


@app.route("/documents", methods=['POST'])
def upload_document():
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
    msg = "File %s added to the database" % file.filename
    return jsonify({'document': doc.as_dict()}), 201


@app.route("/documents/<document_id>/<page_number>", methods=['GET'])
def get_page(document_id, page_number):
    page_content = Content.query.filter_by(document_id=document_id, page_number=page_number).first()
    if page_content is None:
        return jsonify({'details': {'content': "Page does not exist"}}), 404
    doc = Document.query.filter_by(id=document_id).first()
    details = page_content.as_dict()
    details['pages'] = doc.pages
    return jsonify({'details': details})


if __name__ == '__main__':
    app.run(debug=True)
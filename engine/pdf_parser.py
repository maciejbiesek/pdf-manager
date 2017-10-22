from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTChar
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


class PdfParser(object):
    def __init__(self, file):
        self.file = file
        self.document = self.set_parser()

    def set_parser(self):
        parser = PDFParser(self.file)
        document = PDFDocument(parser)
        parser.set_document(document)
        return document

    def get_text_from_objects(self, layout, content=None):
        if content is None:
            content = []
        for lt_object in layout:
            if isinstance(lt_object, LTTextBox) or isinstance(lt_object, LTTextLine) or \
                    isinstance(lt_object, LTChar):
                content.append(lt_object.get_text())
            elif isinstance(lt_object, LTFigure):
                # LTFigure objects are containers for other LT* objects, so recurse through the children
                content.append(self.get_text_from_objects(lt_object, content))

        return "".join(content)

    def extract_pdf(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        text_pages = {}
        for i, page in enumerate(PDFPage.create_pages(self.document)):
            interpreter.process_page(page)
            layout = device.get_result()
            text_pages[i+1] = self.get_text_from_objects(layout)

        return text_pages

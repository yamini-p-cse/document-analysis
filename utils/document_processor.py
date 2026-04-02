import PyPDF2
from docx import Document
from typing import Optional
import os

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        except Exception as e:
            print(f"PDF Error: {str(e)}")
        return text.strip()
    
    @staticmethod
    def extract_text_from_docx(docx_path: str) -> str:
        """Extract text from DOCX"""
        text = ""
        try:
            doc = Document(docx_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n\n"
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += cell.text + "\n"
        except Exception as e:
            print(f"DOCX Error: {str(e)}")
        return text.strip()
    
    @staticmethod
    def extract_text(file_path: str) -> Optional[str]:
        """Extract text from ANY format"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return DocumentProcessor.extract_text_from_docx(file_path)
        elif ext in ['.txt', '.text']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except:
                return None
        elif ext.lower() in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            # OCR support (add later)
            print("OCR not implemented yet")
            return None
        
        print(f"Unsupported format: {ext}")
        return None
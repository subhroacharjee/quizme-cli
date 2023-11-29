from cgitb import text
import os

from PyPDF2 import PdfReader

def extract_text_from_pdf(path):
   text = ""
   with open(os.path.abspath(path), "rb") as pdf:
      pdf_reader = PdfReader(pdf)
      for page in pdf_reader.pages:
       text += page.extract_text()
      return text
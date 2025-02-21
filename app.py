import os
import pdfplumber
import docx
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def extract_text(file_path):
    """Extract text from PDF, DOCX, or TXT files."""
    if not os.path.exists(file_path):
        print("File not found.")
        return None
    
    file_extension = file_path.split('.')[-1].lower()
    text = ""
    
    if file_extension == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
    
    elif file_extension == 'docx':
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    
    elif file_extension == 'txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    
    else:
        print("Unsupported file format.")
        return None
    
    return text.strip()

def summarize_text(text, num_sentences=3):
    """Generate a summary using LSA (Latent Semantic Analysis)."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    
    return " ".join([str(sentence) for sentence in summary])

if __name__ == "__main__":
    file_path = input("Enter the file path: ")
    text = extract_text(file_path)
    
    if text:
        print("\nExtracted Text:\n", text[:500], "...")  
        summary = summarize_text(text)
        print("\nSummary:\n", summary)


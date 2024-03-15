import os
from PyPDF2 import PdfReader  # Importing PdfReader instead of PdfFileReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file using the updated PdfReader class.
    """
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:  # Iterating over pages directly
            text += page.extract_text()
        return text

def main():
    pdf_directory = '/Users/andy/Documents/Test PDFs (Python Input)'  
    output_directory = '/Users/andy/Documents/Test PDFs (Python Output)' 

    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            text = extract_text_from_pdf(pdf_path)
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.txt')
            
            with open(output_path, 'w') as output_file:
                output_file.write(text)
            print(f"Processed {filename}")

if __name__ == "__main__":
    main()

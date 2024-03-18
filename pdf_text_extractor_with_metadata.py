import csv
import os
import re
from PyPDF2 import PdfReader

def find_doi_in_text(text):
    """
    Searches the extracted text for DOIs using regular expressions and returns the first match found.
    """
    # Regular expression to match both DOI formats
    doi_regex = r'\b(?:https?://doi\.org/|doi:)(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b'
    match = re.search(doi_regex, text)
    return match.group(1) if match else 'Unknown'

def extract_and_standardize_metadata(pdf_path, text):
    """
    Extracts and standardizes metadata from a given PDF file and extracted text.
    """
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        raw_metadata = reader.metadata
        year = raw_metadata.get('/CreationDate', 'Unknown')[2:6] if '/CreationDate' in raw_metadata else 'Unknown'
        standardized_metadata = {
            'Title': raw_metadata.get('/Title', 'Unknown').replace('/', '-'),
            'Author': raw_metadata.get('/Author', 'Unknown').replace('/', '-'),
            'Year': year,
            'DOI': find_doi_in_text(text)
        }
        return standardized_metadata

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file.
    """
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() if page.extract_text() else ''
        return text

def generate_output_filename(serial_number, metadata):
    """
    Generates an output filename based on serial number, author, and year.
    """
    author = metadata['Author'].split(',')[0] if ',' in metadata['Author'] else metadata['Author']
    year = metadata['Year']
    return f"{serial_number}-{author}-{year}.txt"

def main():
    pdf_directory = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/1 pdf input'  # Update with the actual directory
    output_directory = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output'  # Update with the actual output directory
    csv_file_path = os.path.join(output_directory, 'metadata_summary.csv')

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Serial Number', 'Title', 'Author', 'Year', 'DOI', 'Original PDF Name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        serial_number = 1
        for pdf_file in os.listdir(pdf_directory):
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(pdf_directory, pdf_file)
                # Extract text
                text = extract_text_from_pdf(pdf_path)
                # Extract and standardize metadata, including DOI extraction from text
                metadata = extract_and_standardize_metadata(pdf_path, text)
                # Generate output filename
                output_filename = generate_output_filename(serial_number, metadata)
                output_path = os.path.join(output_directory, output_filename)
                with open(output_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)
                
                # Write metadata to CSV
                writer.writerow({
                    'Serial Number': serial_number,
                    'Title': metadata['Title'],
                    'Author': metadata['Author'],
                    'Year': metadata['Year'],
                    'DOI': metadata['DOI'],
                    'Original PDF Name': pdf_file
                })

                print(f'Processed: {pdf_file}')
                serial_number += 1

if __name__ == '__main__':
    main()

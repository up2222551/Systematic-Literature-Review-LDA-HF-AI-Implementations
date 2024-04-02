import csv
import os
import re
import logging
from PyPDF2 import PdfReader
from PyPDF2.generic import IndirectObject
from concurrent.futures import ProcessPoolExecutor, as_completed

# Setup basic logging
logging.basicConfig(level=logging.ERROR, filename='error_log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def find_doi_in_text(text):
    """
    Searches the extracted text for DOIs using regular expressions and returns the first match found.
    """
    # Regular expression to match both DOI formats
    doi_regex = r'\b(?:https?://doi\.org/|doi:)(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b'
    match = re.search(doi_regex, text)
    return match.group(1) if match else 'Unknown'

def get_metadata_value(value):
    """
    Extracts the actual value from the metadata field, handling IndirectObject instances.
    Converts everything to string and replaces slashes with dashes.
    """
    try:
        if isinstance(value, IndirectObject):
            value = value.get_object()
        return str(value).replace('/', '-') if value else 'Unknown'
    except Exception as e:
        print(f"Error extracting metadata value: {e}")
        return 'Unknown'

def extract_and_standardize_metadata(pdf_path, text):
    """
    Extracts and standardizes metadata from a given PDF file and extracted text,
    with added exception handling for more robust processing.
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            raw_metadata = reader.metadata
            standardized_metadata = {
                'Title': get_metadata_value(raw_metadata.get('/Title', 'Unknown')),
                'Author': get_metadata_value(raw_metadata.get('/Author', 'Unknown')),
                'Keywords': get_metadata_value(raw_metadata.get('/Keywords', 'Unknown')),
                'CreationDate': get_metadata_value(raw_metadata.get('/CreationDate', 'Unknown'))[2:10] if '/CreationDate' in raw_metadata else 'Unknown',
                'ModDate': get_metadata_value(raw_metadata.get('/ModDate', 'Unknown'))[2:10] if '/ModDate' in raw_metadata else 'Unknown',
                'Description': get_metadata_value(raw_metadata.get('/Subject', 'Unknown')),
                'Year': get_metadata_value(raw_metadata.get('/CreationDate', 'Unknown'))[2:6] if '/CreationDate' in raw_metadata else 'Unknown',
                'DOI': find_doi_in_text(text)
            }
            return standardized_metadata
    except Exception as e:
        print(f"Error extracting or standardizing metadata for {pdf_path}: {e}")
        # Return a dictionary with 'Unknown' values if an error occurs
        return {key: 'Unknown' for key in ['Title', 'Author', 'Keywords', 'CreationDate', 'ModDate', 'Description', 'Year', 'DOI']}

def extract_text_from_pdf(pdf_path, serial_number):
    """
    Attempts to extract text from a PDF file using PyPDF2. If an error occurs,
    the error is logged along with the serial number and filename.
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = ''.join([page.extract_text() or '' for page in reader.pages])
        return serial_number, pdf_path, text, None  # No error
    except Exception as e:
        logging.error(f"Error extracting text from {pdf_path} (Serial {serial_number}): {e}")
        return serial_number, pdf_path, "", str(e)  # Error encountered


def log_errors_to_csv(errors, csv_file_path='error_log.csv'):
    """
    Logs errors to a CSV file. Each error is associated with the serial number of the PDF and its filename.
    """
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Serial Number', 'PDF File', 'Error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for error in errors:
            writer.writerow({'Serial Number': error[0], 'PDF File': error[1], 'Error': error[2]})

def generate_output_filename(serial_number, metadata):
    """
    Generates an output filename based on serial number, author, and year.
    """
    author = metadata['Author'].split(',')[0] if ',' in metadata['Author'] else metadata['Author']
    year = metadata['Year']
    return f"{serial_number}-{author}-{year}.txt"

def process_pdf(pdf_path, serial_number, output_directory):
    try:
        text = extract_text_from_pdf(pdf_path, serial_number)[2]  # Adjusted to match the output format
        metadata = extract_and_standardize_metadata(pdf_path, text)
        output_filename = generate_output_filename(serial_number, metadata)
        output_path = os.path.join(output_directory, output_filename)

        # Save extracted text and metadata to an output file
        with open(output_path, 'w', encoding='utf-8') as text_file:
            metadata_text = f"Title: {metadata['Title']}\nAuthor: {metadata['Author']}\nYear: {metadata['Year']}\nDOI: {metadata['DOI']}\nKeywords: {metadata['Keywords']}\nCreated: {metadata['CreationDate']}\nModified: {metadata['ModDate']}"
            text_file.write(metadata_text + "\n\n---METADATA END---\n\n" + text)

        return serial_number, pdf_path, "Success", None
    except Exception as e:
        logging.error(f"Error processing PDF {pdf_path} (Serial {serial_number}): {e}")
        return serial_number, pdf_path, None, str(e)

def process_pdfs_in_parallel(pdf_directory, output_directory):
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    errors = []

    with ProcessPoolExecutor(max_workers=12) as executor:
        future_to_pdf = {
            executor.submit(process_pdf, os.path.join(pdf_directory, pdf_file), idx + 1, output_directory): (idx + 1, pdf_file)
            for idx, pdf_file in enumerate(pdf_files)
        }

        for future in as_completed(future_to_pdf):
            serial_number, pdf_file = future_to_pdf[future]
            result = future.result()
            if result[-1]:  # Check if there's an error (last element in result)
                errors.append((serial_number, pdf_file, result[-1]))

    return errors

def main():
    pdf_directory = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/1 pdf input'
    output_directory = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output'
    csv_file_path = os.path.join(output_directory, 'metadata_summary.csv')

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    errors = process_pdfs_in_parallel(pdf_directory, output_directory)

    # Collect metadata for CSV
    metadata_list = []
    for idx, pdf_file in enumerate(os.listdir(pdf_directory)):
        if pdf_file.endswith('.pdf'):
            serial_number = idx + 1
            pdf_path = os.path.join(pdf_directory, pdf_file)
            text = extract_text_from_pdf(pdf_path, serial_number)[2]
            metadata = extract_and_standardize_metadata(pdf_path, text)  # Pass both pdf_path and text
            original_pdf_name = pdf_file
            metadata_list.append({
                'Serial Number': serial_number,
                'Author': metadata['Author'],
                'Year': metadata['Year'],
                'DOI': metadata['DOI'],
                'Original PDF Name': original_pdf_name
           })

    # Write metadata to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Serial Number', 'Author', 'Year', 'DOI', 'Original PDF Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for metadata in metadata_list:
            writer.writerow(metadata)

    # Logging errors to CSV if any
    if errors:
        log_errors_to_csv(errors, os.path.join(output_directory, 'error_log.csv'))
        print("Errors logged to 'error_log.csv'")
    else:
            print("No errors encountered.")

if __name__ == "__main__":
    main()

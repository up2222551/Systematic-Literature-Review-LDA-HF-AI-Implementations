def extract_and_standardize_metadata(pdf_path, text):
    """
    Extracts and standardizes metadata from a given PDF file and extracted text.
    """
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        raw_metadata = reader.metadata
        standardized_metadata = {
            'Title': raw_metadata.get('/Title', 'Unknown').replace('/', '-'),
            'Author': raw_metadata.get('/Author', 'Unknown').replace('/', '-'),
            'Keywords': raw_metadata.get('/Keywords', 'Unknown').replace('/', '-'),
            'CreationDate': raw_metadata.get('/CreationDate', 'Unknown')[2:10] if '/CreationDate' in raw_metadata else 'Unknown',
            'ModDate': raw_metadata.get('/ModDate', 'Unknown')[2:10] if '/ModDate' in raw_metadata else 'Unknown',
            'Description': raw_metadata.get('/Subject', 'Unknown').replace('/', '-'),  # Assuming 'Description' is stored in '/Subject'
            'Year': raw_metadata.get('/CreationDate', 'Unknown')[2:6] if '/CreationDate' in raw_metadata else 'Unknown',
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
        # Updated field names to include additional metadata fields
        fieldnames = ['Serial Number', 'Title', 'Author', 'Year', 'DOI', 'Keywords', 'Created', 'Modified', 'Description', 'Original PDF Name']
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
                
   # Open the output file and write metadata, marker, and text
                with open(output_path, 'w', encoding='utf-8') as text_file:
                    metadata_text = f"Title: {metadata['Title']}\nAuthor: {metadata['Author']}\nYear: {metadata['Year']}\nDOI: {metadata['DOI']}\nKeywords: {metadata['Keywords']}\nCreated: {metadata['CreationDate']}\nModified: {metadata['ModDate']}"
                    text_file.write(metadata_text)
                    # Include the '---METADATA END---' marker
                    text_file.write("\n\n---METADATA END---\n\n")
                    text_file.write(text)
                
                # Write extended metadata to CSV, including 'Description'
                writer.writerow({
                    'Serial Number': serial_number,
                    'Title': metadata['Title'],
                    'Author': metadata['Author'],
                    'Year': metadata['Year'],
                    'DOI': metadata['DOI'],
                    'Keywords': metadata['Keywords'],
                    'Created': metadata['CreationDate'],
                    'Modified': metadata['ModDate'],
                    'Description': metadata['Description'],  # Only included in CSV
                    'Original PDF Name': pdf_file
                })

                print(f'Processed: {pdf_file}')
                serial_number += 1

if __name__ == '__main__':
    main()


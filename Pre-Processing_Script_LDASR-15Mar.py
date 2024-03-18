import os
import nltk
from nltk.corpus import words

# Download necessary NLTK data
nltk.download('words')

english_vocab = set(words.words())

def is_valid_word(word):
    return word in english_vocab

def merge_artefacts(text):
    words = text.split()
    i = 0
    while i < len(words) - 1:
        if is_valid_word(words[i] + words[i + 1]):
            words[i] = words[i] + words[i + 1]  # Merge the words
            del words[i + 1]  # Remove the next word as it's merged
        else:
            i += 1

    # Remove standalone non-words
    words = [word for word in words if is_valid_word(word)]

    return ' '.join(words)

def process_files(input_folder, output_folder):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    files_with_decode_errors = []  # List to keep track of files with decode errors

    # Process each file in the input directory
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        # Read the content of the file, ignoring undecodable characters
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

        # Check if any characters were ignored - this is a simple heuristic
        if '\ufffd' in text:
            files_with_decode_errors.append(filename)

        # Ignore metadata
        content_start = text.find('---METADATA END---')
        if content_start != -1:
            text = text[content_start + len('---METADATA END---'):].strip()

        # Process the text
        processed_text = merge_artefacts(text)

        # Save the processed text in the output directory
        output_file_path = os.path.join(output_folder, 'processed_' + filename)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(processed_text)
        print(f"Processed and saved: {output_file_path}")

    # Report any files that had undecodable characters
    if files_with_decode_errors:
        print("Files with undecodable characters (processed with ignored characters):")
        for file in files_with_decode_errors:
            print(file)
        
# Set your input and output folders
input_folder = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output'
output_folder = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/3 processed output'

process_files(input_folder, output_folder)

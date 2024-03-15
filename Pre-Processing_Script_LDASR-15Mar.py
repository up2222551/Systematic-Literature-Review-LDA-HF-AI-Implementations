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

    # Process each file in the input directory
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        # Read the content of the file
        with open(file_path, 'r') as file:
            text = file.read()

        # Process the text
        processed_text = merge_artefacts(text)

        # Save the processed text in the output directory
        output_file_path = os.path.join(output_folder, 'processed_' + filename)
        with open(output_file_path, 'w') as file:
            file.write(processed_text)
        print(f"Processed and saved: {output_file_path}")

# Set your input and output folders
input_folder = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output'
output_folder = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/3 processed output'

process_files(input_folder, output_folder)

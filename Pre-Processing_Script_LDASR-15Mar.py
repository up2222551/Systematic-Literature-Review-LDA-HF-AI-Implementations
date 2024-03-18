import os
import nltk
from nltk.corpus import words

# Ensure necessary NLTK data is downloaded
nltk.download('words', quiet=True)

english_vocab = set(words.words())

def is_valid_word(word):
    return word in english_vocab

def merge_artefacts(text):
    """
    Merge adjacent words if their concatenation forms a valid word,
    and remove standalone non-words.
    """
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
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if not filename.endswith('.txt'):  # Skip non-txt files
            continue
        
        file_path = os.path.join(input_folder, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()

            # Separate metadata and content
            metadata_end_index = text.find('---METADATA END---')
            if metadata_end_index != -1:
                metadata = text[:metadata_end_index + len('---METADATA END---')].strip()
                content = text[metadata_end_index + len('---METADATA END---'):].strip()
            else:
                metadata = ""
                content = text  # Process the entire text if no metadata end marker is found
            
            processed_content = merge_artefacts(content)

            # Reinsert metadata at the beginning of the processed content
            output_text = metadata + '\n\n' + processed_content if metadata else processed_content

            output_file_path = os.path.join(output_folder, filename)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(output_text)

            print(f"Processed and saved: {output_file_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Set your input and output folders
input_folder = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output'
output_folder = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/3 processed output'

process_files(input_folder, output_folder)

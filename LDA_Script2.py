import os
import csv
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
import numpy as np
import multiprocessing

# Adjusted function to load documents and ignore metadata
def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Split the content at the "---METADATA END---" marker and keep only the text after it
                _, _, text_after_metadata = content.partition('---METADATA END---')
                documents.append(text_after_metadata.strip())
    return documents

# Function for tokenizing and cleaning the dataset
def preprocess_texts(documents):
    stop_words = stopwords.words('english')
    return [[word for word in simple_preprocess(doc) if word not in stop_words] for doc in documents]

# Function to save document topic distributions to a CSV file
def save_topic_distributions(document_topics, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Document ID', 'Topic ID', 'Probability'])
        for doc_id, topics in enumerate(document_topics):
            for topic_id, prob in topics:
                writer.writerow([doc_id, topic_id, prob])

# Function to perform LDA analysis
def perform_lda_analysis(processed_texts):
    # Create Dictionary and Corpus needed for Topic Modeling
    dictionary = corpora.Dictionary(processed_texts)
    corpus = [dictionary.doc2bow(text) for text in processed_texts]

    # Parameters for LDA training
    min_topics = 2
    max_topics = 10
    step_size = 1
    coherence_values = []
    model_list = []

    # Training multiple LDA models and calculating the coherence score
    for num_topics in range(min_topics, max_topics, step_size):
        model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=dictionary,
                                                num_topics=num_topics,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=processed_texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    # Selecting the model with the highest coherence score
    optimal_model_index = np.argmax(coherence_values)
    optimal_model = model_list[optimal_model_index]
    optimal_num_topics = range(min_topics, max_topics, step_size)[optimal_model_index]

    print(f'Optimal Number of Topics: {optimal_num_topics}')
    print(f'Optimal Model\'s Coherence Score: {coherence_values[optimal_model_index]}')

    # To see the topics in the optimal model
    for idx, topic in optimal_model.print_topics(-1):
        print(f'Topic: {idx} \nWords: {topic}')

    # Compute the topic distribution for each document
    document_topics = optimal_model.get_document_topics(corpus, minimum_probability=0.0)

    # Save the topic distributions to a CSV file
    output_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution/document_topic_distributions.csv'  # Update this path
    save_topic_distributions(document_topics, output_path)
    print(f'Document topic distributions saved to {output_path}')

# Main execution
if __name__ == '__main__':
    # If you are on macOS, use the 'fork' start method
    multiprocessing.set_start_method('fork')

    # Load and preprocess the dataset
    folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/3 processed output'  # Update this path
    documents = load_documents(folder_path)
    processed_texts = preprocess_texts(documents)

    # Perform LDA Analysis
    perform_lda_analysis(processed_texts)

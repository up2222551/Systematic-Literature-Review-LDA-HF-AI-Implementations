import os
import csv
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from sklearn.model_selection import KFold
import numpy as np

def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                _, _, text_after_metadata = content.partition('---METADATA END---')
                documents.append((filename, text_after_metadata.strip()))  # Include filename here
    return documents

def preprocess_texts(documents):
    stop_words = stopwords.words('english')
    return [(doc[0], [word for word in simple_preprocess(doc[1]) if word not in stop_words]) for doc in documents]

def save_topic_distributions(document_topics, fold_number, output_folder):
    file_path = os.path.join(output_folder, f'topic_distributions_fold_{fold_number}.csv')
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Document ID', 'Topic ID', 'Probability'])
        for doc_id, (filename, topics) in enumerate(document_topics):  # Adjusted to include filename
            for topic_id, prob in topics:
                writer.writerow([filename, doc_id, topic_id, prob])

def save_topic_keywords(lda_model, output_folder, num_words):
    file_path = os.path.join(output_folder, 'topic_keywords.csv')
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Topic ID', 'Keywords'])
        for topic_id in range(lda_model.num_topics):
            topic_keywords = lda_model.show_topic(topic_id, topn=num_words)
            keywords = ", ".join([word for word, _ in topic_keywords])
            writer.writerow([topic_id, keywords])

def perform_lda_and_save_distributions(processed_texts, output_folder, num_topics=10, num_folds=5):
    kf = KFold(n_splits=num_folds, shuffle=True, random_state=42)
    coherence_scores = []

    for fold, (train_index, test_index) in enumerate(kf.split(processed_texts)):
     # Adjust how train_texts and test_texts are created from processed_texts
        train_texts = [processed_texts[i][1] for i in train_index]  # Extract texts for training
        test_texts = [processed_texts[i] for i in test_index]  # Keep full tuple for test (to preserve filenames)


        dictionary = corpora.Dictionary(train_texts)
        corpus = [dictionary.doc2bow(text) for text in train_texts]

        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                               id2word=dictionary,
                                               num_topics=num_topics,
                                               random_state=100,
                                               chunksize=100,
                                               passes=10,
                                               per_word_topics=True)

        # Evaluate model coherence
        test_corpus = [dictionary.doc2bow(text[1]) for text in test_texts]
        coherence_model = CoherenceModel(model=lda_model, texts=test_texts, dictionary=dictionary, coherence='c_v')
        coherence_scores.append(coherence_model.get_coherence())

        # Save document-topic distributions for the fold
        document_topics = [lda_model.get_document_topics(bow) for bow in test_corpus]
        save_topic_distributions(document_topics, fold + 1, output_folder)

    # Save topic keywords for the entire corpus
    save_topic_keywords(lda_model, output_folder, num_words=10)

    # Print and return the average coherence score
    average_coherence_score = np.mean(coherence_scores)
    print(f"Average Coherence Score: {average_coherence_score}")
    return average_coherence_score

if __name__ == '__main__':
    input_folder = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/3 processed output'  # Update this path to where your documents are located
    output_folder = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution'    # Update this path to where you want to save CSV files
    documents = load_documents(input_folder)
    processed_texts = preprocess_texts(documents)

    # Perform LDA and save distributions
    average_coherence = perform_lda_and_save_distributions(processed_texts, output_folder)

    # Optionally, you can save the average coherence score and any other summary statistics to a text or CSV file as well.
    summary_path = os.path.join(output_folder, 'lda_summary.csv')
    with open(summary_path, 'w', newline='', encoding='utf-8') as summary_file:
        writer = csv.writer(summary_file)
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Average Coherence Score', average_coherence])

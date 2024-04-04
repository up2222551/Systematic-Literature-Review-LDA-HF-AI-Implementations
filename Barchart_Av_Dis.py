import pandas as pd
import matplotlib.pyplot as plt

# Paths to your CSV files
fold_csv_files = ['/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution/topic_distributions_fold_1.csv', '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution/topic_distributions_fold_2.csv', '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution/topic_distributions_fold_3.csv', '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution/topic_distributions_fold_4.csv', '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution/topic_distributions_fold_5.csv']

# Topic titles based on the provided mapping
topic_titles = {
    0: "Process and System Evaluation",
    1: "Enhanced Data Analysis and Learning Models",
    2: "Organisation and Performance in AI systems",
    3: "Smart Data Management",
    4: "Algorithmic Problem Solving",
    5: "Cognitive Aspects of Human-AI Interaction",
    6: "Socio Environment Aspects of Health",
    7: "Human-Centred System Design",
    8: "Technology and Health Research",
    9: "Image Data Analysis"
}

# Load and aggregate the topic probabilities for each document across all folds
doc_topic_prob = pd.DataFrame()

for file in fold_csv_files:
    fold_df = pd.read_csv(file)
    # Normalize probabilities within each document to ensure they sum to 1 across topics
    fold_df['Normalized Probability'] = fold_df.groupby('Document ID')['Probability'].apply(lambda x: x / x.sum())
    doc_topic_prob = doc_topic_prob.append(fold_df)

# Calculate the mean probability for each document-topic pair
mean_prob = doc_topic_prob.groupby(['Document ID', 'Topic ID'])['Normalized Probability'].mean().reset_index()

# Determine the dominant topic for each document
dominant_topics = mean_prob.loc[mean_prob.groupby('Document ID')['Normalized Probability'].idxmax()]

# Count how many documents belong to each topic
topic_counts = dominant_topics['Topic ID'].value_counts().reset_index()
topic_counts.columns = ['Topic ID', 'Document Count']

# Map topic IDs to titles
topic_counts['Topic Title'] = topic_counts['Topic ID'].map(topic_titles)

# Sort by the number of documents per topic
topic_counts.sort_values('Document Count', ascending=False, inplace=True)

# Plotting
plt.figure(figsize=(12, 8))
plt.barh(topic_counts['Topic Title'], topic_counts['Document Count'], color='skyblue')
plt.xlabel('Number of Documents', fontsize=14)
plt.ylabel('Topics', fontsize=14)
plt.title('Topic Distribution Across All Documents', fontsize=16)
plt.tight_layout()
plt.show()

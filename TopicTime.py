import pandas as pd
import matplotlib.pyplot as plt
import os

# File paths
index_file_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output/metadata_summary.csv'
lda_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution'
output_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/6 topics over time'

# Ensure output directory exists
os.makedirs(output_folder_path, exist_ok=True)

# Read the index file
index_df = pd.read_csv(index_file_path)
index_df.rename(columns={'Serial Number': 'Document ID'}, inplace=True)

# Filter out rows from index_df where 'Year' is 'Unknown', '-26-', or 'know'
index_df = index_df[~index_df['Year'].isin(['Unknown', '-26-', 'know'])]

# Read and concatenate all LDA topic distribution files
lda_files = [f for f in os.listdir(lda_folder_path) if f.endswith('.csv') and 'lda_summary' not in f and 'topic_keywords' not in f]
lda_dfs = []
for file in lda_files:
    filepath = os.path.join(lda_folder_path, file)
    lda_df = pd.read_csv(filepath)
    lda_dfs.append(lda_df)
concatenated_lda_df = pd.concat(lda_dfs)

# Merge the LDA topic distributions with the index file on 'Document ID'
merged_df = pd.merge(concatenated_lda_df, index_df, how='left', on='Document ID')

# Group by 'Year' and 'Topic ID', then calculate the mean probability
grouped_df = merged_df.groupby(['Year', 'Topic ID'])['Probability'].mean().reset_index()

# Topic ID to Name mapping
topic_names = {
    0: 'Process and System Evaluation',
    1: 'Enhanced Data Analysis and Learning Models',
    2: 'Organisation and Performance in AI systems',
    3: 'Smart Data Management',
    4: 'Algorithmic Problem Solving',
    5: 'Cognitive Aspects of Human-AI Interaction',
    6: 'Socio Environment Aspects of Health',
    7: 'Human-Centred System Design',
    8: 'Technology and Health Research',
    9: 'Image Data Analysis'
}

# Rename 'Topic ID' values in 'grouped_df' with their corresponding topic names from 'topic_names'
grouped_df['Topic ID'] = grouped_df['Topic ID'].map(topic_names)

# Pivot the DataFrame for easier plotting, with years as rows and topics as columns
pivot_df = grouped_df.pivot(index='Year', columns='Topic ID', values='Probability')

# Plotting
plt.figure(figsize=(14, 9))
for column in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[column], marker='o', linestyle='-', label=column)
plt.xlabel('Year')
plt.ylabel('Average Topic Probability')
plt.title('Topic Prevalence Over Time')
plt.legend(title='Topic', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_folder_path, 'topics_over_time.png'))
plt.show()

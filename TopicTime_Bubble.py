import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Define file paths
index_file_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output/metadata_summary.csv'
lda_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution'
output_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/6 topics over time'

# Ensure the output directory exists
os.makedirs(output_folder_path, exist_ok=True)

# Read and preprocess data
index_df = pd.read_csv(index_file_path)
index_df.rename(columns={'Serial Number': 'Document ID'}, inplace=True)
index_df = index_df[~index_df['Year'].isin(['Unknown', '-26-', 'know'])]

lda_files = [f for f in os.listdir(lda_folder_path) if f.endswith('.csv') and 'lda_summary' not in f and 'topic_keywords' not in f]
lda_dfs = [pd.read_csv(os.path.join(lda_folder_path, file)) for file in lda_files]
concatenated_lda_df = pd.concat(lda_dfs)

merged_df = pd.merge(concatenated_lda_df, index_df, how='left', on='Document ID')
grouped_df = merged_df.groupby(['Year', 'Topic ID'])['Probability'].mean().reset_index()
articles_per_year = merged_df.groupby(['Year'])['Document ID'].nunique().reset_index().rename(columns={'Document ID': 'Articles'})

# Map Topic IDs to names
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
grouped_df['Topic Name'] = grouped_df['Topic ID'].map(topic_names)
grouped_df = pd.merge(grouped_df, articles_per_year, on='Year', how='left')

# Visualization
plt.figure(figsize=(14, 10))

# Normalize bubble sizes. Adjust these as needed.
max_size = 2000  # Maximum bubble size
min_size = 50  # Minimum bubble size
grouped_df['Normalized Articles'] = (grouped_df['Articles'] - grouped_df['Articles'].min()) / (grouped_df['Articles'].max() - grouped_df['Articles'].min())
grouped_df['Bubble Size'] = grouped_df['Normalized Articles'] * (max_size - min_size) + min_size

for topic_name in topic_names.values():
    subset = grouped_df[grouped_df['Topic Name'] == topic_name]
    plt.scatter(subset['Year'], subset['Probability'], s=subset['Bubble Size'], alpha=0.6, label=topic_name)

plt.xlabel('Year')
plt.ylabel('Average Topic Probability')
plt.title('Topic Prevalence Over Time (Bubble Size Represents Number of Articles)')
plt.legend(title='Topic', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_folder_path, 'adjusted_topics_over_time_bubble.png'))
plt.show()

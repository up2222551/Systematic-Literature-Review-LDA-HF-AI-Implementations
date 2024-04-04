import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Adjust these paths according to your file structure
index_file_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output/metadata_summary.csv'
lda_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution'
output_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/6 topics over time'

# Ensure the output directory exists
os.makedirs(output_folder_path, exist_ok=True)

# Reading and preprocessing the data
index_df = pd.read_csv(index_file_path)
index_df.rename(columns={'Serial Number': 'Document ID'}, inplace=True)
index_df = index_df[~index_df['Year'].isin(['Unknown', '-26-', 'know'])]

lda_files = [f for f in os.listdir(lda_folder_path) if f.endswith('.csv') and 'lda_summary' not in f and 'topic_keywords' not in f]
lda_dfs = [pd.read_csv(os.path.join(lda_folder_path, file)) for file in lda_files]
concatenated_lda_df = pd.concat(lda_dfs)

merged_df = pd.merge(concatenated_lda_df, index_df, how='left', on='Document ID')
grouped_df = merged_df.groupby(['Year', 'Topic ID'])['Probability'].mean().reset_index()
articles_per_year = merged_df.groupby(['Year'])['Document ID'].nunique().reset_index().rename(columns={'Document ID': 'Articles'})

# Ensure all topics are included and correctly mapped
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

# Merge the count of articles into the grouped DataFrame
grouped_df = pd.merge(grouped_df, articles_per_year, on='Year', how='left')

# Visualization
plt.figure(figsize=(14, 10))
colors = plt.cm.tab10(np.linspace(0, 1, len(topic_names)))

for (topic_id, topic) in topic_names.items():
    subset = grouped_df[grouped_df['Topic ID'] == topic_id]
    # Adjust the bubble size scaling here; you might want to tweak these values
    bubble_sizes = subset['Articles'] * 10 + 10  # Adding a base size to ensure visibility
    plt.scatter(subset['Year'], subset['Probability'], s=bubble_sizes, alpha=0.6, label=topic)

plt.xlabel('Year')
plt.ylabel('Average Topic Probability')
plt.title('Topic Prevalence Over Time (Bubble Size Represents Number of Articles)')
plt.legend(title='Topic', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_folder_path, 'topics_over_time_bubble.png'))
plt.show()

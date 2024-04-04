import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# File paths
index_file_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output/metadata_summary.csv'
lda_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution'
output_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/6 topics over time'

# Ensure output directory exists
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

# Count articles per year
articles_per_year = merged_df.groupby(['Year'])['Document ID'].nunique().reset_index()
articles_per_year.rename(columns={'Document ID': 'Articles'}, inplace=True)

# Map Topic IDs to names
topic_names = {
    0: 'Process and System Evaluation',
    1: 'Enhanced Data Analysis and Learning Models',
    # Add the rest of your topics here...
}
grouped_df['Topic Name'] = grouped_df['Topic ID'].map(topic_names)

# Merge the count of articles into the grouped_df
grouped_df = pd.merge(grouped_df, articles_per_year, on='Year', how='left')

# Visualization
plt.figure(figsize=(14, 10))

# Generate a colormap
colors = plt.cm.tab10(np.linspace(0, 1, len(topic_names)))

for (topic, color) in zip(topic_names.values(), colors):
    subset = grouped_df[grouped_df['Topic Name'] == topic]
    plt.scatter(subset['Year'], subset['Probability'], s=subset['Articles']*10, color=color, alpha=0.6, label=topic)

plt.xlabel('Year')
plt.ylabel('Average Topic Probability')
plt.title('Topic Prevalence Over Time (Bubble Size Represents Number of Articles)')
plt.legend(title='Topic', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_folder_path, 'topics_over_time_bubble.png'))
plt.show()

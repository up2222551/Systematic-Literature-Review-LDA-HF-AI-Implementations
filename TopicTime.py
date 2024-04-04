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
# Rename 'Serial Number' to 'Document ID' for consistency with the LDA files
index_df.rename(columns={'Serial Number': 'Document ID'}, inplace=True)

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

# Pivot the DataFrame for easier plotting, with years as rows and topics as columns
pivot_df = grouped_df.pivot(index='Year', columns='Topic ID', values='Probability')

# Plotting
plt.figure(figsize=(12, 8))
for column in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[column], marker='o', linestyle='-', label=f'Topic {column}')
plt.xlabel('Year')
plt.ylabel('Average Topic Probability')
plt.title('Topic Prevalence Over Time')
plt.legend(title='Topic ID', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_folder_path, 'topics_over_time.png'))
plt.show()

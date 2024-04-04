import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths adjustment
index_file_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/2 text output/metadata_summary.csv'
lda_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution'
output_folder_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/6 topics over time'

# Reading the index file, now assuming it has a 'Year' column
index_df = pd.read_csv(index_file_path)
index_df.rename(columns={'Serial Number': 'document_id'}, inplace=True)

# Read and concatenate LDA topic distribution files, ignoring lda_summary.csv and topic_keywords.csv
lda_files = [f for f in os.listdir(lda_folder_path) if f.endswith('.csv') and 'lda_summary' not in f and 'topic_keywords' not in f]
lda_dfs = [pd.read_csv(os.path.join(lda_folder_path, file)) for file in lda_files]
lda_df = pd.concat(lda_dfs)

# Merge the LDA distributions with the index file based on document_id
merged_df = pd.merge(lda_df, index_df, how='left', on='document_id')

# Aggregate data by 'Year' and 'Topic ID', then calculate mean probability
grouped_df = merged_df.groupby(['Year', 'Topic ID'])['Probability'].mean().reset_index()

# Pivot the data for plotting, with 'Year' as the index
pivot_df = grouped_df.pivot(index='Year', columns='Topic ID', values='Probability')

# Visualization
plt.figure(figsize=(12, 8))
for column in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[column], marker='o', label=f'Topic {column}')
plt.xlabel('Year')
plt.ylabel('Average Topic Probability')
plt.title('Topic Prevalence Over Time')
plt.legend()
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
plt.savefig(os.path.join(output_folder_path, 'topics_over_time.png'))  # Save the plot
plt.show()

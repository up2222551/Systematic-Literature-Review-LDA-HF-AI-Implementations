import pandas as pd
import os

# File paths
metadata_path = '/path/to/your/metadata_summary.csv'
topic_dist_folder = '/path/to/your/topic_distribution_folder'

# Read the metadata file
metadata_df = pd.read_csv(metadata_path)

# Rename 'Serial Number' to 'Document ID' to match topic distribution files
metadata_df.rename(columns={'Serial Number': 'Document ID'}, inplace=True)

# Prepare to read topic distribution files
topic_files = [f for f in os.listdir(topic_dist_folder) if f.endswith('.csv') and 'topic_distribution' in f]

# Read and concatenate all topic distribution files
topic_dfs = []
for file in topic_files:
    file_path = os.path.join(topic_dist_folder, file)
    topic_df = pd.read_csv(file_path)
    topic_dfs.append(topic_df)

all_topics_df = pd.concat(topic_dfs, ignore_index=True)

# Merge the metadata with topic distributions
merged_df = pd.merge(metadata_df, all_topics_df, on='Document ID', how='inner')

# Optionally, save this merged DataFrame for further analysis
output_path = os.path.join(topic_dist_folder, 'merged_topic_data.csv')
merged_df.to_csv(output_path, index=False)

print(f"Merged data saved to: {output_path}")

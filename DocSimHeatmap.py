import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import cosine

def load_topic_distributions(folder_path):
    dfs = []
    for filename in os.listdir(folder_path):
        if filename.startswith('topic_distributions_fold_') and filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            dfs.append(pd.read_csv(file_path))
    return pd.concat(dfs)

def compute_cosine_similarity_matrix(df):
    # Pivot the DataFrame to have documents as rows and topics as columns
    pivot_df = df.pivot_table(index='Document ID', columns='Topic ID', values='Probability', fill_value=0)
    
    # Compute the cosine similarity matrix
    cosine_sim_matrix = np.zeros((pivot_df.shape[0], pivot_df.shape[0]))
    
    for i in range(pivot_df.shape[0]):
        for j in range(pivot_df.shape[0]):
            cosine_sim_matrix[i, j] = 1 - cosine(pivot_df.iloc[i], pivot_df.iloc[j])
    
    return cosine_sim_matrix

def plot_heatmap(matrix):
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, cmap='viridis')
    plt.title('Document Similarity Heatmap')
    plt.xlabel('Document ID')
    plt.ylabel('Document ID')
    plt.show()

if __name__ == '__main__':
    output_folder = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution' # Update this path
    df = load_topic_distributions(output_folder)
    similarity_matrix = compute_cosine_similarity_matrix(df)
    plot_heatmap(similarity_matrix)

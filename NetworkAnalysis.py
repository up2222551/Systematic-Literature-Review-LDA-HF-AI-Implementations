import pandas as pd
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

# Load the merged topic data
merged_data_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/4 topic distribution/merged_topic_data.csv'
merged_df = pd.read_csv(merged_data_path)

# Calculate co-occurrence of topics within documents
co_occurrences = merged_df.groupby('Document ID')['Topic ID'].apply(lambda x: list(combinations(sorted(set(x)), 2))).reset_index(name='Pairs')
co_occurrences = co_occurrences.explode('Pairs').dropna()

# Count the frequency of each pair
co_occurrence_counts = co_occurrences['Pairs'].value_counts().reset_index()
co_occurrence_counts.columns = ['Topic Pair', 'Weight']

# Split the topic pairs for clarity
co_occurrence_counts[['Topic 1', 'Topic 2']] = pd.DataFrame(co_occurrence_counts['Topic Pair'].tolist(), index=co_occurrence_counts.index)
co_occurrence_counts.drop('Topic Pair', axis=1, inplace=True)

# Exporting co-occurrence data to CSV
co_occurrence_csv_path = '/Users/andy/Documents/Systemic Review LDA Analysis 2024/SLR-LDA-HF-AI/7 network analysis/networkanalysis.csv'
co_occurrence_counts.to_csv(co_occurrence_csv_path, index=False)
print(f"Co-occurrence data saved to: {co_occurrence_csv_path}")

# Create the network graph
G = nx.Graph()
for _, row in co_occurrence_counts.iterrows():
    G.add_edge(row['Topic 1'], row['Topic 2'], weight=row['Weight'])

# Draw the graph
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G, seed=42)  # For consistent layout
edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())

# Scale edge weights for visibility
weights = [w * 0.1 for w in weights]  # Adjust scaling factor as needed

nx.draw(G, pos, node_color='skyblue', with_labels=True, edgelist=edges, edge_color=weights, width=1, edge_cmap=plt.cm.Blues)
plt.title('Network Analysis of Topic Co-Occurrence')
plt.show()

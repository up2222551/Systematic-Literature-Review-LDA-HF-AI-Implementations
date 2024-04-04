import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

# Assuming the merged data is saved as 'merged_topic_data.csv' in your topic distribution folder
merged_data_path = '/path/to/your/topic_distribution_folder/merged_topic_data.csv'
merged_df = pd.read_csv(merged_data_path)

# Step 1: Calculate Co-occurrence
# Create a DataFrame for topic pairs and their co-occurrence count
co_occurrence = pd.DataFrame(merged_df.groupby('Document ID')['Topic ID'].apply(lambda topics: list(combinations(sorted(set(topics)), 2)))).reset_index()
co_occurrence = co_occurrence.explode('Topic ID')
co_occurrence = co_occurrence.dropna().groupby('Topic ID').size().reset_index(name='Weight')

# Split the topic pairs back into separate columns
co_occurrence[['Topic 1', 'Topic 2']] = pd.DataFrame(co_occurrence['Topic ID'].tolist(), index=co_occurrence.index)

# Step 2: Create a Network Graph
G = nx.Graph()

# Add edges with weights
for index, row in co_occurrence.iterrows():
    G.add_edge(row['Topic 1'], row['Topic 2'], weight=row['Weight'])

# Step 3: Visualize the Graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=7)  # For consistent layout
edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())

nx.draw(G, pos, node_color='lightblue', with_labels=True, edgelist=edges, edge_color=weights, width=2.0, edge_cmap=plt.cm.Blues)
plt.title('Network Analysis of Topic Co-Occurrence')
plt.show()

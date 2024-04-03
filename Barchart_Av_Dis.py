import pandas as pd
import matplotlib.pyplot as plt

# Paths to your CSV files
fold_csv_files = ['path_to_fold1.csv', 'path_to_fold2.csv', 'path_to_fold3.csv', 'path_to_fold4.csv', 'path_to_fold5.csv']
keywords_csv = 'path_to_keywords.csv'

# Load and process each fold
topic_counts = {}

for file in fold_csv_files:
    df = pd.read_csv(file)
    # Assuming the topic with the highest probability is the dominant topic for each document
    dominant_topics = df.groupby('Document ID')['Probability'].idxmax()
    dominant_topic_ids = df.loc[dominant_topics, 'Topic ID']
    
    for topic_id in dominant_topic_ids:
        if topic_id not in topic_counts:
            topic_counts[topic_id] = 0
        topic_counts[topic_id] += 1

# Load the keywords for each topic
keywords_df = pd.read_csv(keywords_csv)
keywords_df.set_index('Topic ID', inplace=True)

# Create a new DataFrame for the bar chart data
bar_chart_data = pd.DataFrame(list(topic_counts.items()), columns=['Topic ID', 'Document Count']).set_index('Topic ID')
bar_chart_data['Keywords'] = keywords_df.loc[bar_chart_data.index]['Keywords']

# Sort by the number of documents per topic
bar_chart_data.sort_values('Document Count', ascending=False, inplace=True)

# Plotting
plt.figure(figsize=(12, 8))
plt.bar(bar_chart_data['Keywords'], bar_chart_data['Document Count'], color='skyblue')
plt.xlabel('Topics (Keywords)', fontsize=14)
plt.ylabel('Number of Documents', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.title('Topic Distribution Across All Documents', fontsize=16)
plt.tight_layout()
plt.show()

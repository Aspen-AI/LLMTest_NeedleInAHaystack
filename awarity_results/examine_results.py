import os
import json
import matplotlib.pyplot as plt
from collections import Counter

def process_json_files(directory_path):
    scores = []

    # Iterate over all files in the given directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            
            # Open and read each JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Extract the score and add it to the scores list
                score = data.get("score")
                if score is not None:
                    scores.append(score)
    
    return scores

def plot_histogram(scores):
    # Create a histogram of the scores with bins from 1 to 10
    bins = range(1, 12)  # 12 to include the value 11 to have the upper edge for the bin 10
    plt.hist(scores, bins=bins, edgecolor='black', align='left')

    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title('Histogram of Scores')
    plt.xticks(range(1, 11))  # Set x-axis ticks to be from 1 to 10
    plt.xlim(0.5, 10.5)  # Adjust x-axis limits to center the bins
    plt.show()

if __name__ == "__main__":
    directory_path = input("Enter the directory path containing JSON files: ")
    scores = process_json_files(directory_path)
    plot_histogram(scores)

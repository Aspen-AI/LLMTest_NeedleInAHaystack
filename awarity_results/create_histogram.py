import os
import json
import matplotlib.pyplot as plt
from collections import Counter
from statistics import mean

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

def plot_histogram(scores, title='Histogram of Scores'):
    # Create a histogram of the scores with bins from 1 to 10
    bins = range(1, 12)  # 12 to include the value 11 to have the upper edge for the bin 10
    plt.hist(scores, bins=bins, edgecolor='black', align='left')

    # Calculate mean and median
    mean_value = mean(scores)
    #median_value = median(scores)

    # # Add mean and median to the plot
    # plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value:.2f}')
    # plt.axvline(median_value, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_value:.2f}')

    # # Add text annotation for mean and median
    # plt.text(mean_value, plt.ylim()[1]*0.9, f'Mean: {mean_value:.2f}', color='red', ha='center')
    # plt.text(median_value, plt.ylim()[1]*0.8, f'Median: {median_value:.2f}', color='green', ha='center')

    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title(f'{title}\n(average={mean_value:.2f})')
    plt.xticks(range(1, 11))  # Set x-axis ticks to be from 1 to 10
    plt.xlim(0.5, 10.5)  # Adjust x-axis limits to center the bins
    plt.show()

if __name__ == "__main__":
    title = input("Enter the title (default: Histogram of Scores): ")
    title = "Histogram of Scores" if title == "" else title
    directory_path = input("Enter the directory path containing JSON files: ")
    scores = process_json_files(directory_path)
    plot_histogram(scores, title)

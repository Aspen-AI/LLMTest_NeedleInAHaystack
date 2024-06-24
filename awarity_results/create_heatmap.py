# NOTE: Code copied from ./viz/CreateVizFromLLMTesting.ipynb, and then modified

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import json
import glob

def create_heatmap(folder_path):
    # Using glob to find all json files in the directory
    json_files = glob.glob(f"{folder_path}/*.json")

    # List to hold the data
    data = []

    # Iterating through each file and extract the 3 columns we need
    for file in json_files:
        with open(file, 'r') as f:
            json_data = json.load(f)

            # Extracting the required fields
            document_depth = json_data.get("depth_percent", None)
            token_limit = json_data.get("context_length", None)
            score = json_data.get("score", None)
            data_to_append = {
                "Document Depth": document_depth,
                "Token Limit": token_limit,
                "Score": score
            }
            #print(data_to_append)
            # Appending to the list
            data.append(data_to_append)


    # Creating a DataFrame
    df = pd.DataFrame(data)

    print (df.head())
    print (f"You have {len(df)} rows")

    pivot_table = pd.pivot_table(df, values='Score', index=['Document Depth', 'Token Limit'], aggfunc='mean').reset_index() # This will aggregate
    pivot_table = pivot_table.pivot(index="Document Depth", columns="Token Limit", values="Score") # This will turn into a proper pivot
    #pivot_table.iloc[:5, :5]
    pivot_table.iloc[:,:]

    # Create a custom colormap. Go to https://coolors.co/ and pick cool colors
    cmap = LinearSegmentedColormap.from_list("custom_cmap", ["#F0496E", "#EBB839", "#0CD79F"])

    # Create the heatmap with better aesthetics
    plt.figure(figsize=(17.5, 8))  # Can adjust these dimensions as needed
    sns.heatmap(
        pivot_table,
        # annot=True,
        fmt="g",
        cmap=cmap,
        cbar_kws={'label': 'Score'}
    )

    # More aesthetics
    plt.title(f'{folder_path}')  # Adds a title
    plt.xlabel('Context Length')  # X-axis label
    plt.ylabel('Depth Percent')  # Y-axis label
    plt.xticks(rotation=45)  # Rotates the x-axis labels to prevent overlap
    plt.yticks(rotation=0)  # Ensures the y-axis labels are horizontal
    plt.tight_layout()  # Fits everything neatly into the figure area

    # Show the plot
    plt.show()

if __name__ == "__main__":
    directory_path = input("Enter the directory path containing JSON result files: ")
    create_heatmap(directory_path)

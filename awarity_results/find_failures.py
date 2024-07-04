import os
import json

if __name__ == "__main__":
    directory_path = input("Enter the directory path containing JSON files: ")
    
    # Iterate over all files in the given directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            
            # Open and read each JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Extract the score and add it to the scores list
                score = data.get("score")
                if score != 10:
                    print(f"{file_path} = {score}")

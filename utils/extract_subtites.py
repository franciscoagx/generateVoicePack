import os
import argparse
import csv
import json

# Function to read a subtitles.csv file and extract phrases
def read_subtitles_csv(file_path):
    phrases = set()  # Use a set to avoid duplicates
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) > 1:
                phrase = row[1].strip('"')  # Get the phrase and remove any surrounding quotes
                phrases.add(phrase)  # Add the phrase to the set
    return list(phrases)

# Recursive function to process directories and build the structure
def process_folders(path):
    structure = {}
    total_phrases = 0
    missing_subtitles = []

    # Walk through the directory and find 'subtitles.csv' files
    for root, dirs, files in os.walk(path):
        # Skip directories that start with 'radio_check_' or 'spotter_'
        dirs[:] = [d for d in dirs if not (d.startswith('radio_check_') or d.startswith('spotter_'))]

        relative_path = os.path.relpath(root, path)
        subdirs = relative_path.split(os.sep)

        # Search for subtitles.csv
        found_subtitles = False
        for file in files:
            if file == 'subtitles.csv':
                found_subtitles = True
                file_path = os.path.join(root, file)
                phrases = read_subtitles_csv(file_path)
                total_phrases += len(phrases)

                # Build the dictionary recursively
                current_node = structure
                for subdir in subdirs[:-1]:  # Exclude the last subdir for now
                    if subdir not in current_node:
                        current_node[subdir] = {}
                    current_node = current_node[subdir]

                # Assign the phrases directly to the last subdir level
                current_node[subdirs[-1]] = phrases

        # Only include paths with subdirectories and exclude base-level directories
        if not found_subtitles and len(subdirs) > 1:
            missing_subtitles.append(relative_path)

    return structure, total_phrases, missing_subtitles

# Main function to handle command-line arguments and execute the script
def main():
    parser = argparse.ArgumentParser(description="Process folder, find 'subtitles.csv' files, extract phrases, and save to JSON.")
    parser.add_argument('--folder', type=str, required=True, help='The folder to process')
    args = parser.parse_args()

    folder_path = args.folder

    # Get the folder name to use in the output file
    folder_name = os.path.basename(os.path.normpath(folder_path))

    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        print(f"The folder '{folder_path}' exists. Processing and extracting phrases...")

        # Process the folder and build the structure
        structure, total_phrases, missing_subtitles = process_folders(folder_path)

        # Save the structure to <folder_name>_subtitles.json
        output_file = f"{folder_name}_subtitles.json"
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(structure, jsonfile, indent=2, ensure_ascii=False)

        # Save the total phrases count and missing subtitles directories to missing_<folder_name>_subtitles.json
        missing_output_file = f"{folder_name}_subtitles_extra.json"
        missing_data = {
            "total_phrases": total_phrases,
            "missing_subtitles": missing_subtitles
        }
        with open(missing_output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(missing_data, jsonfile, indent=2, ensure_ascii=False)

        print(f"Processing complete. The files {output_file} and {missing_output_file} have been generated.")
    else:
        print(f"Error: The folder '{folder_path}' does not exist or is not a directory.")

if __name__ == '__main__':
    main()

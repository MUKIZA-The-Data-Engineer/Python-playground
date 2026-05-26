import os

# Set the path to your folder
folder_path = 'G:/.shortcut-targets-by-id/1AfDrHzItusIMCn9wq9_QO8GxGKOiiLqZ/Baho Coffee Company/Baho_coffee'

for filename in os.listdir(folder_path):
    if '_' in filename:
        # Create the new name
        new_name = filename.replace('_', ' ')
        # Full paths
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)
        
        os.rename(old_file, new_file)
        print(f"Renamed: {filename} -> {new_name}")
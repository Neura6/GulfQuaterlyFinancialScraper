import os
import shutil

def send_financial_reports(file = '', destination = 'financialReports' ):
    # List of files to move
    files = [file]

    source_folder = '.'  # Current directory; change if needed
    destination_folder = destination

    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    for file_name in files:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)

        # Check if the file exists before moving
        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"Moved {file_name} to {destination_folder}")
        else:
            print(f"File not found: {file_name}")

# Call the function

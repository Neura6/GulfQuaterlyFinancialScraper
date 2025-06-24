import os
import patoolib

def unzip(folder_path='pdfs'):
    """
    Extracts all archive files from a given folder.
    
    Supported formats: .zip, .rar, .7z, .tar, .tar.gz
    
    Args:
        folder_path (str): Path to the folder containing archive files.
    """
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.zip', '.rar', '.7z', '.tar', '.tar.gz')):
            archive_path = os.path.join(folder_path, filename)
            
            # Create output folder based on filename (without extension)
            folder_name = os.path.splitext(filename)[0]
            output_path = os.path.join(folder_path, folder_name)
            os.makedirs(output_path, exist_ok=True)

            try:
                print(f"Extracting {filename} to {output_path}...")
                patoolib.extract_archive(archive_path, outdir=output_path)
            except Exception as e:
                print(f"Failed to extract {filename}: {e}")

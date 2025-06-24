import os
import pandas as pd

def rename_pdfs_from_csv(csv_file_path='output_with_pdf_info.csv', pdf_folder_path='pdfs', suffix='_2025_Q1.pdf'):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Loop through each row in the CSV
    for index, row in df.iterrows():
        old_name = row['PDF_File']
        new_name = row['Stock'] + suffix

        old_file_path = os.path.join(pdf_folder_path, str(old_name))
        new_file_path = os.path.join(pdf_folder_path, new_name)

        # Check if the file exists before renaming
        if os.path.exists(old_file_path):
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {old_name} ➡ {new_name}')
        else:
            print(f'File not found: {old_name}')

# Example usage

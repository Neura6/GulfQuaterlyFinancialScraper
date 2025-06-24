import pandas as pd

def clean_csv(csv_file: str) -> pd.DataFrame:
    df = pd.read_csv(csv_file)

    # Function to check for valid PDF_URL
    def has_pdf(value):
        if pd.isna(value):  # handles NaN properly
            return False
        value = str(value).strip()
        return value != "" and value != "0"

    df['Has_Pdf'] = df['PDF_URL'].apply(has_pdf)

    # Drop 'PDF_File' if it exists
    if 'PDF_File' in df.columns:
        df = df.drop(columns=['PDF_File'])

    # Save back to the same file (preserves empty fields)
    df.to_csv(csv_file, index=False, na_rep='')


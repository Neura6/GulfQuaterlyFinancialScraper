import pandas as pd

def stripCSV(csv_path):
    """
    Reads a CSV file, keeps only the top 5 rows, and overwrites the original file.

    Parameters:
        csv_path (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: A DataFrame with only the top 5 rows.
    """
    df = pd.read_csv(csv_path)
    top5 = df.head(2)
    top5.to_csv(csv_path, index=False)
    return top5


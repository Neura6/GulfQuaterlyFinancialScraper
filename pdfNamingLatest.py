import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def download_pdfs_by_latest(csv_path, download_folder='pdfs', wait_time=20, suffix=''):
    # Read the CSV
    df = pd.read_csv(csv_path)
    df = df[df['URL'].notna() & df['URL'].str.strip().astype(bool)]

    # Create the target folder
    download_dir = os.path.abspath(download_folder)
    os.makedirs(download_dir, exist_ok=True)

    # Set up Chrome options to auto-download PDFs
    options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True,
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)

    # Launch browser
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    def get_latest_file(path):
        files = [os.path.join(path, f) for f in os.listdir(path)]
        files = [f for f in files if os.path.isfile(f)]
        if not files:
            return None
        latest_file = max(files, key=os.path.getctime)
        return latest_file

    try:
        for idx, row in df.iterrows():
            link = row['URL']
            name = row['Name']

            print(f"Downloading: {link} as {name}.pdf")
            driver.get(link)
            time.sleep(wait_time)  # Wait for download to start and complete

            # Rename the latest downloaded file
            latest_file = get_latest_file(download_dir)
            if latest_file and latest_file.endswith('.pdf'):
                new_name = os.path.join(download_dir, f"{name}{suffix}")
                if os.path.exists(new_name):
                    print(f"File {new_name} already exists, skipping rename.")
                else:
                    os.rename(latest_file, new_name)
                    print(f"Renamed {latest_file} to {new_name}")
            else:
                print(f"No PDF found to rename after downloading {link}")
    finally:
        driver.quit()
        print("Download complete.")

# Example usage:

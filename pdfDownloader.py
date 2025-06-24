import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def download_pdfs_from_csv(csv_path='extracted_urls_with_names.csv', output_folder='pdfs', wait_time=5):
    # Read the CSV
    df = pd.read_csv(csv_path)
    df = df[df['PDF_URL'].notna() & df['PDF_URL'].str.strip().astype(bool)]

    # Create the target folder
    os.makedirs(output_folder, exist_ok=True)

    # Set up Chrome options to auto-download PDFs in headless mode
    options = Options()
    prefs = {
        "download.default_directory": os.path.abspath(output_folder),
        "plugins.always_open_pdf_externally": True,
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless=new")  # Use "--headless=new" for better compatibility with downloads
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Stealth options
    options.add_argument("--headless=chrome")  # You can also try without headless if still blocked
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Set a real browser user agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36")

    # Additional arguments to reduce detection
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False) 

    # Launch browser
    driver = webdriver.Chrome(options=options)

    try:
        # Loop through links and download
        for link in df['PDF_URL']:
            print(f"Downloading: {link}")
            driver.get(link)
            time.sleep(wait_time)  # Wait for the download to complete; increase if needed
    finally:
        # Cleanup
        time.sleep(10)
        driver.quit()
        print("Download complete.")

# Example usage

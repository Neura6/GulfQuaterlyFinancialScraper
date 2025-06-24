import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

def oman_pdfs(input_csv = "omanURLs.csv" , output_csv = 'oman.csv', year = '2025', quarter = '1'):
    """
    Extract PDF links from web pages listed in a CSV file and add them to new columns in the CSV.

    Parameters:
    - input_csv: Path to the input CSV file with a 'URL' column.
    - output_csv: Path to save the updated CSV file.
    - date_string: Date string used in XPath to identify the relevant table row (default is '2025-03').
    """
    if quarter == '1':
        date_string = f"{year}-03-31"
    elif quarter == '2':
        date_string = f"{year}-06-30"
    elif quarter == '3':
        date_string = f"{year}-09-30"
    elif quarter == '4':
        date_string = f"{year}-12-31"       
    

    # Load CSV
    df = pd.read_csv(input_csv)

    # Prepare new columns
    df['PDF_URL'] = ''
    df['PDF_File'] = ''

    # Setup Selenium WebDriver (Chrome)
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    for index, row in df.iterrows():
        url = row['URL']
        try:
            driver.get(url)
            time.sleep(4)  # Wait for page to load

            pdf_href = None

            try:
                xpath = f"//td[contains(normalize-space(.), '{date_string}')]/following-sibling::td[1]//div//a[normalize-space(text())='English']"
                english_link = driver.find_element(By.XPATH, xpath)
                pdf_href = english_link.get_attribute('href')
            except NoSuchElementException:
                print(f"No matching element found for: {url}")
                continue

            if pdf_href:
                df.at[index, 'PDF_URL'] = pdf_href
                df.at[index, 'PDF_File'] = pdf_href.split('/')[-1]
                print(f"PDF found for {url}: {pdf_href}")
            else:
                print(f"No PDF link found for: {url}")

        except WebDriverException as e:
            print(f"WebDriver error for {url}: {e}")

    driver.quit()

    # Save updated DataFrame
    df.to_csv(output_csv, index=False)
    print(f"Updated data saved to {output_csv}")

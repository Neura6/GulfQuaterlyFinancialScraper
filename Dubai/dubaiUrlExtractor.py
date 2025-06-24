import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def dubai_urls(output_file='dubaiURLs.csv', delay=3):
    # Initialize WebDriver
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the URL
        url = 'https://www.dfm.ae/the-exchange/market-information/listed-securities/equities'
        driver.get(url)
        time.sleep(delay)

        # Find all data rows
        rows = driver.find_elements(By.CSS_SELECTOR, "div[data-index]")
        print(f"Found {len(rows)} rows.")

        names, stocks, hrefs = [], [], []

        # Extract data
        for row in rows:
            try:
                name_element = row.find_element(By.CSS_SELECTOR, "div span:nth-of-type(2)")
                name = name_element.text
                stock = row.find_element(By.CSS_SELECTOR, "div span:nth-of-type(1)").text
                href = row.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

                names.append(name)
                stocks.append(stock)
                hrefs.append(href)
            except Exception:
                continue

        # Create DataFrame and append to CSV
        df = pd.DataFrame({'Name': names, 'Stock': stocks, 'URL': hrefs})
        file_exists = os.path.isfile(output_file)
        df.to_csv(output_file, mode='a', header=not file_exists, index=False)
        print(f"{len(df)} rows appended to {output_file}")

    finally:
        # Always close the browser
        driver.quit()

# Example usage

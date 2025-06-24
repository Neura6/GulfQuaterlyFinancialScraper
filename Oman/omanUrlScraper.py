import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import os

def oman_urls(output_file='omanURLs.csv', delay=3):
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
        url = 'https://www.msx.om/companies.aspx'
        driver.get(url)
        time.sleep(delay)

        file_exists = os.path.isfile(output_file)
        page_count = 0
        max_pages = 8

        while page_count < max_pages:
            time.sleep(delay)

            # Find all data rows
            rows = driver.find_elements(By.CSS_SELECTOR, "tr[role='row']")
            print(f"Page {page_count + 1}: Found {len(rows)} rows.")

            names, stocks, hrefs = [], [], []

            for row in rows:
                try:
                    name_element = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(2) a")
                    name = name_element.text
                    stock = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(1) a").text
                    href = name_element.get_attribute('href')

                    names.append(name)
                    stocks.append(stock)
                    hrefs.append(href)
                except Exception:
                    continue

            df = pd.DataFrame({'Name': names, 'Stock': stocks, 'URL': hrefs})
            df.to_csv(output_file, mode='a', header=not file_exists, index=False)
            file_exists = True
            print(f"{len(df)} rows appended to {output_file}")

            page_count += 1

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "span.k-i-arrow-e")
                next_button.click()
            except (NoSuchElementException, ElementClickInterceptedException):
                print("No more pages or cannot click Next.")
                break

    finally:
        driver.quit()

    # Remove duplicates, keep first (original)
    if os.path.isfile(output_file):
        df_all = pd.read_csv(output_file)
        df_unique = df_all.drop_duplicates(subset='URL', keep='first')
        df_unique.to_csv(output_file, index=False)
        print(f"Duplicates removed. Final row count: {len(df_unique)}")

# Example usage

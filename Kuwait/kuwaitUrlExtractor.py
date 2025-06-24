import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def kuwait_urls(output_csv: str = 'extracted_data.csv', wait_time: int = 3):
    url = 'https://www.boursakuwait.com.kw/en/participants/participants/listed-companies'
    # Setup the WebDriver
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(wait_time)  # Wait for page to load

        # Find all table rows excluding the header
        rows = driver.find_elements(By.CSS_SELECTOR, "tr")

        # Lists to store extracted data
        names, stocks, hrefs = [], [], []

        # Loop through each row to extract required information
        for row in rows:
            try:
                name_element = row.find_element(By.CSS_SELECTOR, "td[type='link'] a")
                name = name_element.text
                stock = row.find_element(By.CSS_SELECTOR, "td[type='ticker']").text
                href = name_element.get_attribute('href')

                names.append(name)
                stocks.append(stock)
                hrefs.append(href)
            except Exception:
                continue  # Skip rows that don’t match the expected structure

        # Create a DataFrame
        df = pd.DataFrame({
            'Name': names,
            'Stock': stocks,
            'URL': hrefs
        })

        # Export to CSV
        df.to_csv(output_csv, index=False)
        print(f"{len(df)} rows saved to {output_csv}")
        return df

    finally:
        driver.quit()

# Example usage:

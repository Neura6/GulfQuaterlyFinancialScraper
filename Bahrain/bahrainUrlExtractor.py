import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def bahrain_urls(output_file='extracted_data.csv'):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    url = 'https://bahrainbourse.com/en/Products%20and%20Services/AssetClasses/Pages/Equities.aspx'
    driver.get(url)
    time.sleep(3)

    rows = driver.find_elements(By.XPATH, "//tr[not(contains(@class, 'tbl-data'))]")

    names, stocks, hrefs = [], [], []

    for row in rows:
        try:
            nameElement = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(2) a")
            name = nameElement.text
            stock = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(3)").text
            href = nameElement.get_attribute('href')

            names.append(name)
            stocks.append(stock)
            hrefs.append(href)
        except Exception:
            continue

    df = pd.DataFrame({'Name': names, 'Stock': stocks, 'URL': hrefs})
    df.to_csv(output_file, index=False)
    print(f"{len(df)} rows saved to {output_file}")
    driver.quit()
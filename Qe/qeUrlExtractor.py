import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import urllib.parse
from typing import Optional
import time


def qe_pdfs(output_csv: str = 'qeUrls.csv', quarter = '1', year = '2025') -> pd.DataFrame:
    def extract_and_decode_url(js_call: str) -> Optional[str]:
        if not js_call:
            return None
        match = re.search(r'checkDocumentAjax\(\s*["\']?(https%3A.*?)["\']?\s*\)', js_call)
        if match:
            encoded_url = match.group(1)
            decoded_url = urllib.parse.unquote(encoded_url)
            return decoded_url
        else:
            raise ValueError(f"Invalid input format: {js_call}")

    # Initialize the driver
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)




    try:
        url = 'https://www.qe.com.qa/financial-statements'
        driver.get(url)
        time.sleep(5)
        yearButton = driver.find_element(By.CSS_SELECTOR,'#yearsDropDown_PL_HP')
        yearButton.click()
        year2024 = driver.find_element(By.CSS_SELECTOR, f'[value="{year}"]')
        year2024.click()
        yearButton = driver.find_element(By.CSS_SELECTOR, "input.yearbtn[value='Submit']")
        yearButton.click()
        time.sleep(5)
        rows = driver.find_elements(By.CSS_SELECTOR, 'tr.remove_border_cust')
        print(f"Found {len(rows)} rows")

        data = []
        for row in rows:
            try:
                td_tag = row.find_elements(By.CSS_SELECTOR,'td')
                a_tag = td_tag[quarter-1].find_element(By.XPATH, f'.//a[@aria-label="Download Detailed FS Report"]')
                href = a_tag.get_attribute('onclick')
                if href:
                    decoded_url = extract_and_decode_url(href)
                else:
                    href = a_tag.get_attribute('href')
                    if href:
                        decoded_url = href
                name = row.find_element(By.CSS_SELECTOR, 'th').text
                data.append({'Name': name, 'URL': decoded_url})
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

        df = pd.DataFrame(data)
        df['Has_PDF'] = df['URL'].apply(lambda x: bool(x and x.strip()))
        df.to_csv(output_csv, index=False)

        print(f"{len(df)} entries saved to {output_csv}")
        return df

    finally:
        driver.quit()


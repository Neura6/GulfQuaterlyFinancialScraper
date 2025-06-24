import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

def kuwait_pdfs(input_csv: str, output_csv: str = 'extracted_data_with_pdf.csv', year: str = '2025', quarter: str = "1", wait_time: int = 2):
    # Load CSV
    df = pd.read_csv(input_csv)

    # Add new columns if not present
    df['PDF_URL'] = ''
    df['PDF_File'] = ''

    # Setup Selenium WebDriver (Chrome)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        for index, row in df.iterrows():
            url = row['URL']
            try:
                driver.get(url)
                time.sleep(wait_time)  # Allow page to load

                # Click on the "Financial Statement" link
                ca_button = driver.find_element(By.XPATH, '//a[text()="Financial Statement "]')
                ca_button.click()
                time.sleep(wait_time + 1)

                # Locate the PDF link for the specified year
                link = driver.find_element(
                    By.XPATH,
                    f".//td[normalize-space(text())='{year}']/following-sibling::td[{quarter}]//a[contains(@href, '.pdf')]"
                )
                pdf_href = link.get_attribute('href')
                print(pdf_href)

                if pdf_href:
                    df.at[index, 'PDF_URL'] = pdf_href
                    df.at[index, 'PDF_File'] = pdf_href.split('/')[-1]

            except NoSuchElementException:
                print(f"PDF or button not found for: {url}")
            except WebDriverException as e:
                print(f"WebDriver error for {url}: {e}")

    finally:
        driver.quit()

    # Save the updated DataFrame
    df.to_csv(output_csv, index=False)
    print(f"PDF links saved to {output_csv}")
    return df

# Example usage:

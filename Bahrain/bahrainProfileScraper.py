import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

def bahrain_pdfs(input_file='extracted_data.csv', output_file='extracted_data_with_pdf.csv',year='',quarter=''):
    changeYear = False

    if quarter == "1":
        date = f"31 March {year}"
        if year=="2024":
            changeYear=True
    elif quarter == "2":
        date = f"30 June {year}"
        if year=="2024":
            changeYear=True
    elif quarter == "3":
        date = f"30 September {year}"
        if year=="2024":
            changeYear=True
    elif quarter == "4":
        date = f"31 December {year}"
    else:
        date = "Invalid quarter"    

    df = pd.read_csv(input_file)
    df['PDF_URL'] = ''
    df['PDF_File'] = ''

    options = Options()
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
            time.sleep(2)

            caButton = driver.find_element(By.XPATH, '//a[text()="Corporate Actions"]')
            caButton.click()
            time.sleep(3)

            if changeYear:
                yearButton = driver.find_element(By.CSS_SELECTOR,'#ddlYear')
                yearButton.click()
                year2024 = driver.find_element(By.CSS_SELECTOR, '[value="2024"]')
                year2024.click()
                time.sleep(5)

            frButton = driver.find_element(By.XPATH, f'//a[starts-with(normalize-space(text()), "Financial Results for the period ended {date}")]')
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", frButton)
            time.sleep(2)
            frButton.click()
            time.sleep(5)

            pdf_element = driver.find_element(By.XPATH, '//a[contains(@href, ".pdf") and contains(@class, "download1")]')
            pdf_href = pdf_element.get_attribute('href')
            print(pdf_href)

            if pdf_href:
                df.at[index, 'PDF_URL'] = pdf_href
                df.at[index, 'PDF_File'] = pdf_href.split('/')[-1]
        except NoSuchElementException:
            print(f"PDF button not found for: {url}")
        except WebDriverException as e:
            print(f"WebDriver error for {url}: {e}")

    driver.quit()
    df.to_csv(output_file, index=False)
    print(f"Updated data saved to {output_file}")


# saudiProfileScraper.py
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options

def Saudi_profiles(input_csv='saudiURLs.csv', output_csv='saudi.csv', quarter = '1', year = '2025'):

    year = int(year)

    if quarter == "1":
        reportMonths = [f"{year}-05", f"{year}-06", f"{year}-07"]

    elif quarter == "2":
        reportMonths = [f"{year}-08", f"{year}-09", f"{year}-10"]

    elif quarter == "3":
        reportMonths = [f"{year}-11", f"{year}-12", f"{year+1}-01"]

    elif quarter == "4":
        reportMonths = [f"{year+1}-02", f"{year+1}-03", f"{year+1}-04"]

    else:
        reportMonths = []  # fallback for unexpected value

    options = Options()

    # Stealth options
    options.add_argument("--headless=chrome")  # You can also try without headless if still blocked
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Set a real browser user agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36")

    # Additional arguments to reduce detection
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    # Stealth script to remove WebDriver flags (run before any interaction)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        """
    })
    df_input = pd.read_csv(input_csv)
    urls = df_input['URL'].tolist()

    data = []
    save_interval = 10

    for idx, url in enumerate(urls, start=1):
        driver.get(url)
        time.sleep(2)

        try:
            li_element = driver.find_element(By.XPATH, '//li[normalize-space(.)="FINANCIAL STATEMENTS AND REPORTS"]')
            li_element.click()
            time.sleep(2)
        except (NoSuchElementException, ElementClickInterceptedException):
            print(f"Couldn't find/click LI on {url}")

        try:
            h3_text = driver.find_element(By.CSS_SELECTOR, 'section.saudiPage h3').text
        except NoSuchElementException:
            h3_text = ''

        try:
            name_text = driver.find_element(By.CSS_SELECTOR, 'div.price_name div.name').text
        except NoSuchElementException:
            name_text = ''

        pdf_href = ''
        try:
            a_element = driver.find_element(By.XPATH,f"//a[(contains(@href, '{reportMonths[0]}') or contains(@href, '{reportMonths[1]}') or contains(@href, '{reportMonths[2]}')) and contains(@href, '.pdf')]")
            pdf_href = a_element.get_attribute('href')
        except NoSuchElementException:
            pdf_href = ''

        data.append({
            'Company': h3_text,
            'Stock': name_text,
            'PDF_URL': pdf_href,
            'PDF_File': pdf_href.split('/')[-1],
            'Source_URL': url,
            
        })

        if idx % save_interval == 0:
            pd.DataFrame(data).to_csv(output_csv, index=False)
            print(f"Saved progress at {idx} URLs")

    pd.DataFrame(data).to_csv(output_csv, index=False)
    print(f"Scraped data from {len(data)} pages. Saved to {output_csv}")
    driver.quit()

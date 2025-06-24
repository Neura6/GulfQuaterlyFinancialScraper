# saudiUrlExtractor.py
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def Saudi_urls(output_csv='saudiURLs.csv'):
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

    url = 'https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch?locale=en'
    driver.get(url)

    rows = driver.find_elements(By.XPATH, '//tr[contains(@class, "even") or contains(@class, "odd")]')
    print(f"Found {len(rows)} rows")

    hrefs = []
    for row in rows:
        try:
            a_tag = row.find_element(By.CSS_SELECTOR, 'a.ellipsis')
            href = a_tag.get_attribute('href')
            if href:
                hrefs.append(href)
        except:
            continue

    df = pd.DataFrame({'URL': hrefs})
    df.to_csv(output_csv, index=False)
    print(f"{len(df)} URLs saved to {output_csv}")
    driver.quit()



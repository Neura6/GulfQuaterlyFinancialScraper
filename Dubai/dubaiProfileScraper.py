import pandas as pd
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def dubai_pdfs(input_file='dubaiURLs.csv', output_file='dubai.csv', delay=10, year = '2024', quarter = '4'):
    # Load the CSV
    df = pd.read_csv(input_file)

    # Prepare new columns
    df['PDF_URL'] = ''
    df['PDF_File'] = ''

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for index, row in df.iterrows():
            if quarter == "1":
                targetText = '1st QTR of'
            elif quarter == "2":
                targetText = '2nd QTR of'
            elif quarter == "3":
                targetText = '3rd QTR of'
            elif quarter == "4":
                targetText = 'year of'

            url = row['URL']
            print(f"Processing {url}")
            try:
                page.goto(url)
                time.sleep(delay)

                # Click the "Reports" link
                ca_button = page.locator('//a[text()=" Reports"]')
                ca_button.scroll_into_view_if_needed()
                time.sleep(2)
                ca_button.click()
                time.sleep(3)

                # Locate financial statement span
                target_span = page.locator(f"//span[text()='Financial statements for the {targetText} {year}']/ancestor::div[1]")
                target_span.scroll_into_view_if_needed()
                time.sleep(2)

                # Locate and click the button
                button = target_span.locator("xpath=following-sibling::div/div/button")
                button.click()
                time.sleep(2)

                # Get PDF link
                link = page.locator('//a[contains(@href, ".pdf")]')
                pdf_href = link.get_attribute('href')
                if pdf_href:
                    print(f"Found PDF: {pdf_href}")
                    df.at[index, 'PDF_URL'] = pdf_href
                    df.at[index, 'PDF_File'] = pdf_href.split('/')[-1]
            except PlaywrightTimeoutError:
                print(f"Timeout while processing: {url}")
            except Exception as e:
                print(f"Error for {url}: {e}")

        browser.close()

    # Save updated DataFrame
    df.to_csv(output_file, index=False)
    print(f"Updated data saved to {output_file}")

# Example usage:

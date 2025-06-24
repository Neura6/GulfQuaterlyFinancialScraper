import asyncio
import pandas as pd
import os
import random
from playwright.async_api import async_playwright
import time

def adx_pdfs(csv_input_path: str = 'Adx/adxUrls.csv', output_csv_path: str = "adx.csv", year='2024', quarter='1'):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]

    async def scrape_profile(browser, url):
        if quarter == '1':
            date_string = f"March 31,{year}"
        elif quarter == '2':
            date_string = f"June 30,{year}"
        elif quarter == '3':
            date_string = f"September 30,{year}"
        elif quarter == '4':
            date_string = f"December 31,{year}"    

        user_agent = random.choice(user_agents)
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()

        await page.goto(url)
        await page.wait_for_timeout(3000)

        company_name = ""
        stock_name = ""
        pdf_url = ""

        try:
            profile_cat = await page.query_selector("div.adx-profile_details-listedHeader-left-details__upper-content")
            if profile_cat:
                stock_element = await profile_cat.query_selector("h2")
                company_element = await profile_cat.query_selector("h4")
                stock_name = await stock_element.inner_text() if stock_element else "N/A"
                company_name = await company_element.inner_text() if company_element else "N/A"
                await page.get_by_text("Financial Reports").nth(0).click()
                time.sleep(5)



            found = False

            for attempt in range(5):  # Try up to 5 pages
                try:
                    pdf_row = await page.query_selector(f"//td[contains(text(), 'Financial Results for the Period Ended {date_string}')]/parent::tr")
                    if pdf_row:
                        fourth_td = await pdf_row.query_selector("td:nth-child(4) a")
                        pdf_url = await fourth_td.get_attribute("href")
                        print(pdf_url)
                        await page.wait_for_timeout(3000)
                        found = True
                        break
                except:
                    pass

                # If not found, click "Next page"
                next_button = await page.query_selector("a[aria-label='Next page']")
                if next_button:
                    await next_button.click()
                    time.sleep(5)
                    await page.wait_for_timeout(3000)
                else:
                    break

            await context.close()

            if not found:
                print(f"PDF not found after 5 attempts on {url}")
            


            return {
                "Company Name": company_name,
                "Stock": stock_name,
                "PDF_URL": pdf_url if found else "",
                'PDF_File': f"{pdf_url.split('/')[-1]}.pdf" if found else "N/A",
                "Source URL": url
            }

        except Exception as e:
            print(f"Error occurred while scraping {url}:", e)
            await context.close()
            return {
                "Company Name": "Error",
                "Stock": "Error",
                "PDF_URL": "Error",
                'PDF_File': 'Error',
                "Source URL": url
            }

    async def run_scraper():
        df = pd.read_csv(csv_input_path)
        urls = df['url'].dropna().tolist()
        results = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            for url in urls:
                print(f"Scraping: {url}")
                result = await scrape_profile(browser, url)
                results.append(result)

            await browser.close()

        result_df = pd.DataFrame(results)
        if os.path.isfile(output_csv_path):
            existing_df = pd.read_csv(output_csv_path)
            updated_df = pd.concat([existing_df, result_df], ignore_index=True)
        else:
            updated_df = result_df

        updated_df.to_csv(output_csv_path, index=False)
        print(f"Data written to {output_csv_path}")

    asyncio.run(run_scraper())


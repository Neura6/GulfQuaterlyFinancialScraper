import asyncio
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from playwright.async_api import async_playwright


# ==========================
# Playwright Scraper Function
# ==========================
async def scrape_profile(playwright, url):
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    await page.goto(url)
    await page.wait_for_timeout(3000)

    company_name = "N/A"
    stock_name = "N/A"
    pdf_url = ""

    try:
        profile_cat = await page.query_selector("div.adx-profile_details-listedHeader-left-details__upper-content")
        if profile_cat:
            stock_element = await profile_cat.query_selector("h2")
            company_element = await profile_cat.query_selector("h4")
            stock_name = await stock_element.inner_text() if stock_element else "N/A"
            company_name = await company_element.inner_text() if company_element else "N/A"

        # Try to get PDF URL if it exists
        try:
            pdf_span = await page.wait_for_selector("//span[contains(text(), 'Financial Results for the Period Ended March 31,2025')]", timeout=5000)
            await pdf_span.click()
            await page.wait_for_timeout(3000)
            pdf_object = await page.wait_for_selector("object.pdf-modal_file", timeout=5000)
            pdf_url = await pdf_object.get_attribute("data")
        except:
            pass  # No PDF, still save name/stock

    except Exception as e:
        print("Playwright scraping error:", e)

    await browser.close()
    return {
        "Company Name": company_name,
        "Stock Name": stock_name,
        "PDF URL": pdf_url
    }


# ==========================
# Combined Selenium + Playwright
# ==========================
async def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.adx.ae/main-market')
    main_tab = driver.current_window_handle

    time.sleep(5)  # wait for JS/data to load

    # ===============================
    # All Scroll Methods - One by One
    # ===============================

    # Method 1: Scroll container by setting scrollTop
    # try:
    #     scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div.rdt_TableBody')
    #     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    #     time.sleep(2)
    # except Exception as e:
    #     print("ScrollTop method failed:")

    # Method 2: window.scrollBy
    # try:
    #     for _ in range(10):
    #         driver.execute_script("window.scrollBy(0, 300);")
    #         driver.execute_script("window.dispatchEvent(new Event('scroll'))")
    #         time.sleep(0.5)
    # except Exception as e:
    #     print("window.scrollBy method failed:")

    # Method 3: scrollIntoView for each visible row
    # try:
    #     rows = driver.find_elements(By.CSS_SELECTOR, 'div.rdt_TableRow')
    #     for row in rows:
    #         driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", row)
    #         time.sleep(0.2)
    # except Exception as e:
    #     print("scrollIntoView method failed:")

    # Method 4: Smooth autoscroll loop (simulate human)
    try:
        driver.execute_script("""
            let scrollInterval = setInterval(() => {
                window.scrollBy(0, 150);
                window.dispatchEvent(new Event('scroll'));
                if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight) {
                    clearInterval(scrollInterval);
                }
            }, 300);
        """)
        time.sleep(5)  # allow time for loop to run
    except Exception as e:
        print("Smooth auto-scroll failed:")

    # Method 5: Explicit window.scrollTo bottom
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    except Exception as e:
        print("window.scrollTo method failed:")

    # Proceed with scraping
    all_data = []

    async with async_playwright() as p:
        scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div.rdt_TableBody')
        rows = driver.find_elements(By.CSS_SELECTOR, 'div.rdt_TableRow')
        print(f"Total rows found after scroll: {len(rows)}")

        for idx in range(len(rows)):
            try:
                rows = driver.find_elements(By.CSS_SELECTOR, 'div.rdt_TableRow')
                row = rows[idx]

                # Scroll to make sure this row is visible
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                    row
                )
                time.sleep(1)

                company = row.find_element(By.CSS_SELECTOR, 'div.datatable-symbollink a')
                company.click()
                time.sleep(2)

                profile_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View Full Company Profile')]"))
                )
                profile_button.click()

                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
                new_tab = [win for win in driver.window_handles if win != main_tab][0]
                driver.switch_to.window(new_tab)
                time.sleep(2)

                profile_url = driver.current_url
                scraped_data = await scrape_profile(p, profile_url)
                print(scraped_data)
                all_data.append(scraped_data)

                driver.close()
                driver.switch_to.window(main_tab)
                time.sleep(1)

                try:
                    close_btn = driver.find_element(By.CSS_SELECTOR, 'button.dragCloseButton i.icon')
                    close_btn.click()
                except:
                    pass

            except Exception as e:
                print(f"Error processing row {idx + 1}: {e}")
                driver.switch_to.window(main_tab)
                continue

    df = pd.DataFrame(all_data)
    df.to_csv('company_data.csv', index=False)
    print(f"Scraping complete. Total rows saved: {len(df)}")
    driver.quit()


# Run the async main
asyncio.run(main())

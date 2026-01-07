from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.page_load_strategy = "none"  # Fastest

# Initialize Chrome only once
service = Service(ChromeDriverManager().install())
service.creationflags = 0x08000000  # Windows speed-up
driver = webdriver.Chrome(service=service, options=chrome_options)


microwave_pages = [
    "https://www.amazon.in/gp/bestsellers/kitchen/1380072031",
    "https://www.amazon.in/gp/bestsellers/kitchen/1380072031/ref=zg_bs_pg_2_kitchen?ie=UTF8&pg=2"
]

# Prepare CSV file
with open("amazon_best_microwaves.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow([
        "Rank", "Microwave Name", "Rating", "Price", "Product Link", "Start Time", "End Time"
    ])

    current_rank = 1

    for index, page_url in enumerate(microwave_pages, start=1):
        print(f"Scraping Page {index}...")

        driver.execute_cdp_cmd("Page.enable", {})
        driver.execute_cdp_cmd("Network.enable", {})
        driver.get(page_url)

        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

     
        scroll_delay = 2
        prev_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_delay)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height

       
        soup = BeautifulSoup(driver.page_source, "lxml")
        microwave_items = soup.find_all("div", class_="p13n-sc-uncoverable-faceout")

        for item in microwave_items:
            start_time = datetime.now()

            # Name
            name_div = item.find("div", class_="p13n-sc-truncate-desktop-type2")
            if name_div:
                microwave_name = name_div.get_text(strip=True)
            else:
                img = item.find("img", alt=True)
                microwave_name = img["alt"].strip() if img else "N/A"

            # Rating
            rating_span = item.find("span", class_="a-icon-alt")
            rating = rating_span.get_text(strip=True) if rating_span else "N/A"

            # Price
            price_span = item.find("span", class_="p13n-sc-price")
            if not price_span:
                price_span = item.find("span", string=lambda t: t and "₹" in t)
            price = price_span.get_text(strip=True) if price_span else "N/A"

            # Product link
            link_tag = item.find("a", class_="a-link-normal")
            product_url = (
                "https://www.amazon.in" + link_tag.get("href")
                if link_tag else "N/A"
            )

            end_time = datetime.now()

            # Write to CSV
            csv_writer.writerow([
                current_rank, microwave_name, rating, price, product_url,
                start_time.strftime("%Y-%m-%d %H:%M:%S"),
                end_time.strftime("%Y-%m-%d %H:%M:%S")
            ])
            current_rank += 1

        print(f"Page {index} scraped successfully.")

print(" Done! Data saved to amazon_best_microwaves.csv")
driver.quit()
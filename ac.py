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
chrome_options.page_load_strategy = "none"

# Start Chrome driver
service = Service(ChromeDriverManager().install())
service.creationflags = 0x08000000
driver = webdriver.Chrome(service=service, options=chrome_options)

# AC Best Seller Pages (Page 1 & 2)
urls = [
    "https://www.amazon.in/gp/bestsellers/appliances/3474656031",
    "https://www.amazon.in/gp/bestsellers/appliances/3474656031/ref=zg_bs_pg_2_appliances?ie=UTF8&pg=2"
]

with open("amazon_best_acs.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["Rank", "AC Name", "Rating", "Price", "Product Link", "Start Time", "End Time"])

    rank = 1
    for index, url in enumerate(urls, start=1):
        print(f"Scraping Page {index}...")

        driver.get(url)

      
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, "lxml")
        items = soup.find_all("div", class_="p13n-sc-uncoverable-faceout")

        for item in items:
            start = datetime.now()

            # Name
            name_tag = item.find("div", class_="p13n-sc-truncate-desktop-type2")
            if name_tag:
                name = name_tag.get_text(strip=True)
            else:
                img = item.find("img", alt=True)
                name = img["alt"].strip() if img else "N/A"

            # Rating
            rating_tag = item.find("span", class_="a-icon-alt")
            rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

            # Price
            price_tag = item.find("span", class_="p13n-sc-price")
            if not price_tag:
                price_tag = item.find("span", string=lambda t: t and "₹" in t)
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            # Link
            link = item.find("a", class_="a-link-normal")
            product_url = "https://www.amazon.in" + link["href"] if link else "N/A"

            end = datetime.now()

            # Write to CSV
            writer.writerow([
                rank, name, rating, price, product_url,
                start.strftime("%Y-%m-%d %H:%M:%S"),
                end.strftime("%Y-%m-%d %H:%M:%S")
            ])
            rank += 1

        print(f"Page {index} scraped")

print(" All done! Data saved to 'amazon_best_acs.csv'")
driver.quit()
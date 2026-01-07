from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime  # Added to track time

# Set up Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize the Chrome driver just once
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

# URLs to scrape page 1 and 2
tv_pages = [
    "https://www.amazon.in/gp/bestsellers/electronics/1389396031",
    "https://www.amazon.in/gp/bestsellers/electronics/1389396031?pg=2"
]

with open("amazon_best_tvs.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow([
        "Rank", "TV Name", "Rating", "Price", "Product Link",
        "Start Time", "End Time"
    ]) 

    current_rank = 1

    for page_url in tv_pages:
        driver.get(page_url)
        time.sleep(3) 

       
        scroll_delay = 2
        prev_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_delay)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height

        # Parse the loaded page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "lxml")
        tv_items = soup.find_all("div", class_="p13n-sc-uncoverable-faceout")

        for item in tv_items:
            start_time = datetime.now()

            # TV name 
            name_div = item.find("div", class_="p13n-sc-truncate-desktop-type2")
            if name_div:
                tv_name = name_div.get_text(strip=True)
            else:
                img = item.find("img", alt=True)
                tv_name = img["alt"].strip() if img else "N/A"

            # Extract rating
            rating_span = item.find("span", class_="a-icon-alt")
            rating = rating_span.get_text(strip=True) if rating_span else "N/A"

            # Extract price
            price_span = item.find("span", class_="p13n-sc-price")
            if not price_span:
                price_span = item.find("span", string=lambda t: t and "₹" in t)
            price = price_span.get_text(strip=True) if price_span else "N/A"

            # Extract product link
            link_tag = item.find("a", class_="a-link-normal")
            product_url = (
                "https://www.amazon.in" + link_tag.get("href")
                if link_tag else "N/A"
            )

            end_time = datetime.now()

            csv_writer.writerow([
                current_rank, tv_name, rating, price, product_url,
                start_time.strftime("%Y-%m-%d %H:%M:%S"),
                end_time.strftime("%Y-%m-%d %H:%M:%S")
            ])
            current_rank += 1

print(" Data saved to amazon_best_tvs.csv")
driver.quit()
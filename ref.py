from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")  # Remove this line if you want to see the browser


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

urls = [
    "https://www.amazon.in/gp/bestsellers/appliances/1380369031",  # Page 1
    "https://www.amazon.in/gp/bestsellers/appliances/1380369031/ref=zg_bs_pg_2?ie=UTF8&pg=2"  # Page 2
]

filename = "amazon_best_refrigerators.csv"
csv_file = open(filename, "w", newline="", encoding="utf-8-sig")
writer = csv.writer(csv_file)
writer.writerow(["Rank", "Product Name", "Rating", "Price", "Product Link", "Scraped Time"])

def extract_price(soup_item):
    price_whole = soup_item.select_one(".p13n-sc-price")
    if price_whole:
        return price_whole.text.strip()
    return "N/A"

for url in urls:
    driver.get(url)
    time.sleep(3)

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    except Exception as e:
        print(f"Scrolling failed: {e}")

    soup = BeautifulSoup(driver.page_source, "lxml")
    items = soup.select("div.zg-grid-general-faceout")

    for idx, item in enumerate(items, 1):
        name_tag = item.select_one("div.p13n-sc-truncate-desktop-type2") or item.select_one("img")
        name = name_tag.get("alt").strip() if name_tag and name_tag.has_attr("alt") else name_tag.text.strip() if name_tag else "N/A"

        link_tag = item.select_one("a.a-link-normal")
        product_link = "https://www.amazon.in" + link_tag["href"] if link_tag and link_tag.has_attr("href") else "N/A"

        rating_tag = item.select_one("span.a-icon-alt")
        rating = rating_tag.text.strip() if rating_tag else "N/A"

        price = extract_price(item)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow([idx, name, rating, price, product_link, timestamp])

driver.quit()
csv_file.close()
print("Refrigerator data scraped and saved to amazon_best_refrigerators.csv")
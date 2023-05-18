import time
import csv
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Function to scrape product details from Amazon page
def scrape_details(driver):
    driver = webdriver.Chrome()
    # Scrape product title
    try:
        title = driver.find_element(By.ID,"productTitle").text.strip()
    except NoSuchElementException:
        title = "Not available"
    try:
        image_url = driver.find_element(By.ID,"landingImage").get_attribute("src")
    except NoSuchElementException:
        image_url = "Not available"
    try:
        price = driver.find_element(By.ID,"priceblock_ourprice").text.strip()
    except NoSuchElementException:
        price = "Not available"
    try:
        details = driver.find_element(By.ID,"productDescription").text.strip()
    except NoSuchElementException:
        details = "Not available"
    
    return {
        "title": title,
        "image_url": image_url,
        "price": price,
        "details": details
    }

# Read CSV file and create list of product URLs
urls = []
with open('amazon_products.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader) # skip header row
    for row in reader:
        url = f"https://www.amazon.{row[3]}/dp/{row[2]}"
        urls.append(url)

# Launch Selenium web driver
driver = webdriver.Chrome()

# Initialize list to store product details
product_details = []

# Loop through product URLs and scrape details
start_time = time.time()
for i, url in enumerate(urls):
    try:
        driver.get(url)
        time.sleep(1)
        product_details.append(scrape_details(driver))
        print(f"Product {i+1}: Scraped {url}")
    except:
        print(f"Product {i+1}: {url} not available")
    if (i+1) % 100 == 0:
        elapsed_time = time.time() - start_time
        print(f"\nCompleted {i+1} products in {elapsed_time:.2f} seconds\n")
        start_time = time.time()

# Close web driver
driver.quit()

# Convert list of dictionaries to JSON file
with open('product_details.json', 'w') as file:
    json.dump(product_details, file)

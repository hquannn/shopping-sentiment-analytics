import random
import pickle
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Function to load a random cookie set
def load_cookies_from_json(driver, json_file):
    with open(json_file, 'r') as file:
        cookies = json.load(file)
    driver.delete_all_cookies()  # Clear current cookies
    for cookie in cookies:
        # Remove 'sameSite' and 'storeId' if they're causing issues
        cookie.pop('sameSite', None)
        cookie.pop('storeId', None)
        driver.add_cookie(cookie)
    driver.refresh()


# Function to set random headers
def set_random_headers(driver):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
        "Referer": "https://shopee.vn",
    }
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {"headers": headers})

def scrape_shop_products(shop_link):
    driver.get(shop_link)
    time.sleep(5) 

    product_details = []

    while True:

        products = driver.find_elements(By.CLASS_NAME, 'shop-search-result-view')  # Adjust selector as needed

        for product in products:
            # Extract details for each product
            product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
            product_name = product.find_element(By.CLASS_NAME, 'whitespace-normal line-clamp-2 break-words min-h-[2.5rem] text-sm').text  # Adjust selector as needed
            product_price = product.find_element(By.CLASS_NAME, 'font-medium text-base/5 truncate').text  # Adjust selector as needed
            product_rating = product.find_element(By.CLASS_NAME, 'text-shopee-black87 text-xs/sp14 flex-none').text if product.find_elements(By.CLASS_NAME, 'rating-class') else 'N/A'  # Adjust selector
            product_sales = product.find_element(By.CLASS_NAME, 'truncate text-shopee-black87 text-xs min-h-4').text if product.find_elements(By.CLASS_NAME, '_18SLBt') else 'N/A'  # Adjust selector

            product_details.append([product_link, product_name, product_price, product_rating, product_sales])


        return product_details

# Function to scrape and save data from a shop
def scrape_shop(shop_link):
    product_details = scrape_shop_products(shop_link)
    
    # Save all the product details to a CSV file
    df = pd.DataFrame(product_details, columns=['product_link', 'product_name', 'product_price', 'product_rating', 'product_sales'])
    df.to_csv('products.csv', index=False)

# Initialize WebDriver
driver = webdriver.Chrome()

shop_link = "https://shopee.vn/cloudzy_official"

cookie_file = "cookies.json" 

# Scrape the shop products
set_random_headers(driver)

# Scrape the shop products
scrape_shop(shop_link, cookie_file)

# Close WebDriver
driver.quit()


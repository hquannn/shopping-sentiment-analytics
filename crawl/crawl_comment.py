import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Load the CSV file
products_df = pd.read_csv('products.csv')

# Function to load cookies from a JSON file and apply them
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

# Initialize WebDriver
driver = webdriver.Chrome()

# Path to your cookies JSON file
json_file = 'cookies.json'

# Load cookies and set headers
load_cookies_from_json(driver, json_file)
set_random_headers(driver)

def scrape_comments_by_rating(driver, product_link, rating_counts):
    driver.get(product_link)
    time.sleep(5)  # Adjust based on page load time

    comments_data = []
    rating_map = {'5': 0, '4': 0, '3': 0, '2': 0, '1': 0}

    while any(count < rating_counts[rating] for rating, count in rating_map.items()):
        comments = driver.find_elements(By.CLASS_NAME, 'comment-class')  # Adjust the selector
        for comment in comments:
            rating = comment.find_element(By.CLASS_NAME, 'product-rating-overview__filter').text
            if rating in rating_map and rating_map[rating] < rating_counts[rating]:
                user = comment.find_element(By.CLASS_NAME, 'shopee-product-rating__author-name').text
                date = comment.find_element(By.CLASS_NAME, 'shopee-product-rating__time').text
                review = comment.find_element(By.CLASS_NAME, 'shopee-product-rating__main').text
                comments_data.append([product_id, user, date, review, rating])
                rating_map[rating] += 1

        try:
            next_button = driver.find_element(By.CLASS_NAME, 'next-button-class')  # Adjust the selector
            next_button.click()
            time.sleep(3)
        except:
            break

    return comments_data

# Desired number of comments by rating
rating_counts = {'5': 300, '4': 200, '3': float('inf'), '2': float('inf'), '1': float('inf')}

for index, row in products_df.iterrows():
    product_id = row['ID']
    product_link = row['product_link']

    comments_data = scrape_comments_by_rating(driver, product_link, rating_counts)

    # Save the comments to a CSV file
    comments_df = pd.DataFrame(comments_data, columns=['Rating', 'User', 'Date', 'Review'])
    comments_df.to_csv(f'{product_id}.csv', index=False)

# Close WebDriver
driver.quit()

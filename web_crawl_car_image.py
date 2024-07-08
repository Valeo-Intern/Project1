from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.request
import os
import pandas as pd

# Base URL for Google Image search
base_url = "https://www.google.co.kr/imghp"

# Chrome driver options setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("lang=ko_KR")
chrome_options.add_argument("window-size=1920x1080")

# Use WebDriver Manager to handle driver installation
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(base_url)
driver.implicitly_wait(10)  # Increased wait time

# Search query input and execution
search_query = 'car rear seat image'
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# Scroll function
def selenium_scroll_option():
    SCROLL_PAUSE_TIME = 1.0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

selenium_scroll_option()

# Try to click 'Show more results' button
try:
    more_results = driver.find_element(By.CSS_SELECTOR, ".mye4qd")
    if more_results.is_displayed():
        more_results.click()
        selenium_scroll_option()
except Exception as e:
    print("No 'Show more results' button found or error occurred:", e)

# Collect image URLs
images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
images_url = []
for img in images:
    if img.get_attribute('src') is not None:
        images_url.append(img.get_attribute('src'))
    elif img.get_attribute('data-src') is not None:
        images_url.append(img.get_attribute('data-src'))

driver.quit()  # Close the browser

# Remove duplicate URLs
unique_images_url = pd.Series(images_url).unique()

# Create directory for saving images
output_dir = 'rear_seat_images'
os.makedirs(output_dir, exist_ok=True)

# Image download function
def download_image(url, save_path):
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Download images
for i, url in enumerate(unique_images_url):
    save_path = os.path.join(output_dir, f'rear_seat_{i+1}.jpg')
    download_image(url, save_path)

print("Image download complete.")
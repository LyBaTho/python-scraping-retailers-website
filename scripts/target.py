# --- Code Cell ---
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

import time

import pandas as pd

import requests

from bs4 import BeautifulSoup

import json

import re

import os, sys

from selenium.common.exceptions import NoSuchElementException

from urllib.parse import urljoin

import datetime

import pygetwindow as gw

from pathlib import Path

from data_folder_setup import get_data_folder


# --- Code Cell ---
data_folder = get_data_folder()


# --- Code Cell ---
# Step 1: Setup Chrome Options

options = uc.ChromeOptions()

options.add_argument("--start-maximized")  # Ensure maximized


# --- Code Cell ---
# Step 1: Launch undetected Chrome

driver = uc.Chrome(options=options)


# --- Code Cell ---
# Step 2: Go to Walmart homepage

driver.get("https://www.target.com/")

time.sleep(5)


# --- Code Cell ---
# Step 3: Bring Chrome to front (ensure active window)

time.sleep(2)

windows = gw.getWindowsWithTitle('Target')  # Partial match is safer

if windows:

    windows[0].activate()

    print("Activated Target browser window")

else:

    print("Window not found - check browser title")


# --- Code Cell ---
# Step 4: Now go directly to the desired category URL

driver.get("https://www.target.com/c/pantry-grocery/-/N-5xt13")

print("Navigated to category page.")


# --- Code Cell ---
time.sleep(20)


# --- Code Cell ---
# Navigate to the first subcategory - "Condiments & Salad Dressings"

subcategory_url = "https://www.target.com/c/condiments-salad-dressings-pantry-grocery/-/N-5xszw"

driver.get(subcategory_url)

print("Navigated to subcategory: Condiments & Salad Dressings")


# --- Code Cell ---
time.sleep(10)


# --- Code Cell ---
all_products = []


# --- Code Cell ---
page = 1

while True:

    print(f"\n=== Scraping Page {page} ===")



    # Wait for grid container

    WebDriverWait(driver, 15).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="product-grid"]'))

    )



    # Gradual Scroll to Fully Load Products

    scroll_pause_time = 2

    scroll_step = 600

    min_scrolls = 9

    max_scrolls = 50



    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_count = 0



    while scroll_count < max_scrolls:

        driver.execute_script(f"window.scrollBy(0, {scroll_step});")

        time.sleep(scroll_pause_time)



        new_height = driver.execute_script("return document.body.scrollHeight")

        scroll_count += 1



        if scroll_count >= min_scrolls and new_height == last_height:

            print(f" • No more products loading after {scroll_count} scrolls.")

            break



        last_height = new_height



    print(f" • Finished scrolling after {scroll_count} scrolls.")



    # Scrape products

    grid = driver.find_element(By.CSS_SELECTOR, 'div[data-test="product-grid"]')

    items = grid.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')

    print(f" • Found {len(items)} product wrappers")



    for it in items:

        try:

            # Product link and SKU

            link_elem = it.find_element(By.XPATH, './/div[@data-test="@web/ProductCard/ProductCardImageHoverableLink"]//a')

            href = link_elem.get_attribute("href")

            full_url = urljoin("https://www.target.com", href)



            sku_match = re.search(r"/-\/A-(\d+)", full_url)

            sku = sku_match.group(1) if sku_match else ""



            # Product Name from aria-label

            name_elem = it.find_element(By.CSS_SELECTOR, 'a[data-test="product-title"]')

            product_name = name_elem.get_attribute("aria-label").strip()



            # Current Price

            price_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="current-price"]')

            price = price_elem.text.strip()



            # Unit Price

            try:

                unit_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="unit-price"]')

                unit_price = unit_elem.text.strip().replace("\n", " ").strip("()")

            except NoSuchElementException:

                unit_price = ""



            all_products.append({

                "SKU": sku,

                "Product Name": product_name,

                "Category": "condiments & salad dressings",

                "Unit Price": unit_price,

                "URL": full_url,

            })



        except NoSuchElementException:

            print(" • Non-product item skipped (link missing)")

            continue

        except Exception as e:

            print(f" • Skipped item due to error: {e}")

            continue



    # Next page logic with safe scroll before click

    try:

        next_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-test="next"]')

        if next_btn.get_attribute("disabled"):

            print(" • No more pages.")

            break

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)

        time.sleep(1)

        next_btn.click()

        page += 1

        time.sleep(2 + page * 0.2)

    except NoSuchElementException:

        print(" • Next button not found, stopping.")

        break



print(f"\n✦ Done: scraped {len(all_products)} total products")


# --- Code Cell ---
all_products


# --- Code Cell ---
df_condiments = pd.DataFrame(all_products)


# --- Code Cell ---
df_condiments.head()


# --- Code Cell ---
# Navigate to the first subcategory - "Sauces & Marinades"

subcategory_url = "https://www.target.com/c/sauces-marinades-pantry-grocery/-/N-4tg6h"

driver.get(subcategory_url)

print("Navigated to subcategory: Sauces & Marinades")


# --- Code Cell ---
time.sleep(10)


# --- Code Cell ---
all_products = []


# --- Code Cell ---
page = 1

while True:

    print(f"\n=== Scraping Page {page} ===")



    # Wait for grid container

    WebDriverWait(driver, 15).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="product-grid"]'))

    )



    # Gradual Scroll to Fully Load Products

    scroll_pause_time = 2

    scroll_step = 600

    min_scrolls = 9

    max_scrolls = 50



    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_count = 0



    while scroll_count < max_scrolls:

        driver.execute_script(f"window.scrollBy(0, {scroll_step});")

        time.sleep(scroll_pause_time)



        new_height = driver.execute_script("return document.body.scrollHeight")

        scroll_count += 1



        if scroll_count >= min_scrolls and new_height == last_height:

            print(f" • No more products loading after {scroll_count} scrolls.")

            break



        last_height = new_height



    print(f" • Finished scrolling after {scroll_count} scrolls.")



    # Scrape products

    grid = driver.find_element(By.CSS_SELECTOR, 'div[data-test="product-grid"]')

    items = grid.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')

    print(f" • Found {len(items)} product wrappers")



    for it in items:

        try:

            # Product link and SKU

            link_elem = it.find_element(By.XPATH, './/div[@data-test="@web/ProductCard/ProductCardImageHoverableLink"]//a')

            href = link_elem.get_attribute("href")

            full_url = urljoin("https://www.target.com", href)



            sku_match = re.search(r"/-\/A-(\d+)", full_url)

            sku = sku_match.group(1) if sku_match else ""



            # Product Name from aria-label

            name_elem = it.find_element(By.CSS_SELECTOR, 'a[data-test="product-title"]')

            product_name = name_elem.get_attribute("aria-label").strip()



            # Current Price

            price_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="current-price"]')

            price = price_elem.text.strip()



            # Unit Price

            try:

                unit_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="unit-price"]')

                unit_price = unit_elem.text.strip().replace("\n", " ").strip("()")

            except NoSuchElementException:

                unit_price = ""



            all_products.append({

                "SKU": sku,

                "Product Name": product_name,

                "Category": "sauces & marinades",

                "Unit Price": unit_price,

                "URL": full_url,

            })



        except NoSuchElementException:

            print(" • Non-product item skipped (link missing)")

            continue

        except Exception as e:

            print(f" • Skipped item due to error: {e}")

            continue



    # Next page logic with safe scroll before click

    try:

        next_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-test="next"]')

        if next_btn.get_attribute("disabled"):

            print(" • No more pages.")

            break

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)

        time.sleep(1)

        next_btn.click()

        page += 1

        time.sleep(2 + page * 0.2)

    except NoSuchElementException:

        print(" • Next button not found, stopping.")

        break



print(f"\n✦ Done: scraped {len(all_products)} total products")


# --- Code Cell ---
df_sauces = pd.DataFrame(all_products)


# --- Code Cell ---
df_sauces


# --- Code Cell ---
# Navigate to the first subcategory - "Salsa & Dips"

subcategory_url = "https://www.target.com/c/dips-spreads-chips-snacks-cookies-grocery/-/N-5xsy5"

driver.get(subcategory_url)

print("Navigated to subcategory: Salsa & Dips")


# --- Code Cell ---
time.sleep(10)


# --- Code Cell ---
all_products = []


# --- Code Cell ---
page = 1

while True:

    print(f"\n=== Scraping Page {page} ===")



    # Wait for grid container

    WebDriverWait(driver, 15).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="product-grid"]'))

    )



    # Gradual Scroll to Fully Load Products

    scroll_pause_time = 2

    scroll_step = 600

    min_scrolls = 9

    max_scrolls = 50



    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_count = 0



    while scroll_count < max_scrolls:

        driver.execute_script(f"window.scrollBy(0, {scroll_step});")

        time.sleep(scroll_pause_time)



        new_height = driver.execute_script("return document.body.scrollHeight")

        scroll_count += 1



        if scroll_count >= min_scrolls and new_height == last_height:

            print(f" • No more products loading after {scroll_count} scrolls.")

            break



        last_height = new_height



    print(f" • Finished scrolling after {scroll_count} scrolls.")



    # Scrape products

    grid = driver.find_element(By.CSS_SELECTOR, 'div[data-test="product-grid"]')

    items = grid.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')

    print(f" • Found {len(items)} product wrappers")



    for it in items:

        try:

            # Product link and SKU

            link_elem = it.find_element(By.XPATH, './/div[@data-test="@web/ProductCard/ProductCardImageHoverableLink"]//a')

            href = link_elem.get_attribute("href")

            full_url = urljoin("https://www.target.com", href)



            sku_match = re.search(r"/-\/A-(\d+)", full_url)

            sku = sku_match.group(1) if sku_match else ""



            # Product Name from aria-label

            name_elem = it.find_element(By.CSS_SELECTOR, 'a[data-test="product-title"]')

            product_name = name_elem.get_attribute("aria-label").strip()



            # Current Price

            price_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="current-price"]')

            price = price_elem.text.strip()



            # Unit Price

            try:

                unit_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="unit-price"]')

                unit_price = unit_elem.text.strip().replace("\n", " ").strip("()")

            except NoSuchElementException:

                unit_price = ""



            all_products.append({

                "SKU": sku,

                "Product Name": product_name,

                "Category": "salsa & dips",

                "Unit Price": unit_price,

                "URL": full_url,

            })



        except NoSuchElementException:

            print(" • Non-product item skipped (link missing)")

            continue

        except Exception as e:

            print(f" • Skipped item due to error: {e}")

            continue



    # Next page logic with safe scroll before click

    try:

        next_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-test="next"]')

        if next_btn.get_attribute("disabled"):

            print(" • No more pages.")

            break

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)

        time.sleep(1)

        next_btn.click()

        page += 1

        time.sleep(2 + page * 0.2)

    except NoSuchElementException:

        print(" • Next button not found, stopping.")

        break



print(f"\n✦ Done: scraped {len(all_products)} total products")


# --- Code Cell ---
df_salsa = pd.DataFrame(all_products)


# --- Code Cell ---
df_salsa


# --- Code Cell ---
# Navigate to the first subcategory - "Soups, Broth & Chili"

subcategory_url = "https://www.target.com/c/soups-broth-chili-pantry-grocery/-/N-5xszx"

driver.get(subcategory_url)

print("Navigated to subcategory: Soups, Broth & Chili")


# --- Code Cell ---
time.sleep(10)


# --- Code Cell ---
all_products = []


# --- Code Cell ---
page = 1

while True:

    print(f"\n=== Scraping Page {page} ===")



    # Wait for grid container

    WebDriverWait(driver, 15).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="product-grid"]'))

    )



    # Gradual Scroll to Fully Load Products

    scroll_pause_time = 2

    scroll_step = 600

    min_scrolls = 9

    max_scrolls = 50



    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_count = 0



    while scroll_count < max_scrolls:

        driver.execute_script(f"window.scrollBy(0, {scroll_step});")

        time.sleep(scroll_pause_time)



        new_height = driver.execute_script("return document.body.scrollHeight")

        scroll_count += 1



        if scroll_count >= min_scrolls and new_height == last_height:

            print(f" • No more products loading after {scroll_count} scrolls.")

            break



        last_height = new_height



    print(f" • Finished scrolling after {scroll_count} scrolls.")



    # Scrape products

    grid = driver.find_element(By.CSS_SELECTOR, 'div[data-test="product-grid"]')

    items = grid.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')

    print(f" • Found {len(items)} product wrappers")



    for it in items:

        try:

            # Product link and SKU

            link_elem = it.find_element(By.XPATH, './/div[@data-test="@web/ProductCard/ProductCardImageHoverableLink"]//a')

            href = link_elem.get_attribute("href")

            full_url = urljoin("https://www.target.com", href)



            sku_match = re.search(r"/-\/A-(\d+)", full_url)

            sku = sku_match.group(1) if sku_match else ""



            # Product Name from aria-label

            name_elem = it.find_element(By.CSS_SELECTOR, 'a[data-test="product-title"]')

            product_name = name_elem.get_attribute("aria-label").strip()



            # Current Price

            price_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="current-price"]')

            price = price_elem.text.strip()



            # Unit Price

            try:

                unit_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="unit-price"]')

                unit_price = unit_elem.text.strip().replace("\n", " ").strip("()")

            except NoSuchElementException:

                unit_price = ""



            all_products.append({

                "SKU": sku,

                "Product Name": product_name,

                "Category": "soups, broth & chili",

                "Unit Price": unit_price,

                "URL": full_url,

            })



        except NoSuchElementException:

            print(" • Non-product item skipped (link missing)")

            continue

        except Exception as e:

            print(f" • Skipped item due to error: {e}")

            continue



    # Next page logic with safe scroll before click

    try:

        next_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-test="next"]')

        if next_btn.get_attribute("disabled"):

            print(" • No more pages.")

            break

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)

        time.sleep(1)

        next_btn.click()

        page += 1

        time.sleep(2 + page * 0.2)

    except NoSuchElementException:

        print(" • Next button not found, stopping.")

        break



print(f"\n✦ Done: scraped {len(all_products)} total products")


# --- Code Cell ---
df_soups = pd.DataFrame(all_products)


# --- Code Cell ---
# Navigate to the first subcategory - "Spices & Seasonings"

subcategory_url = "https://www.target.com/c/spices-seasonings-pantry-grocery/-/N-5xszu"

driver.get(subcategory_url)

print("Navigated to subcategory: Spices & Seasonings")


# --- Code Cell ---
time.sleep(10)


# --- Code Cell ---
all_products = []


# --- Code Cell ---
page = 1

while True:

    print(f"\n=== Scraping Page {page} ===")



    # Wait for grid container

    WebDriverWait(driver, 15).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="product-grid"]'))

    )



    # Gradual Scroll to Fully Load Products

    scroll_pause_time = 2

    scroll_step = 600

    min_scrolls = 9

    max_scrolls = 50



    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_count = 0



    while scroll_count < max_scrolls:

        driver.execute_script(f"window.scrollBy(0, {scroll_step});")

        time.sleep(scroll_pause_time)



        new_height = driver.execute_script("return document.body.scrollHeight")

        scroll_count += 1



        if scroll_count >= min_scrolls and new_height == last_height:

            print(f" • No more products loading after {scroll_count} scrolls.")

            break



        last_height = new_height



    print(f" • Finished scrolling after {scroll_count} scrolls.")



    # Scrape products

    grid = driver.find_element(By.CSS_SELECTOR, 'div[data-test="product-grid"]')

    items = grid.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')

    print(f" • Found {len(items)} product wrappers")



    for it in items:

        try:

            # Product link and SKU

            link_elem = it.find_element(By.XPATH, './/div[@data-test="@web/ProductCard/ProductCardImageHoverableLink"]//a')

            href = link_elem.get_attribute("href")

            full_url = urljoin("https://www.target.com", href)



            sku_match = re.search(r"/-\/A-(\d+)", full_url)

            sku = sku_match.group(1) if sku_match else ""



            # Product Name from aria-label

            name_elem = it.find_element(By.CSS_SELECTOR, 'a[data-test="product-title"]')

            product_name = name_elem.get_attribute("aria-label").strip()



            # Current Price

            price_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="current-price"]')

            price = price_elem.text.strip()



            # Unit Price

            try:

                unit_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="unit-price"]')

                unit_price = unit_elem.text.strip().replace("\n", " ").strip("()")

            except NoSuchElementException:

                unit_price = ""



            all_products.append({

                "SKU": sku,

                "Product Name": product_name,

                "Category": "spices & seasonings",

                "Unit Price": unit_price,

                "URL": full_url,

            })



        except NoSuchElementException:

            print(" • Non-product item skipped (link missing)")

            continue

        except Exception as e:

            print(f" • Skipped item due to error: {e}")

            continue



    # Next page logic with safe scroll before click

    try:

        next_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-test="next"]')

        if next_btn.get_attribute("disabled"):

            print(" • No more pages.")

            break

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)

        time.sleep(1)

        next_btn.click()

        page += 1

        time.sleep(2 + page * 0.2)

    except NoSuchElementException:

        print(" • Next button not found, stopping.")

        break



print(f"\n✦ Done: scraped {len(all_products)} total products")


# --- Code Cell ---
df_spices = pd.DataFrame(all_products)


# --- Code Cell ---
# Navigate to the first subcategory - "Ramen"

subcategory_url = "https://www.target.com/c/ramen/-/N-f4xv2"

driver.get(subcategory_url)

print("Navigated to subcategory: Ramen")


# --- Code Cell ---
time.sleep(10)


# --- Code Cell ---
all_products = []


# --- Code Cell ---
page = 1

while True:

    print(f"\n=== Scraping Page {page} ===")



    # Wait for grid container

    WebDriverWait(driver, 15).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="product-grid"]'))

    )



    # Gradual Scroll to Fully Load Products

    scroll_pause_time = 2

    scroll_step = 600

    min_scrolls = 9

    max_scrolls = 50



    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_count = 0



    while scroll_count < max_scrolls:

        driver.execute_script(f"window.scrollBy(0, {scroll_step});")

        time.sleep(scroll_pause_time)



        new_height = driver.execute_script("return document.body.scrollHeight")

        scroll_count += 1



        if scroll_count >= min_scrolls and new_height == last_height:

            print(f" • No more products loading after {scroll_count} scrolls.")

            break



        last_height = new_height



    print(f" • Finished scrolling after {scroll_count} scrolls.")



    # Scrape products

    grid = driver.find_element(By.CSS_SELECTOR, 'div[data-test="product-grid"]')

    items = grid.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')

    print(f" • Found {len(items)} product wrappers")



    for it in items:

        try:

            # Product link and SKU

            link_elem = it.find_element(By.XPATH, './/div[@data-test="@web/ProductCard/ProductCardImageHoverableLink"]//a')

            href = link_elem.get_attribute("href")

            full_url = urljoin("https://www.target.com", href)



            sku_match = re.search(r"/-\/A-(\d+)", full_url)

            sku = sku_match.group(1) if sku_match else ""



            # Product Name from aria-label

            name_elem = it.find_element(By.CSS_SELECTOR, 'a[data-test="product-title"]')

            product_name = name_elem.get_attribute("aria-label").strip()



            # Current Price

            price_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="current-price"]')

            price = price_elem.text.strip()



            # Unit Price

            try:

                unit_elem = it.find_element(By.CSS_SELECTOR, 'span[data-test="unit-price"]')

                unit_price = unit_elem.text.strip().replace("\n", " ").strip("()")

            except NoSuchElementException:

                unit_price = ""



            all_products.append({

                "SKU": sku,

                "Product Name": product_name,

                "Category": "ramen",

                "Unit Price": unit_price,

                "URL": full_url,

            })



        except NoSuchElementException:

            print(" • Non-product item skipped (link missing)")

            continue

        except Exception as e:

            print(f" • Skipped item due to error: {e}")

            continue



    # Next page logic with safe scroll before click

    try:

        next_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-test="next"]')

        if next_btn.get_attribute("disabled"):

            print(" • No more pages.")

            break

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)

        time.sleep(1)

        next_btn.click()

        page += 1

        time.sleep(2 + page * 0.2)

    except NoSuchElementException:

        print(" • Next button not found, stopping.")

        break



print(f"\n✦ Done: scraped {len(all_products)} total products")


# --- Code Cell ---
df_ramen = pd.DataFrame(all_products)

df_condiments = df_condiments.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_sauces = df_sauces.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_salsa = df_salsa.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_soups = df_soups.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_spices = df_spices.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_ramen = df_ramen.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)

# --- Code Cell ---
df_final = pd.concat([df_condiments, df_sauces, df_salsa, df_soups, df_spices, df_ramen], ignore_index=True)

df_final = df_final.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)

# --- Code Cell ---
# get today’s date as a string, e.g. "2025-06-14"

today_str = datetime.date.today().isoformat()


# --- Code Cell ---
# add the new column

df_final['Date of Scraping'] = today_str


# --- Code Cell ---
for col in ['Category']:

    df_final[col] = df_final[col].str.lower()


# --- Code Cell ---
df_final.duplicated().any()


# --- Code Cell ---
df_final = df_final.drop_duplicates(keep='first').reset_index(drop=True)

# --- Code Cell ---
driver.quit()


# --- Code Cell ---
filename = f"target_products_{datetime.datetime.now():%Y%m%d}.xlsx"

df_final.to_excel(os.path.join(data_folder, filename), index=False)


# --- Code Cell ---


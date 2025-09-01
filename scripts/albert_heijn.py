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

import datetime

from pathlib import Path

from data_folder_setup import get_data_folder


# --- Code Cell ---
data_folder = get_data_folder()


# --- Code Cell ---
# Step 1: Launch undetected Chrome

driver = uc.Chrome()



# Step 2: Go to AH homepage

driver.get("https://www.ah.nl")

time.sleep(5)



# Step 3: Reject cookie banner

try:

    reject_button = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Weigeren')]"))

    )

    reject_button.click()

    print("Cookie banner rejected.")

    time.sleep(3)

except:

    print("No cookie banner.")

    time.sleep(3)



# Step 4: Navigate to /producten page

try:

    producten_link = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//a[@href='/producten']"))

    )

    producten_link.click()

    print("Clicked 'Producten'.")

    time.sleep(3)

except:

    print("Producten link not found.")

    time.sleep(5)



# Step 5: Reject cookie banner (if it pops up)

try:

    reject_button = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Weigeren')]"))

    )

    reject_button.click()

    print("Cookie banner rejected.")

    time.sleep(3)

except:

    print("No cookie banner.")

    time.sleep(3)



# Step 6: Now go directly to the desired category URL

time.sleep(2)  # slight pause to stabilize session

driver.get("https://www.ah.nl/producten/6409/soepen-sauzen-kruiden-olie")

print("Navigated to category page.")


# --- Code Cell ---
# Navigate to the first subcategory - "Soepen"

time.sleep(3)

subcategory_url = "https://www.ah.nl/producten/1561/soepen"

driver.get(subcategory_url)

print("Navigated to subcategory: Soups")


# --- Code Cell ---
try:

    reject_button = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Weigeren')]"))

    )

    reject_button.click()

    print("Cookie banner rejected.")

    time.sleep(3)

except:

    print("No cookie banner.")

    time.sleep(3)


# --- Code Cell ---
# 1) Define your sub-categories

subcategories = {

    'Fresh soups':     'https://www.ah.nl/producten/2279/verse-soepen',

    'Soup in a bag':      'https://www.ah.nl/producten/11659/soep-in-zak',

    'Canned soup':     'https://www.ah.nl/producten/11660/soep-in-blik',

    'Cup soup':          'https://www.ah.nl/producten/1267/kopsoep',

    'Noodle soup':       'https://www.ah.nl/producten/21301/noedelsoep',

    'Soup mixes':        'https://www.ah.nl/producten/10483/soepmixen',

    'Soup enrichment':   'https://www.ah.nl/producten/10484/soepverrijking',

}


# --- Code Cell ---
all_products = []


# --- Code Cell ---
# 2) Loop over each sub-category

for sub_name, sub_url in subcategories.items():

    print(f"\n=== Scraping sub-category: {sub_name} ===")

    driver.get(sub_url)

    

    # wait for product cards

    WebDriverWait(driver, 10).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testhook='product-card']"))

    )

    

    # 3) click "Meer resultaten" until it's gone

    while True:

        try:

            btn = WebDriverWait(driver, 5).until(

                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testhook='load-more']"))

            )

            driver.execute_script("arguments[0].scrollIntoView();", btn)

            time.sleep(2)

            btn.click()

            time.sleep(2)

        except:

            break

    

    # 4) Collect all product cards

    cards = driver.find_elements(By.CSS_SELECTOR, "article[data-testhook='product-card']")

    print(f"  • Found {len(cards)} products")

    

    for card in cards:

        try:

            # Name & link

            a = card.find_element(By.CSS_SELECTOR, "a.link_root__EqRHd")

            name = a.get_attribute("title")

            href = a.get_attribute("href")

            full_link = href if href.startswith("http") else "https://www.ah.nl" + href

            

            # Unit size

            try:

                unit_el = card.find_element(By.CSS_SELECTOR, "[data-testhook='product-unit-size']")

                unit_size = unit_el.text.strip()

            except:

                unit_size = ""  # if some cards have no unit-size

            

            all_products.append({

                'Product Name': name,

                'URL':          full_link,

                'Unit Size':     unit_size,

                'Category':     'Soups',

                'Sub-Category': sub_name

            })

        except Exception as e:

            print("  • error on one card:", e)


# --- Code Cell ---
# 5) Build DataFrame and save

df_soup = pd.DataFrame(all_products)


# --- Code Cell ---
# Remove "Bekijk " from beginning of each product name

df_soup["Product Name"] = df_soup["Product Name"].str.replace(r"^Bekijk\s+", "", regex=True)


# --- Code Cell ---
df_soup.head()


# --- Code Cell ---
# Navigate to the first subcategory - "Soepen"

time.sleep(3)

subcategory_url = "https://www.ah.nl/producten/10480/sauzen"

driver.get(subcategory_url)

print("Navigated to subcategory: Sauces")


# --- Code Cell ---
try:

    reject_button = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Weigeren')]"))

    )

    reject_button.click()

    print("Cookie banner rejected.")

    time.sleep(3)

except:

    print("No cookie banner.")

    time.sleep(3)


# --- Code Cell ---
# 1) Define your sub-categories

subcategories = {

    'Mayonnaise sauces':     'https://www.ah.nl/producten/1316/mayonaise-sauzen',

    'French fries sauce':      'https://www.ah.nl/producten/1900/fritessaus',

    'Curry sauce, ketchup':     'https://www.ah.nl/producten/21304/currysaus-ketchup',

    'Satay sauce':          'https://www.ah.nl/producten/1490/satesaus',

    'Variation sauces':       'https://www.ah.nl/producten/2403/variatiesauzen',

    'Mustard':        'https://www.ah.nl/producten/10125/mosterd',

    'Hot sauces':   'https://www.ah.nl/producten/21294/hete-sauzen',

    'Meal sauces, gravy':   'https://www.ah.nl/producten/21295/maaltijdsauzen-jus',

    'Pasta sauce':   'https://www.ah.nl/producten/2237/pastasaus',

    'Stir-fry and wok sauces':   'https://www.ah.nl/producten/10543/roerbak-en-woksauzen',

    'Dressings, salad dressings':   'https://www.ah.nl/producten/2249/dressings-slasauzen',

    'Dipping sauce':   'https://www.ah.nl/producten/10566/dipsaus',

    'International meal sauces':   'https://www.ah.nl/producten/10568/maaltijdsauzen-internationaal',

}


# --- Code Cell ---
all_products = []


# --- Code Cell ---
# 2) Loop over each sub-category

for sub_name, sub_url in subcategories.items():

    print(f"\n=== Scraping sub-category: {sub_name} ===")

    driver.get(sub_url)

    

    # wait for product cards

    WebDriverWait(driver, 10).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testhook='product-card']"))

    )

    

    # 3) click "Meer resultaten" until it's gone

    while True:

        try:

            btn = WebDriverWait(driver, 5).until(

                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testhook='load-more']"))

            )

            driver.execute_script("arguments[0].scrollIntoView();", btn)

            time.sleep(2)

            btn.click()

            time.sleep(2)

        except:

            break

    

    # 4) Collect all product cards

    cards = driver.find_elements(By.CSS_SELECTOR, "article[data-testhook='product-card']")

    print(f"  • Found {len(cards)} products")

    

    for card in cards:

        try:

            # Name & link

            a = card.find_element(By.CSS_SELECTOR, "a.link_root__EqRHd")

            name = a.get_attribute("title")

            href = a.get_attribute("href")

            full_link = href if href.startswith("http") else "https://www.ah.nl" + href

            

            # Unit size

            try:

                unit_el = card.find_element(By.CSS_SELECTOR, "[data-testhook='product-unit-size']")

                unit_size = unit_el.text.strip()

            except:

                unit_size = ""  # if some cards have no unit-size

            

            all_products.append({

                'Product Name': name,

                'URL':          full_link,

                'Unit Size':     unit_size,

                'Category':     'Sauces',

                'Sub-Category': sub_name

            })

        except Exception as e:

            print("  • error on one card:", e)


# --- Code Cell ---
# 5) Build DataFrame and save

df_sauce = pd.DataFrame(all_products)


# --- Code Cell ---
# Remove "Bekijk " from beginning of each product name

df_sauce["Product Name"] = df_sauce["Product Name"].str.replace(r"^Bekijk\s+", "", regex=True)


# --- Code Cell ---
df_sauce.head()


# --- Code Cell ---
# Navigate to the first subcategory - "Bouillon"

time.sleep(3)

subcategory_url = "https://www.ah.nl/producten/1070/bouillon"

driver.get(subcategory_url)

print("Navigated to subcategory: Bouillon")


# --- Code Cell ---
try:

    reject_button = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Weigeren')]"))

    )

    reject_button.click()

    print("Cookie banner rejected.")

    time.sleep(3)

except:

    print("No cookie banner.")

    time.sleep(3)


# --- Code Cell ---
# 1) Define your sub-categories

subcategories = {

    'Bouillon cubes':     'https://www.ah.nl/producten/21094/bouillonblokjes',

    'Bouillon liquid':      'https://www.ah.nl/producten/21296/bouillon-vloeibaar',

    'Bouillon drink':     'https://www.ah.nl/producten/21096/drink-bouillon',

    'Miso and ramen Bouillon':          'https://www.ah.nl/producten/21240/miso-en-ramen-bouillon',

    'Fund':       'https://www.ah.nl/producten/1872/fond',

}


# --- Code Cell ---
all_products = []


# --- Code Cell ---
# 2) Loop over each sub-category

for sub_name, sub_url in subcategories.items():

    print(f"\n=== Scraping sub-category: {sub_name} ===")

    driver.get(sub_url)

    

    # wait for product cards

    WebDriverWait(driver, 10).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testhook='product-card']"))

    )

    

    # 3) click "Meer resultaten" until it's gone

    while True:

        try:

            btn = WebDriverWait(driver, 5).until(

                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testhook='load-more']"))

            )

            driver.execute_script("arguments[0].scrollIntoView();", btn)

            time.sleep(2)

            btn.click()

            time.sleep(2)

        except:

            break

    

    # 4) Collect all product cards

    cards = driver.find_elements(By.CSS_SELECTOR, "article[data-testhook='product-card']")

    print(f"  • Found {len(cards)} products")

    

    for card in cards:

        try:

            # Name & link

            a = card.find_element(By.CSS_SELECTOR, "a.link_root__EqRHd")

            name = a.get_attribute("title")

            href = a.get_attribute("href")

            full_link = href if href.startswith("http") else "https://www.ah.nl" + href

            

            # Unit size

            try:

                unit_el = card.find_element(By.CSS_SELECTOR, "[data-testhook='product-unit-size']")

                unit_size = unit_el.text.strip()

            except:

                unit_size = ""  # if some cards have no unit-size

            

            all_products.append({

                'Product Name': name,

                'URL':          full_link,

                'Unit Size':     unit_size,

                'Category':     'Bouillon',

                'Sub-Category': sub_name

            })

        except Exception as e:

            print("  • error on one card:", e)


# --- Code Cell ---
# 5) Build DataFrame and save

df_bouillon = pd.DataFrame(all_products)


# --- Code Cell ---
# Remove "Bekijk " from beginning of each product name

df_bouillon["Product Name"] = df_bouillon["Product Name"].str.replace(r"^Bekijk\s+", "", regex=True)


# --- Code Cell ---
df_bouillon.head()


# --- Code Cell ---
df_final = pd.concat([df_soup, df_bouillon, df_sauce], ignore_index=True)


# --- Code Cell ---
# get today’s date as a string

today_str = datetime.date.today().isoformat()


# --- Code Cell ---
# add the new column

df_final['Date of Scraping'] = today_str


# --- Code Cell ---
# extract the AH product code from the URL and call it SKU

df_final['SKU'] = df_final['URL'].str.extract(r'/product/([^/]+)/')
df_final = df_final.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)

# --- Code Cell ---
# remove SKU column and grab it

sku_col = df_final.pop('SKU')


# --- Code Cell ---
# insert it back at position 0

df_final.insert(0, 'SKU', sku_col)


# --- Code Cell ---
# remove Category column and grab it

cat_col = df_final.pop('Category')


# --- Code Cell ---
# insert it back at position 2

df_final.insert(2, 'Category', cat_col)


# --- Code Cell ---
# remove Sub-Category column and grab it

scat_col = df_final.pop('Sub-Category')


# --- Code Cell ---
# insert it back at position 3

df_final.insert(3, 'Sub-Category', scat_col)


# --- Code Cell ---
# remove Unit Size column and grab it

unit = df_final.pop('Unit Size')


# --- Code Cell ---
# insert it back at position 4

df_final.insert(4, 'Unit Size', unit)


# --- Code Cell ---
for col in ['Category', 'Sub-Category']:

    df_final[col] = df_final[col].str.lower()


# --- Code Cell ---
df_final


# --- Code Cell ---
df_final.duplicated().any()


# --- Code Cell ---
df_final = df_final.drop_duplicates(keep='first').reset_index(drop=True)


# --- Code Cell ---
driver.quit()


# --- Code Cell ---
filename = f"ah_products_{datetime.datetime.now():%Y%m%d}.xlsx"

df_final.to_excel(os.path.join(data_folder, filename), index=False)


# --- Code Cell ---


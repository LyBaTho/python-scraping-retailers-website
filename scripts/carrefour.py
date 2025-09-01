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

driver.get("https://www.carrefour.fr/")

time.sleep(3)



# Step 3: Reject cookie banner

try:

    reject_button = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Tout accepter')]"))

    )

    reject_button.click()

    print("Cookie banner rejected.")

    time.sleep(3)

except:

    print("No cookie banner.")

    time.sleep(3)


# --- Code Cell ---
# Step 4: Now go directly to the desired category URL

time.sleep(2)  # slight pause to stabilize session

driver.get("https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee")

print("Navigated to category page.")


# --- Code Cell ---
# Navigate to the first subcategory - "Soupes"

time.sleep(3)

subcategory_url = "https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/soupes-et-potages"

driver.get(subcategory_url)

print("Navigated to subcategory: Soups")


# --- Code Cell ---
try:

    reject_button = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Tout accepter')]"))

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

    'soups':     'https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/soupes-et-potages'

}


# --- Code Cell ---
all_products = []


# --- Code Cell ---
for sub_name, sub_url in subcategories.items():

    print(f"\n=== Scraping sub-category: {sub_name} ===")

    driver.get(sub_url)



    # 3) Wait for the product grid to appear

    WebDriverWait(driver, 15).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product-list-grid"))

    )



    # 4) Click “Afficher les produits suivants” until it's gone / no new items

    while True:

        try:

            btn = WebDriverWait(driver, 5).until(

                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.pagination__button-wrap button"))

            )

        except:

            print(" • no more load-more button")

            break



        before_count = len(driver.find_elements(

            By.CSS_SELECTOR, "ul.product-list-grid > li.product-list-grid__item"

        ))



        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)

        time.sleep(0.5)

        try:

            btn.click()

        except ElementClickInterceptedException:

            driver.execute_script("arguments[0].click();", btn)



        print(f" • clicked load-more (had {before_count} items)…")



        # wait for new items to appear

        try:

            WebDriverWait(driver, 10).until(

                lambda d: len(d.find_elements(

                    By.CSS_SELECTOR, "ul.product-list-grid > li.product-list-grid__item"

                )) > before_count

            )

            print("   → new items loaded")

            time.sleep(0.5)

        except:

            print("   → timed out waiting for new items")

            break



    # 5) Scrape all loaded items

    items = driver.find_elements(

        By.CSS_SELECTOR, "ul.product-list-grid > li.product-list-grid__item"

    )

    print(f" • total products found: {len(items)}")



    for it in items:

        # URL & SKU

        a = it.find_element(By.TAG_NAME, "a")

        href = a.get_attribute("href")

        m = re.search(r"(\d{7,})", href or "")

        sku = m.group(1) if m else ""



        # Name

        name = it.find_element(By.TAG_NAME, "h3").text.strip()



        # Unit Size: primary selector → fallback to the packaging caption, then regex-extract only the number+unit

        unit = ""

        try:

            unit = it.find_element(

                By.CSS_SELECTOR,

                ".ds-format.product-list-card-plp-grid__shimzone--small"

            ).text.strip()

        except:

            try:

                raw = it.find_element(

                    By.CSS_SELECTOR,

                    "span.product-list-card-plp-grid__packaging"

                ).text.strip()

                # extract only the number+unit, e.g. "1L", "250mL"

                match = re.search(r"(\d+(?:[.,]\d+)?\s*[A-Za-z]+)", raw)

                unit = match.group(1) if match else raw

            except:

                unit = ""



        all_products.append({

            "SKU":            sku,

            "Product Name":   name,

            "Category":       "soups",

            "Sub-Category":   sub_name,

            "Unit Size":      unit,

            "URL":            href

        })


# --- Code Cell ---
df_soup = pd.DataFrame(all_products)


# --- Code Cell ---
df_soup


# --- Code Cell ---
# Navigate to the first subcategory - "Oils, Sauces, and Condiments"

time.sleep(3)

subcategory_url = "https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/sauces-et-condiments"

driver.get(subcategory_url)

print("Navigated to subcategory: Oils, Sauces, and Condiments")


# --- Code Cell ---
try:

    reject_button = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Tout accepter')]"))

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

    'vinaigrettes':     'https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/sauces-et-condiments/huiles-vinaigrettes',

    'sauces':'https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/sauces-et-condiments/sauces',

    'condiments and spices':'https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/sauces-et-condiments/condiments-epices'

}


# --- Code Cell ---
all_products = []


# --- Code Cell ---
for sub_name, sub_url in subcategories.items():

    print(f"\n=== Scraping sub-category: {sub_name} ===")

    driver.get(sub_url)



    # 3) Wait for the product grid to appear

    WebDriverWait(driver, 15).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product-list-grid"))

    )



    # 4) Click “Afficher les produits suivants” until it's gone / no new items

    while True:

        try:

            btn = WebDriverWait(driver, 5).until(

                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.pagination__button-wrap button"))

            )

        except:

            print(" • no more load-more button")

            break



        before_count = len(driver.find_elements(

            By.CSS_SELECTOR, "ul.product-list-grid > li.product-list-grid__item"

        ))



        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)

        time.sleep(0.5)

        try:

            btn.click()

        except ElementClickInterceptedException:

            driver.execute_script("arguments[0].click();", btn)



        print(f" • clicked load-more (had {before_count} items)…")



        # wait for new items to appear

        try:

            WebDriverWait(driver, 10).until(

                lambda d: len(d.find_elements(

                    By.CSS_SELECTOR, "ul.product-list-grid > li.product-list-grid__item"

                )) > before_count

            )

            print("   → new items loaded")

            time.sleep(0.5)

        except:

            print("   → timed out waiting for new items")

            break



    # 5) Scrape all loaded items

    items = driver.find_elements(

        By.CSS_SELECTOR, "ul.product-list-grid > li.product-list-grid__item"

    )

    print(f" • total products found: {len(items)}")



    for it in items:

        # URL & SKU

        a = it.find_element(By.TAG_NAME, "a")

        href = a.get_attribute("href")

        m = re.search(r"(\d{7,})", href or "")

        sku = m.group(1) if m else ""



        # Name

        name = it.find_element(By.TAG_NAME, "h3").text.strip()



        # Unit Size: primary selector → fallback to the packaging caption, then regex-extract only the number+unit

        unit = ""

        try:

            unit = it.find_element(

                By.CSS_SELECTOR,

                ".ds-format.product-list-card-plp-grid__shimzone--small"

            ).text.strip()

        except:

            try:

                raw = it.find_element(

                    By.CSS_SELECTOR,

                    "span.product-list-card-plp-grid__packaging"

                ).text.strip()

                # extract only the number+unit, e.g. "1L", "250mL"

                match = re.search(r"(\d+(?:[.,]\d+)?\s*[A-Za-z]+)", raw)

                unit = match.group(1) if match else raw

            except:

                unit = ""



        all_products.append({

            "SKU":            sku,

            "Product Name":   name,

            "Category":       "oils, sauces, and condiments",

            "Sub-Category":   sub_name,

            "Unit Size":      unit,

            "URL":            href

        })


# --- Code Cell ---
df_sauces = pd.DataFrame(all_products)


# --- Code Cell ---
df_sauces


# --- Code Cell ---
# Navigate to the first subcategory - "Rice, Pasta, and Starches"

time.sleep(3)

subcategory_url = "https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/pates-riz-et-feculents"

driver.get(subcategory_url)

print("Navigated to subcategory: Rice, Pasta, and Starches")


# --- Code Cell ---
try:

    reject_button = WebDriverWait(driver, 10).until(

        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Tout accepter')]"))

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

    'pasta':     'https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/pates-riz-et-feculents/pates',

    'rice':    'https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/pates-riz-et-feculents/riz',

    'couscous, wheat and dried vegetables':'https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/pates-riz-et-feculents/couscous-ble-legumes-secs',

    'mashed potatoes and polenta':'https://www.carrefour.fr/r/bio-et-ecologie/epicerie-salee/pates-riz-et-feculents/puree-polenta'

}


# --- Code Cell ---
all_products = []


# --- Code Cell ---
for sub_name, sub_url in subcategories.items():

    print(f"\n=== Scraping sub-category: {sub_name} ===")

    driver.get(sub_url)



    # 3) Wait for the product grid to appear

    WebDriverWait(driver, 15).until(

        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product-list-grid"))

    )



    # 4) Click “Afficher les produits suivants” until it's gone / no new items

    while True:

        try:

            btn = WebDriverWait(driver, 5).until(

                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.pagination__button-wrap button"))

            )

        except:

            print(" • no more load-more button")

            break



        before_count = len(driver.find_elements(

            By.CSS_SELECTOR, "ul.product-list-grid > li.product-list-grid__item"

        ))



        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)

        time.sleep(0.5)

        try:

            btn.click()

        except ElementClickInterceptedException:

            driver.execute_script("arguments[0].click();", btn)



        print(f" • clicked load-more (had {before_count} items)…")



        # wait for new items to appear

        try:

            WebDriverWait(driver, 10).until(

                lambda d: len(d.find_elements(

                    By.CSS_SELECTOR, "ul.product-list-grid > li.product-list-grid__item"

                )) > before_count

            )

            print("   → new items loaded")

            time.sleep(0.5)

        except:

            print("   → timed out waiting for new items")

            break



    # 5) Scrape all loaded items

    items = driver.find_elements(

        By.CSS_SELECTOR, "ul.product-list-grid > li.product-list-grid__item"

    )

    print(f" • total products found: {len(items)}")



    for it in items:

        # URL & SKU

        a = it.find_element(By.TAG_NAME, "a")

        href = a.get_attribute("href")

        m = re.search(r"(\d{7,})", href or "")

        sku = m.group(1) if m else ""



        # Name

        name = it.find_element(By.TAG_NAME, "h3").text.strip()



        # Unit Size: primary selector → fallback to the packaging caption, then regex-extract only the number+unit

        unit = ""

        try:

            unit = it.find_element(

                By.CSS_SELECTOR,

                ".ds-format.product-list-card-plp-grid__shimzone--small"

            ).text.strip()

        except:

            try:

                raw = it.find_element(

                    By.CSS_SELECTOR,

                    "span.product-list-card-plp-grid__packaging"

                ).text.strip()

                # extract only the number+unit, e.g. "1L", "250mL"

                match = re.search(r"(\d+(?:[.,]\d+)?\s*[A-Za-z]+)", raw)

                unit = match.group(1) if match else raw

            except:

                unit = ""



        all_products.append({

            "SKU":            sku,

            "Product Name":   name,

            "Category":       "rice, pasta, and starches",

            "Sub-Category":   sub_name,

            "Unit Size":      unit,

            "URL":            href

        })


# --- Code Cell ---
df_rice = pd.DataFrame(all_products)


# --- Code Cell ---
df_rice


df_soup = df_soup.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_rice = df_rice.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_sauces = df_sauces.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)


# --- Code Cell ---
df_final = pd.concat([df_soup, df_sauces, df_rice], ignore_index=True)


# --- Code Cell ---
# get today’s date as a string, e.g. "2025-06-14"

today_str = datetime.date.today().isoformat()


# --- Code Cell ---
# add the new column

df_final['Date of Scraping'] = today_str


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
filename = f"carrefour_products_{datetime.datetime.now():%Y%m%d}.xlsx"

df_final.to_excel(os.path.join(data_folder, filename), index=False)


# --- Code Cell ---


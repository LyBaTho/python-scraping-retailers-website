#!/usr/bin/env python
# coding: utf-8

# # CODE

# ## LIBRARIES

# In[1]:


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
from urllib.parse import urljoin
import os, sys
import openpyxl
import datetime
from pathlib import Path
from data_folder_setup import get_data_folder


# In[2]:


data_folder = get_data_folder()


# ## SCRAPING CODE

# ### CATEGORY

# In[3]:


# Step 1: Launch undetected Chrome
driver = uc.Chrome()

# Step 2: Go to AH homepage
driver.get("https://www.tesco.com/?msockid=25a5c8b31e7569da3068dd3c1fd96895")
time.sleep(3)


# In[4]:


# Step 3: Now go directly to the desired category URL
time.sleep(2)  # slight pause to stabilize session
driver.get("https://www.tesco.com/groceries/en-GB/shop/food-cupboard/all?_gl=1*tay54y*_up*MQ..*_ga*NzM3OTUzMTc4LjE3NTAzMzcwODI.*_ga_33B19D36CY*czE3NTAzMzcwODIkbzEkZzAkdDE3NTAzMzcwODIkajYwJGwwJGg5MzI0MzE3NTA.")
print("Navigated to category page.")


# ### SUB-CATEGORY

# #### Table Sauces, Olives, Pickles & Chutney

# In[5]:


# Navigate to the first subcategory - "Table Sauces, Olives, Pickles & Chutney"
time.sleep(3)
subcategory_url = "https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney?_gl=1*1c7xx78*_up*MQ..*_ga*OTg4Mzg1MTc0LjE3NTAzMzcxNzU.*_ga_33B19D36CY*czE3NTAzMzcxNzQkbzEkZzAkdDE3NTAzMzcxNzQkajYwJGwwJGgyMDk0ODMyNTI0"
driver.get(subcategory_url)
print("Navigated to subcategory: Table Sauces, Olives, Pickles & Chutney")


# In[6]:


# 1) Define your sub-categories
subcategories = {
    'salad cream':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/salad-cream?_gl=1*18cfr5k*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'tomato ketchup':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/tomato-ketchup?_gl=1*18cfr5k*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'mayonnaise':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/mayonnaise?_gl=1*18cfr5k*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'brown sauce':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/brown-sauce?_gl=1*17st4vw*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'sweet chilli & hot sauces':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/sweet-chilli-and-hot-sauces?_gl=1*17st4vw*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'bbq, burger, pizza sauces & marinades':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/bbq-burger-pizza-sauces-and-marinades?_gl=1*17st4vw*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'vegan mayo & vegan table sauces':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/vegan-mayo-and-vegan-table-sauces?_gl=1*17st4vw*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'mustard':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/mustard?_gl=1*bx1ke7*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'condiments, worcestershire & soy sauce':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/condiments-worcestershire-and-soy-sauce?_gl=1*bx1ke7*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'salad dressings, toppers & croutons':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/salad-dressings-toppers-and-croutons?_gl=1*94brfv*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'chutneys, relishes & pickles':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/chutneys-relishes-and-pickles?_gl=1*94brfv*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'pickled onions & pickled vegetables':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/pickled-onions-and-pickled-vegetables?_gl=1*94brfv*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'sundried tomatoes, capers & antipasti':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/sundried-tomatoes-capers-and-antipasti?_gl=1*94brfv*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'olives':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/olives?_gl=1*94brfv*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw',
    'christmas condiments & table sauces':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/table-sauces-olives-pickles-and-chutney/christmas-condiments-and-table-sauces?_gl=1*165x5pk*_up*MQ..*_ga*Mjk5NzE2ODgzLjE3NTIxNDQ5MDg.*_ga_33B19D36CY*czE3NTIxNDQ5MDgkbzEkZzAkdDE3NTIxNDQ5MDgkajYwJGwwJGgxNzYwMjI1MzQw'
}


# In[7]:


all_products = []


# In[8]:


for sub_name, sub_url in subcategories.items():
    print(f"\n=== Scraping sub-category: {sub_name} ===")
    page = 1

    while True:
        # build page URL (append &page=… if there’s already a ? in the URL)
        sep = "&" if "?" in sub_url else "?"
        url = f"{sub_url}{sep}page={page}&count=48"
        driver.get(url)

        # wait for the product grid
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul#list-content"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "ul#list-content > li[data-testid]")
        print(f" • Page {page}: found {len(items)} items")
        if not items:
            break

        for it in items:
            # — product link & SKU
            link_elem = it.find_element(By.CSS_SELECTOR, "h2 a")
            name = link_elem.text.strip()
            href = link_elem.get_attribute("href")
            full_url = urljoin("https://www.tesco.com", href)
            m = re.search(r"(\d{7,})", full_url)
            sku = m.group(1) if m else ""

            # — extract unit size from the product title (e.g. “665G”)
            unit = ""
            match = re.search(r"(\d+(?:[.,]\d+)?\s*(?:G|KG|ML|L))", name, re.IGNORECASE)
            if match:
                unit = match.group(1).upper().replace(" ", "")

            all_products.append({
                "SKU":           sku,
                "Product Name":  name,
                "Category":      "table sauces, olives, pickles & chutney",
                "Sub-Category":  sub_name,
                "Unit Size":     unit,
                "URL":           full_url,
            })

        # — check for “Next page” link
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a[data-testid='next']")
            if next_btn.get_attribute("aria-disabled") == "true":
                print(" • No more pages.")
                break
            page += 1
            time.sleep(1 + page * 0.1)  # gentle ramp-up delay
        except NoSuchElementException:
            print(" • Next-button not found, stopping.")
            break

print(f"\n✦ Done: scraped {len(all_products)} total products")


# In[ ]:


df_sauces = pd.DataFrame(all_products)


# In[ ]:


df_sauces


# In[ ]:


df_sauces.duplicated().any()


# In[ ]:


dupes = df_sauces[df_sauces.duplicated(keep=False)]


# In[ ]:


dupes


# In[ ]:


df_sauces = df_sauces.drop_duplicates(keep='first').reset_index(drop=True)


# In[ ]:


df_sauces


# #### Instant Noodles & Easy Meals
# 

# In[ ]:


# Navigate to the first subcategory - "Noodles"
time.sleep(3)
subcategory_url = "https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals?_gl=1*65w20v*_up*MQ..*_ga*OTg4Mzg1MTc0LjE3NTAzMzcxNzU.*_ga_33B19D36CY*czE3NTAzMzcxNzQkbzEkZzAkdDE3NTAzMzcxNzQkajYwJGwwJGgyMDk0ODMyNTI0"
driver.get(subcategory_url)
print("Navigated to subcategory: Instant Noodles & Easy Meals")


# In[ ]:


# 1) Define your sub-categories
subcategories = {
    'easy meals':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/easy-meals?_gl=1*unb2w7*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..',
    'authentic & asian inspired noodles':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/authentic-and-asian-inspired-noodles?_gl=1*1ob5zhg*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..',
    'instant noodle pots':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/instant-noodle-pots?_gl=1*1ob5zhg*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..',
    'instant pasta pots':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/instant-pasta-pots?_gl=1*1ob5zhg*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..',
    'instant packet noodles':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/instant-packet-noodles?_gl=1*1ob5zhg*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..',
    'instant rice pots':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/instant-rice-pots?_gl=1*1ouv8kg*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..',
    'instant packet & pouch pasta':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/instant-packet-and-pouch-pasta?_gl=1*1ouv8kg*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..',
    'instant packet & pouch rice':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/instant-packet-and-pouch-rice?_gl=1*1ouv8kg*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..',
    'cup meals & soups':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/cup-meals-and-soups?_gl=1*1ouv8kg*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..',
    'vegan & vegetarian':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/instant-noodles-and-easy-meals/vegan-and-vegetarian?_gl=1*1ouv8kg*_up*MQ..*_ga*MTQ5MzU5OTE5My4xNzUyMTQ1MjQ2*_ga_33B19D36CY*czE3NTIxNDUyNDUkbzEkZzAkdDE3NTIxNDUyNDUkajYwJGwwJGg1MTEyMjgyMQ..'
}


# In[ ]:


all_products = []


# In[ ]:


for sub_name, sub_url in subcategories.items():
    print(f"\n=== Scraping sub-category: {sub_name} ===")
    page = 1

    while True:
        # build page URL (append &page=… if there’s already a ? in the URL)
        sep = "&" if "?" in sub_url else "?"
        url = f"{sub_url}{sep}page={page}&count=48"
        driver.get(url)

        # wait for the product grid
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul#list-content"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "ul#list-content > li[data-testid]")
        print(f" • Page {page}: found {len(items)} items")
        if not items:
            break

        for it in items:
            # — product link & SKU
            link_elem = it.find_element(By.CSS_SELECTOR, "h2 a")
            name = link_elem.text.strip()
            href = link_elem.get_attribute("href")
            full_url = urljoin("https://www.tesco.com", href)
            m = re.search(r"(\d{7,})", full_url)
            sku = m.group(1) if m else ""

            # — extract unit size from the product title (e.g. “665G”)
            unit = ""
            match = re.search(r"(\d+(?:[.,]\d+)?\s*(?:G|KG|ML|L))", name, re.IGNORECASE)
            if match:
                unit = match.group(1).upper().replace(" ", "")

            all_products.append({
                "SKU":           sku,
                "Product Name":  name,
                "Category":      "instant noodles & easy meals",
                "Sub-Category":  sub_name,
                "Unit Size":     unit,
                "URL":           full_url,
            })

        # — check for “Next page” link
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a[data-testid='next']")
            if next_btn.get_attribute("aria-disabled") == "true":
                print(" • No more pages.")
                break
            page += 1
            time.sleep(1 + page * 0.1)  # gentle ramp-up delay
        except NoSuchElementException:
            print(" • Next-button not found, stopping.")
            break

print(f"\n✦ Done: scraped {len(all_products)} total products")


# In[ ]:


df_noodles = pd.DataFrame(all_products)


# In[ ]:


df_noodles.duplicated().any()


# In[ ]:


dupes = df_noodles[df_noodles.duplicated(keep=False)]


# In[ ]:


dupes


# In[ ]:


df_noodles = df_noodles.drop_duplicates(keep='first').reset_index(drop=True)


# #### Cooking Ingredients
# 

# In[ ]:


# Navigate to the first subcategory - "Cooking Ingredients"
time.sleep(3)
subcategory_url = "https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients?_gl=1*65w20v*_up*MQ..*_ga*OTg4Mzg1MTc0LjE3NTAzMzcxNzU.*_ga_33B19D36CY*czE3NTAzMzcxNzQkbzEkZzAkdDE3NTAzMzcxNzQkajYwJGwwJGgyMDk0ODMyNTI0"
driver.get(subcategory_url)
print("Navigated to subcategory: Cooking Ingredients")


# In[ ]:


# 1) Define your sub-categories
subcategories = {
    'gravy, stuffing & breadcrumbs':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients/gravy-stuffing-and-breadcrumbs?_gl=1*r1i4gg*_up*MQ..*_ga*MTM1ODA0NDA3My4xNzUyMTQ1NTM0*_ga_33B19D36CY*czE3NTIxNDU1MzMkbzEkZzAkdDE3NTIxNDU1MzMkajYwJGwwJGg4ODM3OTczNDQ.',
    'oils & cooking fats':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients/oils-and-cooking-fats?_gl=1*r1i4gg*_up*MQ..*_ga*MTM1ODA0NDA3My4xNzUyMTQ1NTM0*_ga_33B19D36CY*czE3NTIxNDU1MzMkbzEkZzAkdDE3NTIxNDU1MzMkajYwJGwwJGg4ODM3OTczNDQ.',
    'packet sauces, mixes & cook in a bag':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients/packet-sauces-mixes-and-cook-in-a-bag?_gl=1*rlr1sk*_up*MQ..*_ga*MTM1ODA0NDA3My4xNzUyMTQ1NTM0*_ga_33B19D36CY*czE3NTIxNDU1MzMkbzEkZzAkdDE3NTIxNDU1MzMkajYwJGwwJGg4ODM3OTczNDQ.',
    'marinades & seasoning kits':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients/marinades-and-seasoning-kits?_gl=1*rlr1sk*_up*MQ..*_ga*MTM1ODA0NDA3My4xNzUyMTQ1NTM0*_ga_33B19D36CY*czE3NTIxNDU1MzMkbzEkZzAkdDE3NTIxNDU1MzMkajYwJGwwJGg4ODM3OTczNDQ.',
    'salt & pepper':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients/salt-and-pepper?_gl=1*rlr1sk*_up*MQ..*_ga*MTM1ODA0NDA3My4xNzUyMTQ1NTM0*_ga_33B19D36CY*czE3NTIxNDU1MzMkbzEkZzAkdDE3NTIxNDU1MzMkajYwJGwwJGg4ODM3OTczNDQ.',
    'seasoning, herbs & spices':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients/seasoning-herbs-and-spices?_gl=1*rlr1sk*_up*MQ..*_ga*MTM1ODA0NDA3My4xNzUyMTQ1NTM0*_ga_33B19D36CY*czE3NTIxNDU1MzMkbzEkZzAkdDE3NTIxNDU1MzMkajYwJGwwJGg4ODM3OTczNDQ.',
    'stock cubes & pots':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients/stock-cubes-and-pots?_gl=1*1mwx1ef*_up*MQ..*_ga*MTM1ODA0NDA3My4xNzUyMTQ1NTM0*_ga_33B19D36CY*czE3NTIxNDU1MzMkbzEkZzAkdDE3NTIxNDU1MzMkajYwJGwwJGg4ODM3OTczNDQ.',
    'vinegars':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients/vinegars?_gl=1*1mwx1ef*_up*MQ..*_ga*MTM1ODA0NDA3My4xNzUyMTQ1NTM0*_ga_33B19D36CY*czE3NTIxNDU1MzMkbzEkZzAkdDE3NTIxNDU1MzMkajYwJGwwJGg4ODM3OTczNDQ.',
    'speciality ingredients':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-ingredients/speciality-ingredients?_gl=1*1mwx1ef*_up*MQ..*_ga*MTM1ODA0NDA3My4xNzUyMTQ1NTM0*_ga_33B19D36CY*czE3NTIxNDU1MzMkbzEkZzAkdDE3NTIxNDU1MzMkajYwJGwwJGg4ODM3OTczNDQ.'
}


# In[ ]:


all_products = []


# In[ ]:


for sub_name, sub_url in subcategories.items():
    print(f"\n=== Scraping sub-category: {sub_name} ===")
    page = 1

    while True:
        # build page URL (append &page=… if there’s already a ? in the URL)
        sep = "&" if "?" in sub_url else "?"
        url = f"{sub_url}{sep}page={page}&count=48"
        driver.get(url)

        # wait for the product grid
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul#list-content"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "ul#list-content > li[data-testid]")
        print(f" • Page {page}: found {len(items)} items")
        if not items:
            break

        for it in items:
            # — product link & SKU
            link_elem = it.find_element(By.CSS_SELECTOR, "h2 a")
            name = link_elem.text.strip()
            href = link_elem.get_attribute("href")
            full_url = urljoin("https://www.tesco.com", href)
            m = re.search(r"(\d{7,})", full_url)
            sku = m.group(1) if m else ""

            # — extract unit size from the product title (e.g. “665G”)
            unit = ""
            match = re.search(r"(\d+(?:[.,]\d+)?\s*(?:G|KG|ML|L))", name, re.IGNORECASE)
            if match:
                unit = match.group(1).upper().replace(" ", "")

            all_products.append({
                "SKU":           sku,
                "Product Name":  name,
                "Category":      "cooking ingredients",
                "Sub-Category":  sub_name,
                "Unit Size":     unit,
                "URL":           full_url,
            })

        # — check for “Next page” link
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a[data-testid='next']")
            if next_btn.get_attribute("aria-disabled") == "true":
                print(" • No more pages.")
                break
            page += 1
            time.sleep(1 + page * 0.1)  # gentle ramp-up delay
        except NoSuchElementException:
            print(" • Next-button not found, stopping.")
            break

print(f"\n✦ Done: scraped {len(all_products)} total products")


# In[ ]:


df_cooking_ing = pd.DataFrame(all_products)


# In[ ]:


df_cooking_ing.duplicated().any()


# In[ ]:


df_cooking_ing = df_cooking_ing.drop_duplicates(keep='first').reset_index(drop=True)


# #### Cooking Sauces, Meal Kits & Sides
# 

# In[ ]:


# Navigate to the first subcategory - "Cooking Sauces, Meal Kits & Sides"
time.sleep(3)
subcategory_url = "https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides?_gl=1*65w20v*_up*MQ..*_ga*OTg4Mzg1MTc0LjE3NTAzMzcxNzU.*_ga_33B19D36CY*czE3NTAzMzcxNzQkbzEkZzAkdDE3NTAzMzcxNzQkajYwJGwwJGgyMDk0ODMyNTI0"
driver.get(subcategory_url)
print("Navigated to subcategory: Cooking Sauces, Meal Kits & Sides")


# In[ ]:


# 1) Define your sub-categories
subcategories = {
    'chinese':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/chinese?_gl=1*8wcl7h*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'curry pastes':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/curry-pastes?_gl=1*p0osyc*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'free from':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/free-from?_gl=1*p0osyc*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'indian':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/indian?_gl=1*p0osyc*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'italian':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/italian?_gl=1*p0osyc*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'meal kits':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/meal-kits?_gl=1*p0osyc*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'mexican & latin american':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/mexican-and-latin-american?_gl=1*1trgvmf*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'middle eastern':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/middle-eastern?_gl=1*1trgvmf*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'packet mix & traditional sauces':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/packet-mix-and-traditional-sauces?_gl=1*1trgvmf*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'thai':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/thai?_gl=1*1trgvmf*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'japanese':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/japanese?_gl=1*1ubq02b*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'korean':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/korean?_gl=1*1ubq02b*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'american':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/american?_gl=1*1ubq02b*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5',
    'vegan':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/cooking-sauces-meal-kits-and-sides/vegan?_gl=1*1ubq02b*_up*MQ..*_ga*MjA2MTM2OTgxNi4xNzUyMTQ1Nzkz*_ga_33B19D36CY*czE3NTIxNDU3OTIkbzEkZzAkdDE3NTIxNDU3OTIkajYwJGwwJGgxNjExNzQxNzg5'
}


# In[ ]:


all_products = []


# In[ ]:


for sub_name, sub_url in subcategories.items():
    print(f"\n=== Scraping sub-category: {sub_name} ===")
    page = 1

    while True:
        # build page URL (append &page=… if there’s already a ? in the URL)
        sep = "&" if "?" in sub_url else "?"
        url = f"{sub_url}{sep}page={page}&count=48"
        driver.get(url)

        # wait for the product grid
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul#list-content"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "ul#list-content > li[data-testid]")
        print(f" • Page {page}: found {len(items)} items")
        if not items:
            break

        for it in items:
            # — product link & SKU
            link_elem = it.find_element(By.CSS_SELECTOR, "h2 a")
            name = link_elem.text.strip()
            href = link_elem.get_attribute("href")
            full_url = urljoin("https://www.tesco.com", href)
            m = re.search(r"(\d{7,})", full_url)
            sku = m.group(1) if m else ""

            # — extract unit size from the product title (e.g. “665G”)
            unit = ""
            match = re.search(r"(\d+(?:[.,]\d+)?\s*(?:G|KG|ML|L))", name, re.IGNORECASE)
            if match:
                unit = match.group(1).upper().replace(" ", "")

            all_products.append({
                "SKU":           sku,
                "Product Name":  name,
                "Category":      "cooking sauces, meal kits & sides",
                "Sub-Category":  sub_name,
                "Unit Size":     unit,
                "URL":           full_url,
            })

        # — check for “Next page” link
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a[data-testid='next']")
            if next_btn.get_attribute("aria-disabled") == "true":
                print(" • No more pages.")
                break
            page += 1
            time.sleep(1 + page * 0.1)  # gentle ramp-up delay
        except NoSuchElementException:
            print(" • Next-button not found, stopping.")
            break

print(f"\n✦ Done: scraped {len(all_products)} total products")


# In[ ]:


df_cooking_sauces = pd.DataFrame(all_products)


# In[ ]:


df_cooking_sauces.duplicated().any()


# In[ ]:


df_cooking_sauces = df_cooking_sauces.drop_duplicates(keep='first').reset_index(drop=True)


# #### Dried Pasta, Rice, Noodles & Cous Cous
# 

# In[ ]:


# Navigate to the first subcategory - "Dried Pasta, Rice, Noodles & Cous Cous"
time.sleep(3)
subcategory_url = "https://www.tesco.com/groceries/en-GB/shop/food-cupboard/dried-pasta-rice-noodles-and-cous-cous?_gl=1*18pdtq4*_up*MQ..*_ga*OTg4Mzg1MTc0LjE3NTAzMzcxNzU.*_ga_33B19D36CY*czE3NTAzMzcxNzQkbzEkZzAkdDE3NTAzMzcxNzQkajYwJGwwJGgyMDk0ODMyNTI0"
driver.get(subcategory_url)
print("Navigated to subcategory: Dried Pasta, Rice, Noodles & Cous Cous")


# In[ ]:


# 1) Define your sub-categories
subcategories = {
    'pasta & spaghetti':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/dried-pasta-rice-noodles-and-cous-cous/pasta-and-spaghetti?_gl=1*1fqwhc4*_up*MQ..*_ga*MTgwMDgyMDYyLjE3NTIxNDYwMDI.*_ga_33B19D36CY*czE3NTIxNDYwMDIkbzEkZzAkdDE3NTIxNDYwMDIkajYwJGwwJGg2MjcwODg1Mjg.',
    'wholewheat, organic & free from':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/dried-pasta-rice-noodles-and-cous-cous/wholewheat-organic-and-free-from?_gl=1*1fqwhc4*_up*MQ..*_ga*MTgwMDgyMDYyLjE3NTIxNDYwMDI.*_ga_33B19D36CY*czE3NTIxNDYwMDIkbzEkZzAkdDE3NTIxNDYwMDIkajYwJGwwJGg2MjcwODg1Mjg.',
    'cous cous':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/dried-pasta-rice-noodles-and-cous-cous/cous-cous?_gl=1*2p5nm7*_up*MQ..*_ga*MTgwMDgyMDYyLjE3NTIxNDYwMDI.*_ga_33B19D36CY*czE3NTIxNDYwMDIkbzEkZzAkdDE3NTIxNDYwMDIkajYwJGwwJGg2MjcwODg1Mjg.',
    'noodles':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/dried-pasta-rice-noodles-and-cous-cous/noodles?_gl=1*2p5nm7*_up*MQ..*_ga*MTgwMDgyMDYyLjE3NTIxNDYwMDI.*_ga_33B19D36CY*czE3NTIxNDYwMDIkbzEkZzAkdDE3NTIxNDYwMDIkajYwJGwwJGg2MjcwODg1Mjg.',
    'rice':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/dried-pasta-rice-noodles-and-cous-cous/rice?_gl=1*1gvjz9o*_up*MQ..*_ga*MTgwMDgyMDYyLjE3NTIxNDYwMDI.*_ga_33B19D36CY*czE3NTIxNDYwMDIkbzEkZzAkdDE3NTIxNDYwMDIkajYwJGwwJGg2MjcwODg1Mjg.',
    'plain microwave rice':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/dried-pasta-rice-noodles-and-cous-cous/plain-microwave-rice?_gl=1*1gvjz9o*_up*MQ..*_ga*MTgwMDgyMDYyLjE3NTIxNDYwMDI.*_ga_33B19D36CY*czE3NTIxNDYwMDIkbzEkZzAkdDE3NTIxNDYwMDIkajYwJGwwJGg2MjcwODg1Mjg.',
    'flavoured microwave rice':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/dried-pasta-rice-noodles-and-cous-cous/flavoured-microwave-rice?_gl=1*1gvjz9o*_up*MQ..*_ga*MTgwMDgyMDYyLjE3NTIxNDYwMDI.*_ga_33B19D36CY*czE3NTIxNDYwMDIkbzEkZzAkdDE3NTIxNDYwMDIkajYwJGwwJGg2MjcwODg1Mjg.',
    'lentils, grains & pulses':'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/dried-pasta-rice-noodles-and-cous-cous/lentils-grains-and-pulses?_gl=1*1gvjz9o*_up*MQ..*_ga*MTgwMDgyMDYyLjE3NTIxNDYwMDI.*_ga_33B19D36CY*czE3NTIxNDYwMDIkbzEkZzAkdDE3NTIxNDYwMDIkajYwJGwwJGg2MjcwODg1Mjg.'
}


# In[ ]:


all_products = []


# In[ ]:


for sub_name, sub_url in subcategories.items():
    print(f"\n=== Scraping sub-category: {sub_name} ===")
    page = 1

    while True:
        # build page URL (append &page=… if there’s already a ? in the URL)
        sep = "&" if "?" in sub_url else "?"
        url = f"{sub_url}{sep}page={page}&count=48"
        driver.get(url)

        # wait for the product grid
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul#list-content"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "ul#list-content > li[data-testid]")
        print(f" • Page {page}: found {len(items)} items")
        if not items:
            break

        for it in items:
            # — product link & SKU
            link_elem = it.find_element(By.CSS_SELECTOR, "h2 a")
            name = link_elem.text.strip()
            href = link_elem.get_attribute("href")
            full_url = urljoin("https://www.tesco.com", href)
            m = re.search(r"(\d{7,})", full_url)
            sku = m.group(1) if m else ""

            # — extract unit size from the product title (e.g. “665G”)
            unit = ""
            match = re.search(r"(\d+(?:[.,]\d+)?\s*(?:G|KG|ML|L))", name, re.IGNORECASE)
            if match:
                unit = match.group(1).upper().replace(" ", "")

            all_products.append({
                "SKU":           sku,
                "Product Name":  name,
                "Category":      "dried pasta, rice, noodles & cous cous",
                "Sub-Category":  sub_name,
                "Unit Size":     unit,
                "URL":           full_url,
            })

        # — check for “Next page” link
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a[data-testid='next']")
            if next_btn.get_attribute("aria-disabled") == "true":
                print(" • No more pages.")
                break
            page += 1
            time.sleep(1 + page * 0.1)  # gentle ramp-up delay
        except NoSuchElementException:
            print(" • Next-button not found, stopping.")
            break

print(f"\n✦ Done: scraped {len(all_products)} total products")


# In[ ]:


df_pasta = pd.DataFrame(all_products)


# In[ ]:


df_pasta.duplicated().any()


# In[ ]:


df_pasta = df_pasta.drop_duplicates(keep='first').reset_index(drop=True)


# ## AGGREGATE

# In[ ]:


df_pasta = df_pasta.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_sauces = df_sauces.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_noodles = df_noodles.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_cooking_ing = df_cooking_ing.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)
df_cooking_sauces = df_cooking_sauces.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)


# In[ ]:


df_final = pd.concat([df_sauces, df_noodles, df_cooking_ing, df_cooking_sauces, df_pasta], ignore_index=True)


# In[ ]:


df_final.duplicated().any()


# In[ ]:


df_final = df_final.drop_duplicates(subset='SKU', keep='first').reset_index(drop=True)


# In[ ]:


# get today’s date as a string, e.g. "2025-06-14"
today_str = datetime.date.today().isoformat()


# In[ ]:


# add the new column
df_final['Date of Scraping'] = today_str


# In[ ]:


for col in ['Category', 'Sub-Category']:
    df_final[col] = df_final[col].str.lower()


# In[ ]:


driver.quit()


# In[ ]:


filename = f"tesco_products_{datetime.datetime.now():%Y%m%d}.xlsx"
df_final.to_excel(os.path.join(data_folder, filename), index=False)


# In[ ]:





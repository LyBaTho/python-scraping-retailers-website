#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pathlib import Path


# In[2]:


# Dynamically resolve root directories
try:
    code_dir = Path(__file__).parent
except NameError:
    code_dir = Path.cwd()

# Sources and Data root
sources_dir = code_dir.parent
data_root = sources_dir / "data"

# Master folder for aggregated outputs
master_folder = data_root / "master"
master_folder.mkdir(parents=True, exist_ok=True)

# # AH

# In[4]:


# Output file for stacked AH data
output_file = master_folder / "aggregate_data_ah.xlsx"


# In[5]:


# Step 1: Find all monthly folders, sorted by YYYY-MM
month_folders = sorted([f for f in data_root.iterdir() if f.is_dir() and f.name.lower() not in ["aggregate", "master"]])


# In[6]:


# Master DataFrame to stack all AH data
df_stack = pd.DataFrame()


# In[7]:


# Step 2: Loop through folders and stack AH files
for month_folder in month_folders:
    ah_files = list(month_folder.glob("ah_products_*.xlsx"))
    if not ah_files:
        print(f"Skipping {month_folder.name}, no AH data found.")
        continue

    df = pd.read_excel(ah_files[0])
    df_stack = pd.concat([df_stack, df], ignore_index=True)
    print(f"Added {len(df)} rows from {ah_files[0].name}")


# In[8]:


# Step 3: Save stacked file
df_stack.to_excel(output_file, index=False)
print(f"\n✅ Stacked AH data saved to: {output_file}")
print(f"Total rows stacked: {len(df_stack)}")


# # TESCO

# In[10]:


output_file = master_folder / "aggregate_data_tesco.xlsx"


# In[11]:


month_folders = sorted([f for f in data_root.iterdir() if f.is_dir() and f.name.lower() not in ["aggregate", "master"]])


# In[12]:


df_stack = pd.DataFrame()


# In[13]:


for month_folder in month_folders:
    tesco_files = list(month_folder.glob("tesco_products_*.xlsx"))
    if not tesco_files:
        print(f"Skipping {month_folder.name}, no Tesco data found.")
        continue

    df = pd.read_excel(tesco_files[0])
    df_stack = pd.concat([df_stack, df], ignore_index=True)
    print(f"Added {len(df)} rows from {tesco_files[0].name}")


# In[14]:


df_stack.to_excel(output_file, index=False)
print(f"\n✅ Stacked Tesco data saved to: {output_file}")
print(f"Total rows stacked: {len(df_stack)}")


# # CARREFOUR

# In[16]:


output_file = master_folder / "aggregate_data_carrefour.xlsx"


# In[17]:


month_folders = sorted([f for f in data_root.iterdir() if f.is_dir() and f.name.lower() not in ["aggregate", "master"]])


# In[18]:


df_stack = pd.DataFrame()


# In[19]:


for month_folder in month_folders:
    carrefour_files = list(month_folder.glob("carrefour_products_*.xlsx"))
    if not carrefour_files:
        print(f"Skipping {month_folder.name}, no Carrefour data found.")
        continue

    df = pd.read_excel(carrefour_files[0])
    df_stack = pd.concat([df_stack, df], ignore_index=True)
    print(f"Added {len(df)} rows from {carrefour_files[0].name}")


# In[20]:


df_stack.to_excel(output_file, index=False)
print(f"\n✅ Stacked Carrefour data saved to: {output_file}")
print(f"Total rows stacked: {len(df_stack)}")


# # TARGET

# In[22]:


output_file = master_folder / "aggregate_data_target.xlsx"


# In[23]:


month_folders = sorted([f for f in data_root.iterdir() if f.is_dir() and f.name.lower() not in ["aggregate", "master"]])


# In[24]:


df_stack = pd.DataFrame()


# In[25]:


for month_folder in month_folders:
    target_files = list(month_folder.glob("target_products_*.xlsx"))
    if not target_files:
        print(f"Skipping {month_folder.name}, no Target data found.")
        continue

    df = pd.read_excel(target_files[0])
    df_stack = pd.concat([df_stack, df], ignore_index=True)
    print(f"Added {len(df)} rows from {target_files[0].name}")


# In[26]:


df_stack.to_excel(output_file, index=False)
print(f"\n✅ Stacked Target data saved to: {output_file}")
print(f"Total rows stacked: {len(df_stack)}")


# In[ ]:





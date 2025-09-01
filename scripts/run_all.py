import os

print("=== Step 1: Setup Libraries ===")
os.system("python setup_libraries.py")

print("\n=== Step 2: Setup Data Folder ===")
os.system("python data_folder_setup.py")

print("\n=== Step 3: Run Scrapers ===")
os.system("python target.py")

os.system("python tesco.py")

os.system("python carrefour.py")

print("\n=== Step 4: Aggregate Data ===")
os.system("python aggregate_data.py")

print("\n=== Step 5: Summarize Data ===")
os.system("python tracking.py")


print("\n=== All tasks completed ===")

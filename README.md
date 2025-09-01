# 🛒 Retailer Website Scraping Project

Welcome to the **Retailer Website Scraping Project** repository! 🕸️  
This project demonstrates how to use Python to automate data collection from multiple retailer websites, building a reliable dataset for further analysis and reporting.

---

## 📖 Project Overview

This project involves:

1. **Web Scraping Pipelines**: Automated scripts built with Python (Selenium, BeautifulSoup, undetected-chromedriver) to extract product-level data from retailer websites.  
2. **Dynamic Content Handling**: Implemented scrolling and content loading techniques to capture complete product catalogs.  
3. **Data Captured**: SKU details such as product name, price, unit price, and product URL.  
4. **Data Storage**: Structured outputs saved into monthly datasets, later aggregated for analytics and dashboard reporting.  

🎯 This repository is ideal for demonstrating expertise in:
- Python Web Scraping  
- Data Collection Automation  

---

## 🚀 Project Requirements

#### Objective
Automate the collection of product data across retailer websites to build a consistent, analysis-ready dataset.

#### Specifications
- **Technology**: Python with Selenium, BeautifulSoup, and undetected-chromedriver.  
- **Data Collected**: Product SKU, name, price, unit price, and product URL.  
- **Automation**: Scripts handle dynamic loading and pagination to ensure full data coverage.  
- **Documentation**: Clear folder structure and code comments for maintainability.  

---

## 📂 Repository Structure
```
scraping-retailers-website-project/
│
├── datasets/                                                    
│   ├── carrefour_raw_data.png        
│   ├── carrefour_aggregated_data.png                 
│   ├── target_raw_data.png                
│   ├── target_aggregated_data.png           
│   ├── tesco_raw_data.png
│   ├── tesco_aggregated_data.png        
│
├── scripts/                           
│   ├── data_folder_setup/             
│   ├── setup_libraries/                 
│   ├── target/                           
│   ├── tesco/          
│   ├── carrefour/
│   ├── aggregate_data/
│   ├── run_all/
│
├── README.md
```

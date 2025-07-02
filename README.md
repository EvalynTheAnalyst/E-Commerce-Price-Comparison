# 🛍️ E-Commerce Price Comparison App (Jumia vs Kilimall)
![image](https://github.com/user-attachments/assets/10052092-c61f-46b0-95a4-a30e655914e1)


## 📌 Introduction

In the dynamic e-commerce space of **2025**, product prices fluctuate rapidly across platforms, sometimes within hours. Shoppers, procurement teams, and small business owners are constantly hunting for the **best deals**. Yet, manually checking prices across sites like **Jumia** and **Kilimall** is time-consuming, error-prone, and inefficient.

This project solves that by building an **automated price comparison and analysis app**. Powered by **web scraping, data cleaning, NLP-based fuzzy matching, and Streamlit dashboards**, this tool helps you:

- Scrape product prices from both platforms in real time
- Match similar products using text similarity (RapidFuzz)
- Analyze price trends and differences
- Spot the best deals
- Download comparison results instantly

---

## 🚀 Why Price Comparison Matters in 2025

In 2025:
- AI-assisted dynamic pricing is widely adopted by online retailers
- The same phone model can differ by **5–15%** across platforms
- Consumers and businesses expect **real-time insights** before making purchases

This app provides transparency, **saves money**, and enhances decision-making for anyone who shops online.

---

## 🧰 Technologies Used

- `Python` – core logic and data wrangling
- `BeautifulSoup + requests` – web scraping
- `Pandas + NumPy` – data analysis
- `RapidFuzz` – smart text-based product matching
- `Matplotlib` – visualizations
- `Streamlit` – interactive web dashboard

---

## 🔄 Project Workflow

Here's a step-by-step breakdown of how it all works:
```graph TD
  A[🌐 Scrape Data from Jumia & Kilimall] --> B[🗹 Clean & Standardize Product Info]
  B --> C[🔍 Match Similar Products using Fuzzy Matching]
  C --> D[📊 Analyze Price Differences]
  D --> E[📦 Build & Deploy Streamlit Dashboard]
```

### 1. 🕸️ Web Scraping

Two separate functions scrape product listings:
- `scrape_jumia()` fetches data from **Jumia Kenya**
- `scrape_kilimall()` fetches data from **Kilimall Kenya**

Each scraper extracts:
- Product name
- Price
- Discount (if available)
- Ratings and review count

### 2. 🧼 Data Cleaning

Raw data is cleaned using:
- `clean_jumia(df)` and `clean_kilimall(df1)`
- Non-numeric characters are stripped from prices
- Ratings and reviews are extracted using regex
- Missing entries are dropped

### 3. 🧠 Product Matching

We use **RapidFuzz** (a fast and accurate fuzzy string matcher) to pair similar products across platforms.

If their similarity score ≥ 85%, we assume it's a match and extract:
- Prices from both platforms
- Ratings and reviews
- Price difference

### 4. 📊 Data Visualization in Streamlit

Once matched:
- The app shows a **table of matched products**
- It plots a **histogram of price differences**
- It compares **average prices** between Jumia and Kilimall
- It highlights:
  -  Top 10 biggest price gaps
  -  Cheapest products
  - Highest priced item
- You can also **download results as a CSV**
  

### 5. 🌐 Deployment-Ready

To launch:
```bash
streamlit run your_script.py 
```
# 📩 Conclusion

This project shows how you can turn raw web data into intelligent shopping decisions — no manual comparison needed. It's a small but powerful example of how data skills can directly impact everyday life and help others.

Feel free to clone this repo, tweak it, or contribute!



from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy
import streamlit as st
import matplotlib.pyplot as plt 




base_url = "https://www.jumia.co.ke/all-products/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}
def scrape_jumia():
  page = 1

  # Initialize empty list to store product data
  all_products = []

  while True:
    print(f"Scraping page {page}...")
    url = f"{base_url}?page={page}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}, status code: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.select('article.prd')

    if not products:
        print("No more products found. Stopping.")
        break

    for product in products:
        name = product.select_one('div.name') or product.select_one('h3.name')
        price = product.select_one('div.prc')
        discount = product.select_one('div.bdg._dsct')
        reviews = product.select_one('div.rev')
        

        all_products.append({
            "name": name.text.strip() if name else None,
            "price": price.text.strip() if price else None,
            "discount": discount.text.strip() if discount else 0,
            "rate": reviews.text.strip() if reviews else "No ratings",
            
        })

    page += 1

  df = pd.DataFrame(all_products)
  return df


def scrape_kilimall():
    page = 1
    base_url = 'https://www.kilimall.co.ke/category/phones-accessories?id=872&form=category&source=category|allCategory|Phones%20&%20Accessories'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    all_products = []

    while True:
        print(f"Scraping Kilimall page {page}")
        url = f"{base_url}&page={page}"  # page param must be appended using &
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to load page {page}, status: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.select("div.listings div.listing-item")

        if not products:
            print("No more products found. Stopping.")
            break

        for prod in products:
            name = prod.select_one('p.product-title')
            price = prod.select_one('div.product-price')
            total_reviews= prod.select_one('div.rate')
            rate = prod.select_one('span.rate')

            all_products.append({
                "name": name.text.strip() if name else None,
                "price": price.text.strip() if price else None,
                "total_reviews": total_reviews.text.strip() if total_reviews else None,
                "rate" : rate.text.strip() if rate else 0
            })

        page += 1  # move to the next page

    df1 = pd.DataFrame(all_products)
    return df1



def clean_kilimall(df1):
    df1.dropna(subset = 'name')
    df1['price'] = df1['price'].str.replace(r'[^0-9.]', '', regex = True).astype(float)
    df1['total_reviews'] =pd.to_numeric(df1['total_reviews'].str.replace(r'[^0-9]', '', regex = True),errors='coerce')
    

    return df1

def clean_jumia(df):

    df.dropna(subset=['name'])
    df['price'] = df['price'].replace(r'[^0-9.]','', regex= True).astype(float)
    df['discount'] = df['discount'].replace(r'[^0-9]','', regex= True)
    df['ratings'] = df['rate'].str.extract(r'(\d+(?:\.\d+)?)').astype(float)
    df['total_reviews'] = pd.to_numeric(df['rate'].str.extract(r'\((\d+)\)')[0], errors='coerce')
   

    df = df.drop(columns='rate', errors='ignore')

    return df
    

from rapidfuzz import process, fuzz


def compare_products(kili_df, jumia_df, threshold=85):
    matches = []

    for idx, kili_name in enumerate(kili_df['name']):
        match, score, match_idx = process.extractOne(
            kili_name, jumia_df['name'], scorer=fuzz.token_sort_ratio
        )

        if score >= threshold:
            matches.append({
                'kilimall_name': kili_name,
                'jumia_name': match,
                'kilimall_price': kili_df.loc[idx, 'price'],
                'jumia_price': jumia_df.loc[match_idx, 'price'],
                'Kilimall_reviews':kili_df.loc[idx, 'total_reviews'],
                'jumia_reviews': jumia_df.loc[match_idx, 'total_reviews'],
                'price_difference': jumia_df.loc[match_idx, 'price'] - kili_df.loc[idx, 'price']

            })

    return pd.DataFrame(matches)

def connect_streamlit():

    st.set_page_config(page_title='Jumia vs Kilimall Phone Prices', layout='wide', page_icon='🛒')
    st.title("📦 E-Commerce Price Tracker")
    st.markdown('Compare and analyze the prices of your favourite product in **Jumia** and **Kilimall**')

    if st.button("Scrape Jumia and Kilimall"):
        with st.spinner("Scraping data..."):
            jumia_raw = scrape_jumia()
            kilimall_raw = scrape_kilimall()

            clean_j = clean_jumia(jumia_raw)
            clean_k = clean_kilimall(kilimall_raw)

            st.success("Scraping complete!!")

            matches = compare_products(clean_k, clean_j)

            st.markdown("### 📄 Matched Product Prices")
            st.dataframe(matches)

            st.markdown("### 📉 Histogram of Price Differences")
            fig1, ax1 = plt.subplots(figsize =(10,8))
            matches['price_difference'].plot(kind='hist', bins=10, ax=ax1, color='skyblue', edgecolor='black')
            ax1.set_xlabel("Price Difference (Jumia - Kilimall)")
            st.pyplot(fig1)

            # Average Prices
            st.markdown("### 📊 Average Price on Each Platform")
            avg_kili = matches['kilimall_price'].mean()
            avg_jumia = matches['jumia_price'].mean()
            fig2, ax2 = plt.subplots(figsize= (10,8))
            ax2.bar(['Kilimall', 'Jumia'], [avg_kili, avg_jumia], color=['blue', 'orange'])
            ax2.set_ylabel('Average Price (KES)')
            st.pyplot(fig2)

            #Highest Prices
            st.markdown("### 💰 Highest Product Price on Each Platform")
            max_jumia = matches.loc[matches['jumia_price'].idxmax()]
            max_kili = matches.loc[matches['kilimall_price'].idxmax()]
            st.markdown(f"**Jumia:** {max_jumia['jumia_name']} - KES {max_jumia['jumia_price']}")
            st.markdown(f"**Kilimall:** {max_kili['kilimall_name']} - KES {max_kili['kilimall_price']}")

            #  Top 10 Biggest Price Differences
            st.markdown("### 🔍 Top 10 Products with Largest Price Differences")
            top_diff = matches.reindex(matches['price_difference'].abs().sort_values(ascending=False).index).head(10)
            st.dataframe(top_diff[['kilimall_name', 'jumia_name', 'kilimall_price', 'jumia_price', 'price_difference']])


            # Cheapest Products
            st.markdown("### 💸 Top 5 Cheapest Products (Based on Kilimall)")
            cheapest = matches.sort_values(by='kilimall_price').head(5)
            st.dataframe(cheapest[['kilimall_name', 'jumia_name', 'kilimall_price', 'jumia_price', 'price_difference']])

            # Download
            st.download_button("📥 Download CSV", matches.to_csv(index=False), "price_comparison.csv", "text/csv")


if __name__ =="__main__":
    connect_streamlit()
    





#df = scrape_jumia()
#df1 = scrape_kilimall()

#if __name__ == '__main__':
   #jumia = clean_jumia(df)
   #kilimall = clean_kilimall(df1)
   #matched = compare_products(kilimall,jumia)

   #print(df1)
#    print(jumia.head(5))
#    print(kilimall.head(5))
#    print(matched.head())
#    print(matched.shape)







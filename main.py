from playwright.sync_api import sync_playwright
import os
import pandas as pd
import requests
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

def scrape_ctypto_currency_table(page):
    # Wait for the table to load
    page.wait_for_selector("div.ant-table-wrapper")
    page.wait_for_timeout(2000)
    
    # Extract table data
    rows = page.query_selector_all("div.ant-table-body table tbody tr")
    data = []
    for row in rows:
        cells = row.query_selector_all("td")
        row_data = [cell.inner_text().strip() for cell in cells]
        data.append(row_data)
    
    filtered_data = [row for row in data if len(row) == 13 and any(cell != '' for cell in row) and row[0] == '']
    print(filtered_data)
    columns = [
        "blank_column(not use)", "Ranking", "Symbol", "Price", "Price (24h%)", "Funding Rate", "Volume (24h)", "Volume (24h%)", "Market Cap", "OI", "OI (1h%)", "OI (24h%)", "Liquidation (24h)"
    ]
    df = pd.DataFrame(filtered_data, columns=columns)
    return df

def scrape_ctypto_category_table(page):
    # Wait for the table to load
    page.wait_for_selector("div.ant-table-wrapper.home-category-data-table")
    page.wait_for_timeout(2000)
    
    # Extract table data
    rows = page.query_selector_all("div.ant-table-body table tbody tr")
    data = []
    for row in rows:
        cells = row.query_selector_all("td")
        row_data = [cell.inner_text().strip() for cell in cells]
        data.append(row_data)
    
    filtered_data = [row for row in data if len(row) == 11 and any(cell != '' for cell in row)]
    columns = [
        "Ranking", "Categories", "Price (24h%)", "Funding Rate", "Volume (24h)", "Volume (24h%)", "Market Cap", "OI", "OI (1h%)", "OI (24h%)", "Liquidation (24h)"
    ]
    df = pd.DataFrame(filtered_data, columns=columns)
    return df


def scrape_coinglass_table():
    url = "https://www.coinglass.com"
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Go to the target URL
        page.goto(url)

        crypto_currency_df = scrape_ctypto_currency_table(page)
        # Wait for the checkbox to be visible
        page.wait_for_selector("input[class^='MuiCheckbox-input']")
        
        # Click the checkbox
        page.click("input[class^='MuiCheckbox-input']")
        crypto_category_df = scrape_ctypto_category_table(page)
        
        # Close browser
        browser.close()

        return crypto_currency_df, crypto_category_df

# Execute the function and print the data
crypto_currency_df, crypto_category_df = scrape_coinglass_table()
print(crypto_currency_df)
print(crypto_category_df)
# Convert DataFrame to JSON
crypto_currency_json_data = crypto_currency_df.to_json(orient='records')
crypto_category_json_data = crypto_category_df.to_json(orient='records')

print(crypto_currency_json_data)
print(crypto_category_json_data)
response = requests.post(os.getenv('WEBHOOK_URL'), data={'data': crypto_currency_json_data + crypto_category_json_data})
# Check the response
print(response.status_code)
print(response.text)
# Optional: Save to CSV
# df.to_csv("coinglass_data.csv", index=False)
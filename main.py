from playwright.sync_api import sync_playwright
import os
import pandas as pd
import requests
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

def scrape_coinglass_table():
    url = "https://www.coinglass.com"
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Go to the target URL
        page.goto(url)

        # Wait for the checkbox to be visible
        page.wait_for_selector("input[class^='MuiCheckbox-input']")
        
        # Click the checkbox
        page.click("input[class^='MuiCheckbox-input']")
       
        
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
        
        # Close browser
        browser.close()
        
    # Convert to pandas DataFrame for easier analysis
    print(data)
    filtered_data = [row for row in data if len(row) == 11 and any(cell != '' for cell in row)]
    columns = [
        "Ranking", "Categories", "Price (24h%)", "Funding Rate", "Volume (24h)", "Volume (24h%)", "Market Cap", "OI", "OI (1h%)", "OI (24h%)", "Liquidation (24h)"
    ]
    df = pd.DataFrame(filtered_data, columns=columns)
    return df

# Execute the function and print the data
df = scrape_coinglass_table()
print(df)
# Convert DataFrame to JSON
json_data = df.to_json(orient='records')
print(json_data)
response = requests.post(os.getenv('WEBHOOK_URL'), data={'data': json_data})
# Check the response
print(response.status_code)
print(response.text)
# Optional: Save to CSV
# df.to_csv("coinglass_data.csv", index=False)
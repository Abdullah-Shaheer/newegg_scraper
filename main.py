import json
import requests
from fake_useragent import UserAgent
import pandas as pd


products = []
# Set up UserAgent and headers
for i in range(1, 83):
    ua = UserAgent()
    url = f'https://www.newegg.com/store/api/PageDeals?originParams=%7B%22name%22%3A%22Newegg-Deals%22,%22id%22%3A%229447%22%7D&originQuery=%7B%7D&index={i}&from=www.newegg.com'
    headers = {
        "cookie": "NVTC=248326808.0001.5f75b2076.1730951365.1730951365.1730951365.1; NID=9D4M8O6I8O0M5z1j6I; NV_NVTCTIMESTAMP=1730951469; NE_STC_V1=1116a3db87915edaf052c754ce933bd59fe29fcf2029590741cf3346c105adac80bcc63d",
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }
    querystring = {
        "originParams": "{\"name\":\"Newegg-Deals\",\"id\":\"9447\"}",
        "originQuery": "{}",
        "index": f"{i}",
        "from": "www.newegg.com"
    }

    # Request data
    response = requests.get(url, headers=headers, params=querystring, timeout=10)

    # Check if request was successful
    if response.status_code == 200:
        print(f"Scraping Data from page {i}")
        data = response.json()
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            for item in data:
                in_stock = item.get('ItemCell', {}).get('Instock', None)
                final_price = f"{item.get('ItemCell', {}).get('FinalPrice', None)}$"
                unit_cost = f"{item.get('ItemCell', {}).get('UnitCost', None)}$"
                if in_stock is True:
                    in_stock = "Yes"
                product_details = {
                    "Product Number": item.get('ItemCell', {}).get('Item', None),
                    "Title": item.get('ItemCell', {}).get('Description', {}).get('Title', None),
                    "Short Title": item.get('ItemCell', {}).get('Description', {}).get('ShortTitle', None),
                    "Final Price": final_price,
                    "Unit Cost": unit_cost,
                    "In Stock": in_stock,
                    "Manufactory": item.get('ItemCell', {}).get('ItemManufactory', {}).get('Manufactory', None),
                    "Ship From Country Name": item.get('ItemCell', {}).get('ShipFromCountryName', None),
                    "Rating": item.get('ItemCell', {}).get('Review', {}).get('Rating', None),
                    "Number of Reviews": item.get('ItemCell', {}).get('Review', {}).get('HumanRating', None),
                    "Item Model": item.get('ItemCell', {}).get('Model', None),
                    "Shipping Charge": item.get('ItemCell', {}).get('ShippingCharge', None),
                    "Warranty ID": item.get('ItemCell', {}).get('Warranty', {}).get('WarrantyID', None),
                    "Warranty Name": item.get('ItemCell', {}).get('Warranty', {}).get('WarrantyName', None),
                    "Best Selling Ranking": item.get('ItemCell', {}).get('BestSellingRanking', None),
                    "Lowest Price 30 Days": f"{item.get('ItemCell', {}).get('LowestPrice30Days', None)}$",
                    "Item Length": item.get('ItemCell', {}).get('Length', None),
                    "Item Width": item.get('ItemCell', {}).get('Width', None),
                    "Item Height": item.get('ItemCell', {}).get('Height', None),
                    "Item Weight": item.get('ItemCell', {}).get('Weight', None),
                    "Country of Manufacture": item.get('ItemCell', {}).get('ItemManufactory', {}).get('CountryOfMfr',
                                                                                                      None),
                    "Limit Quantity": item.get('ItemCell', {}).get('LimitQuantity', None),
                    "Seller ID": item.get('ItemCell', {}).get('Seller', {}).get('SellerId', None),
                    "Seller Name": item.get('ItemCell', {}).get('Seller', {}).get('SellerName', None),
                    "Seller Rating": item.get('ItemCell', {}).get('Seller', {}).get('SellerRating', None),
                    "Seller Reviews": item.get('ItemCell', {}).get('Seller', {}).get('SellerReviewCount', None)
                }
                products.append(product_details)  # Add to the list of products

            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(products)
            print(df.head())
            df.to_excel('main_output.xlsx', index=False)
            df.to_csv('main_output.csv', index=False)
            with open("main_output.json", 'w', encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            print("Data format is not as expected.")
    else:
        print(f"Status Code Error:- {response.status_code} for page {i}")
# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(products)
print(df.head())
df.to_excel('main_output.xlsx', index=False)
df.to_csv('main_output.csv', index=False)
with open("main_output.json", 'w', encoding="utf-8") as file:
    json.dump(products, file, ensure_ascii=False, indent=4)

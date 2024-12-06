from bs4 import BeautifulSoup
import re
import pypyodbc as odbc
import subprocess
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Your SQL Server connection details
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'Jack\SQLEXPRESS'
DATABASE_NAME = 'SNKRS_Scraping'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

# Establish a connection to the database
connection = odbc.connect(connection_string)
cursor = connection.cursor()

# Function to create and return a new WebDriver instance
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=chrome_options)

# Create the driver instance
driver = create_driver()

try:
    driver.get('https://www.nike.com/my/launch?s=upcoming')

    # Get page source after dynamic content is loaded
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # Look for product links and images
    links = soup.find_all('a', {"data-qa": "product-card-link"})
    others = soup.find_all('img')

    # Loop over products
    for link, other in zip(links, others):

        # Extract Product Link
        product_link = f"https://nike.com{link.get('href')}"

        # Extract Picture URL
        pic_url = other.get('src', '')

        # Extract Name and SKU
        name_and_sku = other.get('alt', '')
        match = re.search(r"(.+?) \((\w+-\w+)\)", name_and_sku)
        
        if match:
            product_name = match.group(1).strip()
            sku = match.group(2).upper()
        else:
            continue

        # Navigate to individual product page
        driver.get(product_link)

        # Get page source after dynamic content is loaded
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # Extract Price and Release Date
        price_tag = soup.find('div', {'class': 'headline-5 pb6-sm fs14-sm fs16-md'})
        release_date_tag = soup.find('div', {'class': 'available-date-component'})

        price = price_tag.text if price_tag else 'Price not found'
        release_date = release_date_tag.text if release_date_tag else 'Release date not found'

        # Check if the SKU already exists in the table
        # Redundancy checking
        check_query = "SELECT COUNT(*) FROM SNKRS WHERE SKU = ?;"
        cursor.execute(check_query, (sku,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Insert the data into the SQL Server table
            insert_query = """
                INSERT INTO SNKRS (Name, ProductLink, PictureLink, SKU, ReleaseDate, Price)
                VALUES (?, ?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, (product_name, product_link, pic_url, sku, release_date, price))
            connection.commit()

            print('==============================================================================')
            print(f'Sending webhook for {product_name}...')

            shared_variables = {
                "product_name": product_name,
                "link": product_link,
                "pic_url": pic_url,
                "release_date": release_date,
                "sku": sku,
                "price": price
            }

            with open('SNKRS_dataSharing.json', 'w') as json_file:
                json.dump(shared_variables, json_file, indent=4)


            subprocess.run(['python', 'SNKRS_dataWebhookSending.py'], check=True)
            # Navigate back to the main upcoming page
            driver.get('https://www.nike.com/my/launch?s=upcoming')

        else:
            print('==============================================================================')
            print(f'Duplicate entry for SKU: {sku}. Skipping insertion.')
            print(f'Skipping webhook sending for this SKU: {sku}')
            print('==============================================================================')
            # Navigate back to the main upcoming page
            driver.get('https://www.nike.com/my/launch?s=upcoming')

    cursor.close()
    connection.close()
    
    print('==============================================================================')
    print('ALL SAVED TO DATABASE!')
    print('ALL WEBHOOK SENT!')
    print('==============================================================================')

finally:
    driver.quit()
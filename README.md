# SNKRS-Scrapping
## License
This code is licensed under the [Apache 2.0 License]. You are free to use, modify, and distribute it, as long as you attribute the original author.


## Introduction
The purpose of this project is to create a web scraper that extracts release details of upcoming sneakers from the Nike SNKRS website. The scraper will automate the process of gathering information about new sneaker releases, including launch dates, product descriptions, prices, and images. This tool is particularly useful for sneaker enthusiasts, collectors, and resellers who want to stay updated on upcoming drops without manually browsing the website.

The extracted data will be stored in a database, providing a structured and centralized source for easy access and retrieval. Additionally, the system will send real-time updates via webhooks to a Discord server, enabling instant notifications for new releases. With minor modifications, the scraper can be converted into a 24/7 website monitor by running it on a server, offering continuous updates without manual intervention. This makes it adaptable for both personal and community use, ensuring users never miss important sneaker drops.

## Short Description
SNKRS_dataScraping.py: Main code

SNKRS_dataLoading.py: Extract and save data into database. It includes validation to prevent duplicate entries by checking for existing SKUs before adding new data

SNKRS_dataWebhookSending.py: Convert data into information and send it to related discord channel via discohook

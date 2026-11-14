from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from Book_Category_Scrape import scrape_category

catalog_url = "https://books.toscrape.com/index.html"
page = requests.get(catalog_url)
page.raise_for_status()
soup = BeautifulSoup(page.content, "html.parser")

"""gathers category name and url and creates a csv filename, calls upon the scrape_category function, and prints a message confirming each category was saved; repeats for each category in URL"""
for link in soup.select("ul.nav.nav-list > li > ul a[href]"):
    category_name = link.get_text(" ", strip=True)
    category_url = urljoin(page.url, link["href"])
    csv_filename = f"{category_name}.csv"
    
    scrape_category(category_url, csv_filename)
    print(f"Saved {category_name} books to {csv_filename}")

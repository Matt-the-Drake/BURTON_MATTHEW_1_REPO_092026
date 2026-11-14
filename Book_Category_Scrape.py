import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
from Single_Book_Scrape import scrape_book

"""Locates where the CSV files will be saved (one directory above this script)"""
SCRIPT_DIR = Path(__file__).resolve().parent.parent / "books_csv"
SCRIPT_DIR.mkdir(exist_ok=True)

def scrape_category(category_url, csv_filename):
    all_books = []
    current_url = category_url

    """while loop that scrapes one category at a time, pulls the URL for the full category, makes the URL parsable"""
    while current_url:
        page = requests.get(current_url)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")

        """obtains each individual book URL address, joins the address with the page URL, calls upon the scrape_book function to scrape each book and append the information to all_books"""
        for link in soup.select("h3 a[href]"):
            book_url = urljoin(page.url, link["href"])
            all_books.append(scrape_book(book_url))

        """moves the "current_url" to the next URL in the list until there are none to pull information from, repeating and eventually stopping the while loop"""
        next_page = soup.select_one("li.next a[href]")
        current_url = urljoin(page.url, next_page["href"]) if next_page else None

    """gathers the path for the category CSV, creates a DataFrame, and saves it"""
    csv_path = SCRIPT_DIR / csv_filename
    pd.DataFrame(all_books).to_csv(csv_path, index=False)
    return all_books

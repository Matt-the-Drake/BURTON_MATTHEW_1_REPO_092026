import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import re

"""Locates where the images will be saved (one directory above this script)"""
IMAGE_DIR = Path(__file__).resolve().parent.parent / "book_images"

def scrape_book(book_url):
    """Assigns the book URL to a variable / checks to make sure the HTML page loaded correctly / allows for the content of the web page to be scraped from"""
    page = requests.get(book_url)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, 'html.parser')
    
    """table finds UPC code and prices, article finds the description and image source, safe_image_name removes characters that cannot be saved as a file name"""
    table = soup.find('table', class_="table table-striped")
    upc_code = table.find("th", string="UPC").find_next("td").get_text(strip=True)
    article = soup.find("article", class_="product_page")
    description = article.find_all('p')[3]
    image_src = article.find_all("div")[5].find("img")["src"]
    image_url = urljoin(page.url, image_src)
    image_name = article.find_all("div")[5].find("img")["alt"]
    safe_image_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", image_name).strip(" .")

    """Gets a directory, gets the extension of the image, creates the name for the image path, downloads the image itself, and writes it onto the file"""
    IMAGE_DIR.mkdir(exist_ok=True)
    image_extension = Path(urlsplit(image_url).path).suffix
    image_path = IMAGE_DIR / f"{safe_image_name}{image_extension}"
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    image_path.write_bytes(image_response.content)

    """
    returns all information gathered, which allows it to be all sorted into a csv file"""
    return{
        "Page URL": page.url,
        "UPC code": upc_code,
        "Book title": soup.find(class_="col-sm-6 product_main").find("h1").get_text(strip=True),
        "Price excluding tax": table.find("th", string="Price (excl. tax)").find_next("td").get_text(strip=True),
        "Price including tax": table.find("th", string="Price (incl. tax)").find_next("td").get_text(strip=True),
        "Quantity available": soup.find("p", class_="instock availability").get_text(strip=True),
        "Product description": description.get_text(strip=True),
        "Category": soup.find("ul", class_="breadcrumb").find_all("li")[3].get_text(strip=True),
        "Review rating": soup.find("p", class_="star-rating").get("class")[1],
        "Image URL": image_url,
        "Image file": str(image_path),
    }

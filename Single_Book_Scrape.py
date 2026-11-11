import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import re

#Locates where the images will be saved (the same file this script is in) and assigns it to a variable, which will be used later to save the images to the folder
IMAGE_DIR = Path(__file__).resolve().parent / "book_images"

#Creates a function to be called upon inside other codes
def scrape_book(book_url):
    #Gets the book url from codes this is used in
    page = requests.get(book_url)
    #checks whether the HTML page is loaded correctly and returns an error if so; if the page loads correctly then this does nothing
    page.raise_for_status()
    #allows for the content of the web page to be scraped from; also this part can be used to find book title, quantity available, category, and review
    soup = BeautifulSoup(page.content, 'html.parser')
    
    #looks inside soup to find the table that has information, specifically the UPC code and prices
    table = soup.find('table', class_="table table-striped")
    #looks inside table to find the td element, inside the th element with the text "UPC", and strips whitespace from the text
    upc_code = table.find("th", string="UPC").find_next("td").get_text(strip=True)
    #looks inside soup to find the article under "class_="product_page"" which will then be used to get the description and image source (src)
    article = soup.find("article", class_="product_page")
    #looks inside article to find the section that contains the description of the book
    description = article.find_all('p')[3]
    #looks inside article to find the image source within the file, which falls under the sixth div element of the article under the class "product_page"
    image_src = article.find_all("div")[5].find("img")["src"]
    #finds the URL for the image by joining the base url of the page with the image source
    image_url = urljoin(page.url, image_src)
    #looks inside article to find the image name from the alt attribute, inside the img tag, which is inside the sixth div tag
    image_name = article.find_all("div")[5].find("img")["alt"]
    #Removes characters that are not allowed in file names, replaces them with underscores, and saves the result to the variable safe_image_name
    safe_image_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", image_name).strip(" .")

    #Creates the directory for the images and saves it to the variable IMAGE_DIR. If the directory already exists, it will not raise an error.
    IMAGE_DIR.mkdir(exist_ok=True)
    #Obtains the file extension for the image from the URL path and saves it to the variable image_extension
    image_extension = Path(urlsplit(image_url).path).suffix
    #Creates the path for the image file using safe_image_name and image_extension and saves it to the variable image_path
    image_path = IMAGE_DIR / f"{safe_image_name}{image_extension}"
    #Sends an HTTP GET request to the image URL and saves the response to the variable image_response
    image_response = requests.get(image_url)
    #Detects if the image failed to download and will raise an error if it did
    image_response.raise_for_status()
    #Writes the image into the file, converting it from raw information into a picture that can be opened and viewed
    image_path.write_bytes(image_response.content)

    #returns all information gathered, which allows it to be all sorted into a csv file by a different code
    return{
        "Page URL": page.url,
        "UPC code": upc_code,
        #Finds the book title in the file, which falls under the h1 tag located under the class "col-sm-6 product_main"
        "Book title": soup.find(class_="col-sm-6 product_main").find("h1").get_text(strip=True),
        #Finds the prices, both excluding and including tax, located inside a table that is under either the "Price (excl. tax)" or "Price (incl. tax)" heading
        "Price excluding tax": table.find("th", string="Price (excl. tax)").find_next("td").get_text(strip=True),
        "Price including tax": table.find("th", string="Price (incl. tax)").find_next("td").get_text(strip=True),
        #Finds the quantity available by finding the p tag located under the class "instock availability"
        "Quantity available": soup.find("p", class_="instock availability").get_text(strip=True),
        #Obtains the description using the description variable
        "Product description": description.get_text(strip=True),
        #Locates the category by finding the fourth li element, located under the ul tag, located within the class "breadcrumb"
        "Category": soup.find("ul", class_="breadcrumb").find_all("li")[3].get_text(strip=True),
        #Finds the review rating by locating the second class, located under the p tag, located within the class "star-rating"
        "Review rating": soup.find("p", class_="star-rating").get("class")[1],
        "Image URL": image_url,
        #Provides the image path as a string so that the user can easily find and view the image
        "Image file": str(image_path),
    }

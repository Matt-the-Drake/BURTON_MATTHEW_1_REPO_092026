# Books To Scrape
## Overview
The purpose of this code is to scrape the website [Books To Scrape](https://books.toscrape.com/), obtain the requested information about every book on sale, and save them to CSV files according to category.
## How this code works
**The Three Parts:**  
There are three scripts that run to create this code: Single_Book_Scrape.py, Book_Category_Scrape.py, and Books_Full_Category.py  
- **Books_Full_Category.py**  pulls up the web page, gets the list of categories and their URLs, activates Book_Category_Scrape.py for each category one at a time, and prints a message for each category that has been saved to a CSV file.  
- **Book_Category_Scrape.py** uses the category URL received from Books_Full_Category.py, strips each book URL, calls upon Single_Book_Scrape.py to scrape information from each book one at a time, and saves the information from each book into a CSV file named for their category  
- **Single_Book_Scrape.py** uses the given book URLs to strip all requested information and returns it back to Book_Category_Scrape.py to be saved
## Installation
All three python codes (Single_Book_Scrape.py, Book_Category_Scrape.py, and Books_Full_Category.py) need to be saved to the same foler. When Books_Full_Category.py is run, two new folders will be created inside the same directory -- or selected if they already exist -- to save the pictures and the CSV files to.


# Books To Scrape
## Overview
The purpose of this code is to scrape the website [Books To Scrape](https://books.toscrape.com/), obtain the requested information about every book on sale, and save them to CSV files according to category.
## How this code works
**The Three Parts:**  
This application is made up of three scripts: Books_Full_Catalog.py, Book_Category_Scrape.py, and Single_Book_Scrape.py  
- **Books_Full_Catalog.py**: Pulls up the web page of the given URL, retrieves the list of categories and their URLs, calls upon Book_Category_Scrape.py for each category one at a time, and prints a confirmation message for each category after they successfully save.  
- **Book_Category_Scrape.py**: Uses the category URL to scrape each book URL, calls upon the Single_Book_Scrape.py function to gather data from every book in a category, and saves the information from each book into a CSV file named for their category  
- **Single_Book_Scrape.py**: Uses the given book URLs to extract information from all requested fields from an individual book and returns it back to Book_Category_Scrape.py
## Installing and Running the Code
All three python codes (Single_Book_Scrape.py, Book_Category_Scrape.py, and Books_Full_Catalog.py) need to be saved to the same foler. When Books_Full_Catalog.py is run, two new folders will be created -- or selected if they already exist -- inside the same directory to save the pictures and the CSV files to.

Open the file explorer to where the scripts were downloaded. Click in the address bar, type "cmd" and press Enter. This will open a command prompt for the current folder.  
Next we will create a virtual environment. We are naming it "env"; "env" is a common name used, but replace it with whatever name is desired. Copy and paste this text into the CMD file previously opened, changing the name as desired:  
```python -m venv env```  
Now to activate it, copy and past (changing env to any name chosen in the last step):  
```env\Scripts\activate.bat```  
Now to install requirements using the requirements.txt file:  
```pip install -r requirements.txt```  
To make sure the installation was successful, you can verify by entering:  
```pip list```  
and making sure that everything matches the requirements.txt file  
Finally, to run the code and get the information scraped from Books To Scrape, enter:  
```python Books_Full_Catalog.py```
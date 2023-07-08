# Import necessary libraries
#from urllib.request import urlopen
#from bs4 import BeautifulSoup as bs
#import mysql.connector as conn
#import csv
#import os

# replace xxxx with your sql user id and password
 sql = conn.connect(host="localhost", user="xxxx", password="xxxx") 

# Define the CSV file name and location
          csv_file = f"C:/Users/Documents/flipkart_data/{product}.csv"


Project Name:		 
	Flipkart_Review_Scraper

Project Description:

The Flipkart Product Review Extractor is a comprehensive web scraping project that allows users to extract and store product reviews from Flipkart's website. 
With this project, users can enter the name of the product they wish to search for, and the program will fetch the product details and reviews from Flipkart.

The program then fetches the product details and reviews from Flipkart's website.

The extracted review information can be stored in two ways: CSV (Comma-Separated Values) file or MySQL database. 

The program creates a CSV file in the specified location and saves the extracted review information in it. 

The program establishes a connection to the local MySQL server, Creates a database if it doesn't exist, and creates a table for storing the review information.

The project aims web scraping techniques and data storage capabilities, the Flipkart Product Review Extractor simplifies the process of gathering valuable insights from product reviews. 
Users can analyze the extracted data, perform sentiment analysis, identify trends, and make informed decisions based on customer feedback. 

The project empowers users with the ability to efficiently extract and store product reviews for various purposes, such as market research, 
competitor analysis, and customer sentiment analysis.


Flowchart

The code you provided is complete and it allows the user to CSV and SQL as the storage option for the extracted data. Here's a breakdown of the code:

1. Prompt the user to enter the product name.
2. Construct the Flipkart search URL for the entered product.
3. Import necessary libraries.
4. Open the URL and read the HTML content.
5. Parse the HTML content using BeautifulSoup.
6. Find all the product boxes in the HTML.
7. Prompt the user to choose the storage option (CSV or SQL).
8. For the CSV storage
   - Define the CSV file name and location.
   - Create the directory if it doesn't exist.
   - Create a CSV file for storing the extracted review information.
   - Perform web scraping and data extraction.
   - Append the review information to the CSV file.
   - Print a message indicating that the data is saved in the CSV file.
9. For the SQL storage:
   - Establish a MySQL connection.
   - Create a database if it doesn't exist.
   - Create a table to store the review information.
   - Perform web scraping and data extraction.
   - Insert the review information into the MySQL table.
   - Print a message indicating that the data is saved in the MySQL table.
   - Handle errors that may occur during the MySQL connection and table creation.
10. Handle the case of an invalid storage option.
11. Print the total number of extracted data.
 

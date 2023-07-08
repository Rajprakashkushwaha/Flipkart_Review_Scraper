# Prompt the user to enter the product name
product = input("Enter the product name:")
print("Welcome to Flipkart Web scraping with your searched items")

# Construct the Flipkart search URL for the entered product
flipkart_link = "https://www.flipkart.com/search?q=" + product

# Import necessary libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import mysql.connector as conn
import csv
import os

# Open the URL and read the HTML content
details = urlopen(flipkart_link).read()

# Parse the HTML content using BeautifulSoup
beautified_details = bs(details, "html.parser")

# Find all the product boxes in the HTML
all_product = beautified_details.find_all('div', {"class": "_13oc-S"})

# Define the CSV file name and location
csv_file = f"C:/Users/Raj/Documents/Python/Project/flipcart/condition/CSVFile/{product}.csv"

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(csv_file), exist_ok=True)

# Create a CSV file for storing the extracted review information
with open(csv_file, "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Price", "Certification", "Place", "Time", "Rating", "Short_review"])
    print(f"CSV file '{csv_file}' created.")

# Establish MySQL connection
try:
    sql = conn.connect(host="localhost", user="root", password="root")
    cursor = sql.cursor()
    site = "flipkart"  # Modify this according to your needs
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {site}")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {site}.{product} (product_name varchar(200), price varchar(25), person varchar(50), rating varchar(5), time varchar(20), certification varchar(50), place varchar(100), short_review varchar(200))")
    print("MySQL table created.")
except conn.Error as e:
    print(f"Error creating MySQL table: {e}")

count = 0

# Iterate through each product box to extract review information
for j in range(len(all_product)-3):
    lnk = "https://www.flipkart.com" + all_product[j].div.div.a["href"]
    single_product = urlopen(lnk)
    single_details = single_product.read()
    details_bt = bs(single_details, "html.parser")

    try:
        # Extract the product name from the details
        product_name = (details_bt.find_all("div", {"class": "aMaAEs"})[0].h1.text)[:110]
    except:
        product_name = "NO product"

    try:
        # Extract the price from the details
        x = details_bt.find_all("div", {"class": "aMaAEs"})[0]
        price = x.find_all("div", {"class": "_30jeq3 _16Jk6d"})[0].text
        price = price.replace(",", "") if "," in price else price    
    except:
        price = "NO price"

    # Find the review boxes in the details
    review_box = details_bt.find_all("div", {"class": "_16PBlm"})

    # Iterate through each review box to extract review information
    for i in range(len(review_box)-1):
        try:
            # Extract the name from the review box
            name = review_box[i].div.div.find_all("div", {"class": "row _3n8db9"})[0].div.p.text
        except:
            name = "No name"

        try:
            # Extract the certification from the review box
            certi = review_box[i].find_all("p", {"class": "_2mcZGG"})[0].text.split(",")[0]
        except:
            certi = "No certi"

        try:
            # Extract the place from the review box
            place = review_box[i].find_all("p", {"class": "_2mcZGG"})[0].text.split(",")[1].strip()
        except:
            place = "No place"

        try:
            # Extract the time from the review box
            time = review_box[i].find_all("p", {"class": "_2sc7ZR"})[1].text
            time = time.replace(",", "") if "," in time else time
        except:
            time = "No time"

        try:
            # Extract the rating from the review box
            rating = review_box[i].div.div.div.div.text
        except:
            rating = "No rating"

        try:
            # Extract the short review from the review box
            short_review = review_box[i].div.div.div.p.text
        except:
            short_review = "No review"

        # Append the review information to the CSV file
        with open(csv_file, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, price, certi, place, time, rating, short_review])

        # Insert the review information into the MySQL table
        try:
            sql = conn.connect(host="localhost", user="root", password="root")
            cursor = sql.cursor()
            s = f"INSERT INTO {site}.{product} VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            v = (product_name, price, name, rating, time, certi, place, short_review)
            cursor.execute(s, v)
            sql.commit()
        except conn.Error as e:
            print(f"Error inserting data into MySQL table: {e}")

        count += 1

# Print the total number of extracted data
print("Number of data is:", count)

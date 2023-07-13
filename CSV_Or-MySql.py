import os
import csv
import mysql.connector as conn
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import time

# Prompt the user to enter the product name
product = input("Enter the product name: ")
print("Welcome to Flipkart Web scraping with your searched items")

# Construct the Flipkart search URL for the entered product
flipkart_link = "https://www.flipkart.com/search?q=" + product

# Open the URL and read the HTML content
details = None
max_retries = 3
for retry in range(max_retries):
    try:
        details = urlopen(flipkart_link).read()
        break
    except Exception as e:
        print(f"Error occurred during request: {e}")
        print(f"Retrying ({retry+1}/{max_retries})...")
        time.sleep(1)

if not details:
    print("Failed to retrieve data from Flipkart. Exiting...")
    exit()

# Parse the HTML content using BeautifulSoup
beautified_details = bs(details, "html.parser")

# Find all the product boxes in the HTML
all_product = beautified_details.find_all('div', {"class": "_13oc-S"})

# Prompt the user to choose the storage option
storage_option = input("Enter the storage option (CSV or MySQL): ").lower()

# Initialize the data list to store review information
data = []

# Perform the web scraping and data extraction
for j in range(len(all_product) - 3):
    # Create a dictionary to store review data for each app
    review_data = {}

    lnk = "https://www.flipkart.com" + all_product[j].div.div.a["href"]
    single_product = None
    for retry in range(max_retries):
        try:
            single_product = urlopen(lnk).read()
            break
        except Exception as e:
            print(f"Error occurred during request: {e}")
            print(f"Retrying ({retry+1}/{max_retries})...")
            time.sleep(1)

    if not single_product:
        print(f"Failed to retrieve data for app {j+1}. Skipping...")
        continue

    details_bt = bs(single_product, "html.parser")
    try:
        # Extract the price from the details
        x = details_bt.find_all("div", {"class": "aMaAEs"})[0]
        price = x.find_all("div", {"class": "_30jeq3 _16Jk6d"})[0].text
        price = price.replace(",", "") if "," in price else "NO price"
        review_data["Price"] = price
    except:
        review_data["Price"] = "NO price"

    try:
        # Extract the name from the review box
        name = details_bt.find("div", {"class": "aMaAEs"}).h1.span.text
        review_data["Name"] = name
    except:
        review_data["Name"] = "No name"

    try:
        # Extract the certification from the review box
        certi = details_bt.find("div", {"class": "_2RngUh"}).text.split(",")[0]
        review_data["Certification"] = certi
    except:
        review_data["Certification"] = "No certification"

    try:
        # Extract the place from the review box
        place = details_bt.find("div", {"class": "_2RngUh"}).text.split(",")[1].strip()
        review_data["Place"] = place
    except:
        review_data["Place"] = "No place"

    try:
        # Extract the time from the review box
        time = details_bt.find_all("div", {"class": "_3LIJIw"})[0].text.split(",")[1].strip()
        review_data["Time"] = time
    except:
        review_data["Time"] = "No time"

    try:
        # Extract the rating from the review box
        rating = details_bt.find("div", {"class": "_1AtVbE"}).text
        review_data["Rating"] = rating
    except:
        review_data["Rating"] = "No rating"

    try:
        # Extract the short review from the review box
        short_review = details_bt.find("div", {"class": "_1AtVbE"}).find_next("div").text
        review_data["Short_review"] = short_review
    except:
        review_data["Short_review"] = "No review"

    # Append the review data to the list
    data.append(review_data)

# CSV storage option
if storage_option == 'csv':
    # Define the CSV file name and location
    csv_file = f"C:/Users/Raj/Documents/Python/Project/flipkart_data/CSVFile/{product}.csv"

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    # Create a CSV file for storing the extracted review information
    with open(csv_file, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Price", "Certification", "Place", "Time", "Rating", "Short_review"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved in CSV file: {csv_file}")

# MySQL storage option
elif storage_option == "mysql":
    try:
        # Establish MySQL connection
        sql = conn.connect(host='localhost', user='root', password='root')
        cursor = sql.cursor()

        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS flipkart")
        cursor.execute("USE flipkart")

        # Create the table if it doesn't exist
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {product} (Name VARCHAR(200), Price VARCHAR(25), Certification VARCHAR(50), Place VARCHAR(100), Time VARCHAR(20), Rating VARCHAR(5), Short_review VARCHAR(200))")

        # Insert the data into the table
        for review in data:
            insert_query = f"INSERT INTO {product} (Name, Price, Certification, Place, Time, Rating, Short_review) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            insert_values = (
                review["Name"],
                review["Price"],
                review["Certification"],
                review["Place"],
                review["Time"],
                review["Rating"],
                review["Short_review"]
            )
            cursor.execute(insert_query, insert_values)

        sql.commit()
        print("Data saved in MySQL table.")

    except conn.Error as e:
        print(f"Error connecting to MySQL or executing queries: {e}")

    finally:
        if sql:
            sql.close()

# Invalid storage option
else:
    print("Invalid storage option. Please choose either 'CSV' or 'MySQL'.")

# Print the total number of extracted data
print("Number of data:", len(data))

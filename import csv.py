import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

# Define Twitter credentials
twitter_username = "username"  # Replace with your Twitter username
twitter_password = "password"  # Replace with your Twitter password

# Path to the CSV file containing Twitter profile links
csv_file_path = r"filepath"    # Replace with the path to your CSV file

# Create a new Chrome webdriver instance
driver = webdriver.Chrome()

# Navigate to the Twitter login page
driver.get("https://twitter.com/login")

# Wait for the login page to load
wait = WebDriverWait(driver, 20)

# Enter Twitter username
username_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
username_input.send_keys(twitter_username)
username_input.send_keys("\n")  # Press Enter

# Wait for the password input to load
time.sleep(2)  # Adjust sleep time as necessary
password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
password_input.send_keys(twitter_password)
password_input.send_keys("\n")  # Press Enter

# Wait for the page to load after login
time.sleep(5)  # Adjust sleep time as necessary

# Read the CSV file to get Twitter profile links
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    profile_links = [row[0] for row in csv_reader]  # Assuming the links are in the first column

# Function to convert follower count to integer
def convert_to_int(count_str):
    if 'K' in count_str:
        return int(float(count_str.replace('K', '').replace(',', '').strip()) * 1000)
    elif 'M' in count_str:
        return int(float(count_str.replace('M', '').replace(',', '').strip()) * 1000000)
    else:
        return int(count_str.replace(',', '').strip()) if count_str.isdigit() else 0

# Iterate over each profile link and scrape data
for user_url in profile_links:
    # Skip the specified links
    if user_url in ["http://www.twitter.com", "http://www.twitter.com/"]:
        print(f"Skipping link: {user_url}")  # Debugging statement
        continue

    driver.get(user_url)
    time.sleep(5)  # Wait for the page to load

    # Log the page source for debugging
    page_source = driver.page_source
    print(f"Page source for {user_url}:\n{page_source}\n")  # Debugging statement

    # Scrape the bio, location, website, join date, following count, and followers count
    soup = BeautifulSoup(page_source, 'html.parser')

    # Initialize variables
    bio = location = website = join_date = following_count = followers_count = ""

    # Extract the bio
    try:
        bio_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='UserDescription']")))
        bio = bio_elements[0].text.strip() if bio_elements else ""
        print("Bio:", bio)  # Debugging statement
    except Exception as e:
        print("Error fetching bio: {}".format(e))  # Error handling

    # Extract the location
    try:
        location_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='UserLocation']")))
        location = location_elements[0].text.strip() if location_elements else ""
        print("Location:", location)  # Debugging statement
    except Exception as e:
        print("Error fetching location: {}".format(e))  # Error handling

    # Extract the website
    try:
        website_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='UserUrl']")))
        website = website_elements[0].text.strip() if website_elements else ""
        print("Website:", website)  # Debugging statement
    except Exception as e:
        print("Error fetching website: {}".format(e))  # Error handling

    # Extract the join date
    try:
        join_date_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='UserJoinDate']")))
        join_date = join_date_elements[0].text.strip() if join_date_elements else ""
        print("Join Date:", join_date)  # Debugging statement
    except Exception as e:
        print("Error fetching join date: {}".format(e))  # Error handling

    # Extract following count
    try:
        following_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href$='following'] span")))
        following_count = following_elements[0].text.strip() if following_elements else "0"  # Default to 0 if empty
        following_count = convert_to_int(following_count)  # Convert to int
        print("Following Count:", following_count)  # Debugging statement
    except Exception as e:
        following_count = 0  # Default to 0 if error occurs
        print("Error fetching following count: {}".format(e))  # Error handling

    # Extract followers count
    try:
        followers_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href$='followers'] span")))
        followers_count = followers_elements[0].text.strip() if followers_elements else "0"  # Default to 0 if empty
        followers_count = convert_to_int(followers_count)  # Convert to int
        print("Followers Count:", followers_count)  # Debugging statement
    except Exception as e:
        followers_count = 0  # Default to 0 if error occurs
        print("Error fetching followers count: {}".format(e))  # Error handling

    # MySQL database connection
    db_connection = mysql.connector.connect(
        host="localhost",  # Replace with your host
        user="root",  # User provided by the user
        password="YourPassword"  # Password provided by the user
    )

    cursor = db_connection.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS twitter_scraper_db;")

    # Connect to the newly created database
    db_connection.database = "twitter_scraper_db"

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS twitter_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(255),
        bio TEXT,
        location VARCHAR(255),
        website VARCHAR(255),
        join_date VARCHAR(255),
        following_count INT,
        followers_count INT
    )
    """)

    # Insert the data into the database, allowing for empty fields
    insert_query = """
    INSERT INTO twitter_data (user_name, bio, location, website, join_date, following_count, followers_count)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (user_url.split('/')[-1], bio, location, website, join_date, following_count, followers_count))
    print("Data inserted successfully for:", user_url)  # Debugging statement

    # Commit the transaction
    db_connection.commit()

    # Close the database connection
    cursor.close()
    db_connection.close()

# Close the webdriver
driver.quit()

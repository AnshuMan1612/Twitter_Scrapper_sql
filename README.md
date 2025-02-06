Twitter Profile Scraper and MySQL Storage

📌 Overview

This Python script automates the process of scraping Twitter profile data using Selenium and BeautifulSoup. The extracted data is then stored in a MySQL database for further analysis.


✨ Features

✅ Logs into Twitter using credentials

✅ Scrapes Twitter profiles from a CSV file

✅ Extracts:


Bio

Location

Website

Join Date

Following Count

Followers Count

✅ Converts following/followers counts into numerical values

✅ Stores the extracted data into a MySQL database


🛠 Setup & Installation

1️⃣ Install Dependencies

Ensure you have Python installed (Python 3.x recommended). Install required libraries:

pip install selenium beautifulsoup4 mysql-connector-python

2️⃣ Install ChromeDriver

Download ChromeDriver compatible with your Google Chrome version:

🔗 ChromeDriver Download

Place it in a directory included in your system’s PATH, or specify its location in the script.

3️⃣ Clone the Repository

git clone https://github.com/your-username/twitter-scraper.git

cd twitter-scraper

4️⃣ Configure Your Credentials

Edit the script (scraper.py) and replace:


twitter_username = "your_username"  # Your Twitter username

twitter_password = "your_password"  # Your Twitter password

csv_file_path = r"your_csv_file_path.csv"  # Path to your CSV file

Also, update the MySQL database credentials:


db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourPassword"
)

5️⃣ Run the Script

python scraper.py

🗄 Database Schema

The script creates a MySQL database named twitter_scraper_db and a table twitter_data:


Column Name	Data Type	Description

id	INT (Primary Key, Auto Increment)	Unique row identifier

user_name	VARCHAR(255)	Twitter handle of the user

bio	TEXT	User's bio from Twitter

location	VARCHAR(255)	User's location

website	VARCHAR(255)	User's website URL

join_date	VARCHAR(255)	The date user joined Twitter

following_count	INT	Number of accounts the user follow
s
followers_count	INT	Number of followers


🛠 How It Works

1️⃣ The script logs into Twitter using Selenium.

2️⃣ Reads Twitter profile URLs from the CSV file.

3️⃣ Scrapes profile details using BeautifulSoup & Selenium.

4️⃣ Stores the extracted data into a MySQL database.


❌ Troubleshooting

Login Issues

Ensure your Twitter credentials are correct.

If login fails, Twitter might have changed its UI – update the CSS selectors accordingly.

Scraper Stops Working

Twitter may block automated access.

Try reducing the scraping speed (time.sleep(5)).

Use rotating proxies or different accounts.

MySQL Errors

Ensure MySQL server is running and credentials are correct.

If the database is not created, manually create it using:

CREATE DATABASE twitter_scraper_db;

⚠ Disclaimer

This project is for educational purposes only. Scraping Twitter may violate its Terms of Service.

Use responsibly, and do not abuse this tool.

💡 Contributing

Pull requests are welcome! If you find any bugs or want to improve the project, feel free to contribute.

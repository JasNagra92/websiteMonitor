import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

host = 'jasnagra92.mysql.pythonanywhere-services.com'
user = 'jasnagra92'
password = f"{os.environ.get('SQLPW')}"
database = "jasnagra92$RegionalDistricts"

try:
    # Establish a connection
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected to the database")

        # Create a cursor
        cursor = connection.cursor()

        # You can perform further database operations here

        # Close the cursor and the connection
        cursor.close()
        connection.close()
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")


# Define the URLs of the websites to monitor
cariboo_url = 'https://www.cariboord.ca/Modules/news/en?CategoryNames=Emergency+Alerts+and+Orders&TagWhiteList='
slrd_url = 'https://www.slrd.bc.ca/emergency-program/emergency-alerts-orders'
nrrm_url = 'https://www.northernrockies.ca/Modules/News/en?CategoryNames=Advisories+and+Public+Notices&datepicker-month-select=8&datepicker-year-select=2023&datepicker-month-select=8&datepicker-year-select=2023&TagWhiteList='
glen_lake_url = 'https://www.cordemergency.ca/emergencies/glen-lake-wildfire-2023'
mcdougall_url = 'https://www.cordemergency.ca/emergencies/mcdougall-creek-wildfire-2023'
sunshine_coast_url = 'https://www.scrd.ca/news/?_news_types=news-release'
Okanagan_Similkameen_url = 'https://www.rdos.bc.ca/newsandevents/rdos-news/hot-topics/'
tnrd_url = 'https://www.tnrd.ca/services/emergency-services/evacuation-orders-alerts/'
peace_river_orders_url = 'https://prrd.bc.ca/category/emergency-evacuations/'
peace_river_alerts_url = 'https://prrd.bc.ca/category/emergency-alerts/'

# Define regex patterns for each website's date format
cariboo_date_pattern = r'\w+, (\w+ \d{1,2}, \d{4} \d{2}:\d{2} [APap][Mm])'
slrd_date_pattern = r'Last updated: (\w{3} \d{1,2}, \d{4} - \d{1,2}:\d{2}[APap][Mm])'
nrrm_date_pattern = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}\s+[APap][Mm]'
okanagen_date_pattern = r'(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday),\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\s+-\s+\d{2}:\d{2}'
sunshine_coast_date_pattern = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}'
Okanagan_Similkameen_date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4},\s+\d{1,2}:\d{2}\s+(?:am|pm)\b'
tnrd_date_pattern = r'\b(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4},\s+\d{1,2}:\d{2}\b'
peace_river_order_date_pattern = r'September\s+\d{1,2},\s+\d{4}'
peace_river_alert_date_pattern = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}'


# Define a function to extract and print dates from a website
def extract_and_print_dates(url, date_pattern, website_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = str(soup)

    date_matches = re.findall(date_pattern, content)
    
    if date_matches:
        print(f"Dates from {website_name}: {url}")
        count = 0
        for date_str in date_matches:
            print(f"{date_str}")
            document = {
                "date": date_str,
                "url": url,
                "website": website_name
            }
            count += 1
            if count >= 1:
                break
    else:
        print(f"No dates found on {website_name}.")

# Extract and print dates for the Cariboo website
extract_and_print_dates(cariboo_url, cariboo_date_pattern, "Cariboo Regional District")

# Extract and print dates for the SLRD website
extract_and_print_dates(slrd_url, slrd_date_pattern, "Squamish-Lillooet Regional District")

# Extract and print dates for the NRRM website
extract_and_print_dates(nrrm_url, nrrm_date_pattern, "Northern Rockies Regional Municipality")

# Extract and print dates for the Glen Lake website
extract_and_print_dates(glen_lake_url, okanagen_date_pattern, "Glen Lake Emergency")

# Extract and print dates for the McDougall Creek website
extract_and_print_dates(mcdougall_url, okanagen_date_pattern, "McDougall Creek Emergency")

# Extract and print dates for the Sunshine Coast website
extract_and_print_dates(sunshine_coast_url, sunshine_coast_date_pattern, "Sunshine Coast Regional District")

# Extract and print dates for the Okanagan-Similkameen website
extract_and_print_dates(Okanagan_Similkameen_url, Okanagan_Similkameen_date_pattern, "Okanagan-Similkameen Regional District")

# Extract and print dates for the Thompson-Nicola website
extract_and_print_dates(tnrd_url, tnrd_date_pattern, "Thompson-Nicola Regional District")

# Extract and print dates for the Peace River Regional District website
extract_and_print_dates(peace_river_orders_url, peace_river_order_date_pattern, "Peace River Regional District Orders")

# Extract and print dates for the Peace River Regional District website
extract_and_print_dates(peace_river_alerts_url, peace_river_alert_date_pattern, "Peace River Regional District Alerts")

input("Press Enter to exit...")
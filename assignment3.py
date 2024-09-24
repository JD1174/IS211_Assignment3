import argparse
import urllib.request
import csv
import re
from datetime import datetime

# Function to download the web log file from the provided URL
def download_file(url):
    # Open the URL and read the content, decode from bytes to string
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    return data

# Function to process the downloaded file and convert it into a list of CSV rows
def process_file(data):
    # Split the file data into lines
    lines = data.splitlines()
    # Use the csv.reader to parse the CSV lines into a list of lists
    reader = csv.reader(lines)
    return list(reader)

# Function to count and display the percentage of image hits (.jpg, .gif, .png)
def count_image_hits(data):
    # Regular expression to match image file extensions (case-insensitive)
    image_extensions = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)
    # Calculate total number of hits
    total_hits = len(data)
    # Count how many hits are for image files
    image_hits = sum(1 for row in data if image_extensions.search(row[0]))
    # Calculate the percentage of image requests
    percentage = (image_hits / total_hits) * 100
    # Print the result with one decimal point
    print(f"Image requests account for {percentage:.1f}% of all requests")

# Function to determine and print the most popular browser
def most_popular_browser(data):
    # Dictionary to count requests for each browser
    browsers = {'Firefox': 0, 'Chrome': 0, 'Internet Explorer': 0, 'Safari': 0}
    # Loop through each row of the data
    for row in data:
        # Increment the appropriate browser counter based on the user agent string
        if 'Firefox' in row[2]:
            browsers['Firefox'] += 1
        elif 'Chrome' in row[2]:
            browsers['Chrome'] += 1
        elif 'MSIE' in row[2]:
            browsers['Internet Explorer'] += 1
        elif 'Safari' in row[2] and 'Chrome' not in row[2]:
            browsers['Safari'] += 1
    # Find the browser with the most hits
    popular_browser = max(browsers, key=browsers.get)
    print(f"The most popular browser is {popular_browser}")

# Function to calculate and print how many hits occurred in each hour of the day
def hits_by_hour(data):
    # Initialize a list with 24 zeros, one for each hour
    hours = [0] * 24
    # Loop through each row of the data
    for row in data:
        # Parse the datetime string and extract the hour
        hour = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').hour
        # Increment the counter for that hour
        hours[hour] += 1
    
    # Create a list of tuples (hour, count) and sort by count in descending order
    sorted_hours = sorted(enumerate(hours), key=lambda x: x[1], reverse=True)
    
    # Loop through the sorted hours and print the number of hits for each hour
    for hour, count in sorted_hours:
        print(f"Hour {hour:02d} has {count} hits")

# Main function to control the flow of the program
def main(url):
    print(f"Running main with URL = {url}...")
    # Download the file from the given URL
    data = download_file(url)
    processed_data = process_file(data)
    # Call the function to count image hits
    count_image_hits(processed_data)
    # Call the function to determine the most popular browser
    most_popular_browser(processed_data)
    # Call the function to calculate hits by hour
    hits_by_hour(processed_data)

# Entry point of the script, parsing the command line argument for URL
if __name__ == "__main__":
    # Create an ArgumentParser object to handle command line arguments
    parser = argparse.ArgumentParser()
    # Define the --url argument as required
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    # Parse the arguments and get the URL value
    args = parser.parse_args()
    # Call the main function with the provided URL
    main(args.url)
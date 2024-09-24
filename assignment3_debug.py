import argparse
import urllib.request
import csv
import re
from datetime import datetime

# Function to download the web log file from the provided URL
def download_file(url):
    print(f"Downloading file from {url}...")  # Debug
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    print("Download complete, file size:", len(data), "bytes")  # Debug
    return data

# Function to process the downloaded file and convert it into a list of CSV rows
def process_file(data):
    print("Processing file...")  # Debug
    lines = data.splitlines()
    reader = csv.reader(lines)
    
    # Print the first few lines to verify the CSV is being read correctly
    for i, row in enumerate(reader):
        if i < 5:  # Print first 5 rows for debugging
            print(f"Row {i}: {row}")  # Debug
        else:
            break
    
    processed_data = list(reader)
    print(f"Total rows processed: {len(processed_data)}")  # Debug
    return processed_data

# Function to count and display the percentage of image hits (.jpg, .gif, .png)
def count_image_hits(data):
    image_extensions = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)
    total_hits = len(data)
    image_hits = sum(1 for row in data if image_extensions.search(row[0]))
    percentage = (image_hits / total_hits) * 100 if total_hits > 0 else 0
    print(f"Total requests: {total_hits}, Image requests: {image_hits}")  # Debug
    print(f"Image requests account for {percentage:.1f}% of all requests")

# Function to determine and print the most popular browser
def most_popular_browser(data):
    browsers = {'Firefox': 0, 'Chrome': 0, 'Internet Explorer': 0, 'Safari': 0}
    for row in data:
        if 'Firefox' in row[2]:
            browsers['Firefox'] += 1
        elif 'Chrome' in row[2]:
            browsers['Chrome'] += 1
        elif 'MSIE' in row[2]:
            browsers['Internet Explorer'] += 1
        elif 'Safari' in row[2] and 'Chrome' not in row[2]:
            browsers['Safari'] += 1
    
    # Debug: Print browser counts
    print("Browser counts:", browsers)  # Debug
    
    if browsers:
        popular_browser = max(browsers, key=browsers.get)
        print(f"The most popular browser is {popular_browser}")

# Function to calculate and print how many hits occurred in each hour of the day
def hits_by_hour(data):
    hours = [0] * 24
    for row in data:
        try:
            # Parse the datetime string and extract the hour
            hour = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').hour
            hours[hour] += 1
        except Exception as e:
            # Debug: Print error message if datetime parsing fails
            print(f"Error parsing datetime for row {row}: {e}")  # Debug
    
    # Debug: Print hourly counts
    print("Hourly hits:", hours)  # Debug
    
    for hour, count in enumerate(hours):
        if count > 0:  # Only print if there are hits
            print(f"Hour {hour:02d} has {count} hits")

# Main function to control the flow of the program
def main(url):
    print(f"Running main with URL = {url}...")  # Debug
    data = download_file(url)
    processed_data = process_file(data)
    
    # Debug: Check if processed data is non-empty
    if processed_data:
        print(f"First row after processing: {processed_data[0]}")  # Debug
    else:
        print("No data processed.")  # Debug
    
    count_image_hits(processed_data)
    most_popular_browser(processed_data)
    hits_by_hour(processed_data)

# Entry point of the script, parsing the command line argument for URL
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
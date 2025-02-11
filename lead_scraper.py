import requests
from bs4 import BeautifulSoup
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to scrape leads from public directories and forums

def scrape_leads(url):
    leads = []  # List to store lead data
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example scraping logic (to be customized based on actual HTML structure)
        for entry in soup.find_all('div', class_='lead-entry'):
            lead = {
                'full_name': entry.find('span', class_='full-name').text,
                'email': entry.find('span', class_='email').text,
                'phone': entry.find('span', class_='phone').text,
                'location': entry.find('span', class_='location').text,
                'age': entry.find('span', class_='age').text,
                'gender': entry.find('span', class_='gender').text,
                'marital_status': entry.find('span', class_='marital-status').text,
                'occupation': entry.find('span', class_='occupation').text,
                'income_level': entry.find('span', class_='income-level').text,
            }
            leads.append(lead)
            logging.info(f'Lead collected: {lead}')
    except Exception as e:
        logging.error(f'Error while scraping: {e}')

    return leads

# Function to save leads to a CSV file

def save_to_csv(leads, filename='leads.csv'):
    keys = leads[0].keys() if leads else []
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(leads)
    logging.info(f'Saved {len(leads)} leads to {filename}')

import requests
from bs4 import BeautifulSoup
import csv
import os

# Ensure the output directory exists
os.makedirs('output', exist_ok=True)

BASE_URL = 'http://books.toscrape.com/'

def scrape_books(url):
    books_data = []
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Failed to retrieve the webpage: {url}')
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text[2:]  # Remove the currency symbol (£)
            books_data.append({'Title': title, 'Price': price})
            print(f'Title: {title}')
            print(f'Price: £{price}')
            print('-' * 40)

        # Find the 'next' button link
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page = next_button.find('a')['href']
            url = BASE_URL + 'catalogue/' + next_page
        else:
            url = None

    return books_data

def save_to_csv(data, filename='output/books.csv'):
    if not data:
        print('No data to save.')
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f'Scraping completed. Data saved to {filename}.')

if __name__ == '__main__':
    books_data = scrape_books(BASE_URL)
    save_to_csv(books_data)

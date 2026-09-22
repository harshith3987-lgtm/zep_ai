import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
RAW_OUTPUT = os.path.join(DATA_DIR, 'raw_scraped_books.json')

CATEGORIES = {
    'Mystery': 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
    'Fantasy': 'http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html',
    'Fiction': 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html'
}

def scrape_category(cat_name, start_url):
    books = []
    current_url = start_url

    while current_url:
        print(f'  [+] Scraping {cat_name} -> {current_url}')
        resp = requests.get(current_url, timeout=15)
        if resp.status_code != 200:
            print(f'  [-] Failed with status {resp.status_code}')
            break

        soup = BeautifulSoup(resp.content, 'html.parser')
        pods = soup.select('article.product_pod')

        for pod in pods:
            title_tag = pod.select_one('h3 a')
            title = title_tag['title'] if title_tag and 'title' in title_tag.attrs else title_tag.text.strip()
            price_text = pod.select_one('p.price_color').text.strip()

            rating_tag = pod.select_one('p.star-rating')
            classes = rating_tag['class'] if rating_tag else []
            star_rating = [c for c in classes if c != 'star-rating'][0] if len(classes) > 1 else 'None'

            avail_tag = pod.select_one('p.instock.availability')
            availability = avail_tag.text.strip() if avail_tag else 'Unknown'

            books.append({
                'title': title,
                'price_raw': price_text,
                'star_rating_text': star_rating,
                'availability_text': availability,
                'category': cat_name
            })

        next_button = soup.select_one('li.next a')
        if next_button:
            next_href = next_button['href']
            current_url = urljoin(current_url, next_href)
        else:
            current_url = None

    return books

def run():
    all_books = []
    print('Starting extraction across Mystery, Fantasy, and Fiction...')
    for cat_name, cat_url in CATEGORIES.items():
        print(f'\nFetching category: {cat_name}')
        cat_books = scrape_category(cat_name, cat_url)
        all_books.extend(cat_books)
        print(f'  [✓] Collected {len(cat_books)} books from {cat_name}')

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RAW_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(all_books, f, indent=2, ensure_ascii=False)

    print('\n' + '='*50)
    print(f'[✓] TOTAL SCRAPED: {len(all_books)} books across {len(CATEGORIES)} categories.')
    print(f'[✓] Saved to: {RAW_OUTPUT}')
    print('='*50)

if __name__ == '__main__':
    run()
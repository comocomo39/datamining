from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time


def scrape_upcoming_films(url):
    films_data = []

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    film_items = soup.find_all('li', class_='listitem')

    for item in film_items:
        film_link = item.find('a', class_='frame')
        if film_link:
            film_href = film_link['href']
            film_url = f"https://letterboxd.com{film_href}"
            film_id = film_href.strip('/').split('/')[-1]
            film_details = scrape_film_details(driver, film_url)
            films_data.append({
                'movie_id': film_id,
                'genre': film_details['genre'],
                'overview': film_details['overview']
            })

    driver.quit()
    return films_data


def scrape_film_details(driver, film_url):
    driver.get(film_url)
    time.sleep(5)  # Wait for the dynamic content to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the 'tab-genres' div and then find the first 'a' tag with the class 'text-slug'
    genre_tag = soup.find('div', id='tab-genres').find('a', class_='text-slug')
    genre = genre_tag.get_text(strip=True) if genre_tag else 'unknown'

    description_tag = soup.find('div', class_='truncate').find_next('p') if soup.find('div',
                                                                                      class_='truncate') else None
    overview = description_tag.get_text(separator=' ', strip=True) if description_tag else 'No overview available'

    return {'genre': genre, 'overview': overview}


def save_to_csv(films_data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['movie_id', 'genre', 'overview'])
        for film in films_data:
            writer.writerow([film['movie_id'], film['genre'], film['overview']])


# URL della pagina con i film in arrivo
upcoming_films_url = 'https://letterboxd.com/films/upcoming/'
films_data = scrape_upcoming_films(upcoming_films_url)

# Salva i dati raccolti in un file CSV
csv_filename = 'data_scraping.csv'
if films_data:
    save_to_csv(films_data, csv_filename)
    print(f"Dati salvati con successo in {csv_filename}")
else:
    print("Nessun dato da salvare.")

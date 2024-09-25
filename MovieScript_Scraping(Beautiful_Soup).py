import re
import time
from bs4 import BeautifulSoup
import requests

root = 'https://subslikescript.com'
website = f'{root}/movies_letter-X'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
result = requests.get(website, headers=headers)
content = result.text
soup = BeautifulSoup(content, 'lxml')

pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

links = []

# Loop through all the pages
for page in range(1, int(last_page) + 1):
    result = requests.get(f'{website}?page={page}', headers=headers)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find('article', class_='main-article')

    for link in box.find_all('a', href=True):
        links.append(link['href'])

    # Loop through each link to get transcript
    for link in links:
        try:
            result = requests.get(f'{root}{link}', headers=headers)
            time.sleep(2)  # Slow down requests to avoid being blocked
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            box = soup.find('article', class_='main-article')
            title = box.find('h1').get_text()
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')

            # Sanitize title to avoid issues with invalid characters
            title = re.sub(r'[\\/*?:"<>|]', "", title)

            with open(f'{title}.txt', 'w', encoding='utf-8') as file:
                file.write(transcript)
        except Exception as e:
            print('------ Link not working -------')
            print(link)
            print(e)

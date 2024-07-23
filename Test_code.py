import requests
from bs4 import BeautifulSoup
import json

def get_vacancies(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
        print(f"Successfully connected to {url}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
        return None
    except Exception as err:
        print(f"An error occurred: {err}")  # Other errors
        return None
    
    return response.text

def parse_vacancies(html):
    if html is None:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    vacancies = []
    items = soup.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y')
    print(f"Found {len(items)} vacancies on the page.")
    
    for item in items:
        title_tag = item.find('a', class_='bloko-link')
        title = title_tag.text.strip() if title_tag else 'Без названия'
        
        link = title_tag['href'] if title_tag else 'Нет ссылки'
        
        company_tag = item.find('a', class_='bloko-link bloko-link_kind-secondary')
        company = company_tag.text.strip() if company_tag else 'Не указана'
        
        city_tag = item.find('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni')
        city = city_tag.text.strip() if city_tag else 'Не указан'
        
        salary_tag = item.find('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh')
        salary = salary_tag.text.strip() if salary_tag else 'Не указана'

        vacancies.append({
            'title': title,
            'link': link,
            'salary': salary,
            'city': city,
            'company': company,
            
        })
    
    return vacancies

def write_vacancies_to_file(vacancies):
    if not vacancies:
        print("Нет данных для записи в файл.")
        return
    with open('Prorock.json', 'w', encoding='utf-8', newline='') as file:
        json.dump(vacancies, file, ensure_ascii=False, indent=4)
    print("Данные записаны в файл: 'Prorock.json'.")

if __name__ == '__main__':
    base_url = 'https://moscow.hh.ru/search/vacancy'
    params = {
        'text': 'python django flask',
        'salary': '',
        'enable_snippets': 'true',
        'area': '1,2',
        'page': 0,
        'per_page': 20
    }
    full_url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    html_content = get_vacancies(full_url)
    if html_content:
        vacancies = parse_vacancies(html_content)
        write_vacancies_to_file(vacancies)
    print("Программа завершена.")

import requests
from bs4 import BeautifulSoup
import json
import re

def get_vacancies(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Successfully connected to {url}")
    else:
        print(f"Failed to connect to {url}, status code: {response.status_code}")
    
    response.raise_for_status()
    return response.text

def parse_vacancies(html):
    soup = BeautifulSoup(html, 'lxml')
    vacancies = []
    count = 0

    items = soup.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter')
    print(f"Found {len(items)} vacancies on the page.")
    
    for item in items:
        title_tag = item.find('a', class_='serp-item__title')
        company_tag = item.find('a', class_='vacancy-serp__vacancy-address')
        city_tag = item.find('div', class_='bloko-text bloko-text_no-top-indent')
        salary_tag = item.find('span', class_='bloko-header-section-3')
        description_tag = item.find('div', class_='g-user-content')

        if not title_tag or not company_tag or not city_tag:
            print("Missing one of the required tags.")
            continue

        title = title_tag.text
        link = title_tag['href']
        company = company_tag.text.strip()
        city = city_tag.text.strip()
        salary = salary_tag.text if salary_tag else 'Не указана'
        description = description_tag.text.lower() if description_tag else ""

        print(f"\nProcessing vacancy: {title} at {company} in {city}")
        print(f"Link: {link}")
        print(f"Salary: {salary}")
        print(f"Description: {description}")
        
        if re.search(r'\bdjango\b', description) or re.search(r'\bflask\b', description):
            print(f"Match found: {title}")
            vacancies.append({
                'title': title,
                'link': link,
                'company': company,
                'city': city,
                'salary': salary
            })
            count += 1
    
    print(f"Total vacancies added: {count}")
    return vacancies


def save_vacancies_to_json(vacancies, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)

def main():
    url_moscow = "https://hh.ru/search/vacancy?text=Python&area=1&search_field=name&search_field=description"
    url_spb = "https://hh.ru/search/vacancy?text=Python&area=2&search_field=name&search_field=description"

    html_moscow = get_vacancies(url_moscow)
    html_spb = get_vacancies(url_spb)

    vacancies_moscow = parse_vacancies(html_moscow)
    vacancies_spb = parse_vacancies(html_spb)

    all_vacancies = vacancies_moscow + vacancies_spb

    save_vacancies_to_json(all_vacancies, 'vacancies.json')

if __name__ == '__main__':
    main()

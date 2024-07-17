import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
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

    items = soup.find_all('div', class_='vacancy-serp-item')
    print(f"Found {len(items)} vacancies on the page.")
    
    for item in items:
        title_tag = item.find('a', class_='bloko-link')
        company_tag = item.find('div', class_='vacancy-serp-item__meta-info-company')
        city_tag = item.find('span', class_='vacancy-serp-item__meta-info')
        salary_tag = item.find('span', class_='bloko-header-section-3')
        description_tag = item.find('div', class_='g-user-content')

        if not title_tag or not company_tag or not city_tag:
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

def save_vacancies_to_xml(vacancies, filename):
    root = ET.Element("vacancies")
    for vacancy in vacancies:
        vacancy_element = ET.SubElement(root, "vacancy")
        
        title_element = ET.SubElement(vacancy_element, "title")
        title_element.text = vacancy['title']
        
        link_element = ET.SubElement(vacancy_element, "link")
        link_element.text = vacancy['link']
        
        company_element = ET.SubElement(vacancy_element, "company")
        company_element.text = vacancy['company']
        
        city_element = ET.SubElement(vacancy_element, "city")
        city_element.text = vacancy['city']
        
        salary_element = ET.SubElement(vacancy_element, "salary")
        salary_element.text = vacancy['salary']
    
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

def main():
    url_moscow = "https://hh.ru/search/vacancy?text=Python&area=1&search_field=name&search_field=description"
    url_spb = "https://hh.ru/search/vacancy?text=Python&area=2&search_field=name&search_field=description"

    html_moscow = get_vacancies(url_moscow)
    html_spb = get_vacancies(url_spb)

    vacancies_moscow = parse_vacancies(html_moscow)
    vacancies_spb = parse_vacancies(html_spb)

    all_vacancies = vacancies_moscow + vacancies_spb

    save_vacancies_to_xml(all_vacancies, 'vacancies.xml')

if __name__ == '__main__':
    main()

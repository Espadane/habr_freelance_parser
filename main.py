import json
import requests
from bs4 import BeautifulSoup


def get_pagination(url):
    """получаем пагинацию"""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    pages = soup.find('div', class_='pagination')
    last_page = pages.find_all('a')[-2].text
    
    return last_page



def get_tasks(url, last_page):
    """получаем задачи"""
    tasks = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    posts = soup.find_all('article')
    for post in posts:
        title = post.find('div', class_='task__title').get('title')
        link = 'https://freelance.habr.com/' + post.find('div', class_='task__title').find('a').get('href')
        try:
            price = post.find('div', class_='task__price').find('span', class_='count').text
        except:
            price = '___'

        tasks.append({
            'title' : title,
            'link' : link, 
            'price' : price
        })

    return tasks

def write_json(tasks, taks_name):
    """пишем задачи в джейсон файл"""
    with open(f'{taks_name}_tasks_habr.json', 'a') as file:
        json.dump(tasks[0:20], file, indent=4, ensure_ascii=False) #последние 20 задач


def main():
    urls_to_parse = ['https://freelance.habr.com/tasks?q=python',
                    'https://freelance.habr.com/tasks?q=javascript',
                    ]
    for url in urls_to_parse:
        taks_name = url.split('=')[-1]
        last_page = get_pagination(url)
        # for i in range(1, int(last_page)):
        for i in range(1, 2):
            url = f'https://freelance.habr.com/tasks?page={i}&q={taks_name}'
            print(url)
            tasks = get_tasks(url, last_page)
            write_json(tasks, taks_name)


if __name__ == '__main__':
    main()
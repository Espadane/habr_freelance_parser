import json
import requests
from bs4 import BeautifulSoup
import os
import asyncio


async def get_tasks(url, taks_name):
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

    write_json(tasks, taks_name)

def write_json(tasks, taks_name):
    """пишем задачи в джейсон файл"""
    if not os.path.exists('reports'):
        os.mkdir('reports')
    with open(f'reports/{taks_name}_tasks_habr.json', 'a') as file:
        json.dump(tasks[0:20], file, indent=4, ensure_ascii=False) #последние 20 задач


async def main():
    urls_to_parse = ['https://freelance.habr.com/tasks?q=python',
                    'https://freelance.habr.com/tasks?q=javascript',
                    ]
    jobs = []
    for url in urls_to_parse:
        print(url)
        taks_name = url.split('=')[-1]
        for i in range(1, 2):
            url = f'https://freelance.habr.com/tasks?page={i}&q={taks_name}'
            job = asyncio.create_task(get_tasks(url, taks_name))
            jobs.append(job)
        await asyncio.gather(*jobs)


if __name__ == '__main__':
    asyncio.run(main())

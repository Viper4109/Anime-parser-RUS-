import requests
from bs4 import BeautifulSoup
import csv
import re
import time
from fake_useragent import UserAgent

link1 = r'Scripts\Python space\\' #Укажите путь до папки в которую вы хотите сохранить файл выходных данных "Anime_data.csv", если оставить скобки пустыми будет использоваться путь по умолчанию. (там же где находится скрипт)
# пример пути: r'Scripts\Python space\\' в конце обязательны два слеша.
# Скрипт будет работать бесконечно, но вы можете его завершить когда хотите. По моим подсчетам на 09.06.2024 там парсится 36-38 страниц, остальные пустые. Но эта информация может быть неактуальной.
page = 3   # просто укажите число на странице, где вы хотите, чтобы скрипт перестал работать. 
# Если page равно None или 0, скрипт будет работать бесконечно, пока вы не отключите его вручную.

class ParseAnime():
    
    def parse(self):
        self.__create_csv()
        
        ua = UserAgent()
        user_agent = ua.random
        
        num = 1
        while True:
            headers = {
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'origin': 'https://jut.su',
                'referer': 'https://jut.su/anime/',
                'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': user_agent,
                'x-requested-with': 'XMLHttpRequest',
            }

            data = {
                'ajax_load': 'yes',
                'start_from_page': num,
                'show_search': '',
                'anime_of_user': '',
            }
            
            response = requests.post('https://jut.su/anime/', headers=headers, data=data)

            soup = BeautifulSoup(response.content, 'lxml')

            cards = soup.find_all('div', class_='all_anime_global')
            
            names = []
            links = []
            episodes = []
            
            for i,v in enumerate(cards):
                name = v.find('div', class_='aaname')
                link = v.find('a')
                link = 'https://jut.su' + link.get('href')
                episode = v.find('div', class_='aailines')
                episode = self.process_entry(episode.text)
                names.insert(i, name.text)
                links.insert(i, link)
                episodes.insert(i, episode)
            
            self.save_csv(num, names, episodes, links)
            print(f'[+] Страница {num} сохранена.')
            if type(page) == int and page is not None and page > 0:
                if num == page:
                    break
            num += 1
            time.sleep(2)
    
    def process_entry(self, entry):
        seasons = re.search(r'(\d+)\s*сезон', entry)
        episodes = re.search(r'(\d+)\s*сер', entry)
        movies = re.search(r'(\d+)\s*фильм', entry)
        
        result = []
        if seasons:
            result.append(f'Сезоны: {int(seasons.group(1))}')
        if episodes:
            result.append(f'Серии: {int(episodes.group(1))}')
        if movies:
            result.append(f'Фильмы: {int(movies.group(1))}')
        
        return ', '.join(result)
        
    def __create_csv(self):
        with open(rf'{link1}Anime_data.csv', mode='w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['№', 'Название', 'Кол-во серий' , 'Cсылка'])
        
    def save_csv(self, num, names, episodes, links):
        with open(rf'{link1}Anime_data.csv', mode='a', newline="") as file:
            writer = csv.writer(file)
            num -= 1
            for i,name in enumerate(names):
                writer.writerow([str(i + 1 + (30 * num)) + ')',
                                name,
                                episodes[i],
                                links[i]])
                
if __name__ == "__main__":
    parser = ParseAnime()
    parser.parse()
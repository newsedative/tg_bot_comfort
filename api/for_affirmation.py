# получение аффирмаций с сайта

import requests
from bs4 import BeautifulSoup as bs
import random


URL_TEMPLATE = "https://ivseitaki-interesno.ru/affirmacii-na-kazhdyj-den-bolee-200-proverennyh-affirmacij-na-ljubov-zdorove-bogatstvo-uspeh-i-mnogie-drugie.html"
r = requests.get(URL_TEMPLATE)
soup = bs(r.text, "html.parser")
vacancies_names = soup.find_all('div', class_='td-post-content')
affirm_list = ' '
for name in vacancies_names:
    affirm_list = str(name.ol)
affirm_list = affirm_list.replace('<li>', '')
affirm_list = affirm_list.replace('</li>', '')
aff = affirm_list.split('\n')[1:]


def random_aff():
    return random.choice(aff)
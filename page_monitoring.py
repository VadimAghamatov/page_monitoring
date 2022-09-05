import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime
from art import tprint

# Немного сделаем дружелюбным
tprint('Monitoring for you', font='bulbhead')

# URL мониторинга
url = input("\nВведите веб адрес (Например: https://example.com): ")

# Работай как браузер
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

PrevVersion = ""
FirstRun = True

while True:

    # загрузка страницы
    response = requests.get(url, headers=headers)
    # парсинг загруженной страницы
    soup = BeautifulSoup(response.text, "lxml")

    # удаление всех стилей и скриптов
    for script in soup(["script", "style"]):
        script.extract()
    soup = soup.get_text()
    # сравнение текста станицы с прежней версией
    if PrevVersion != soup:
        # первый подход - только запоминаем состояние
        if FirstRun == True:
            PrevVersion = soup
            FirstRun = False
            print ("Начало мониторинга " +url+ " в "+ str(datetime.now())+ " каждые 60 секунд. ")

        else:
            print ("Найдено изменение в: "+ str(datetime.now()))
            OldPage = PrevVersion.splitlines()
            NewPage = soup.splitlines()
            # сравниваем версии страницы на изменения с помощью библиотеки difflib
            #d = difflib.Differ()
            #diff = d.compare(OldPage, NewPage)
            diff = difflib.context_diff(OldPage,NewPage,n=10)
            out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])
            print (out_text)
            OldPage = NewPage
            #print ('\n'.join(diff))
            PrevVersion = soup

    else:
        print( "Нет изменений "+ str(datetime.now()))
    time.sleep(60)
    continue

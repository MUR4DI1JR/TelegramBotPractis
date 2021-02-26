import time
import schedule
import telebot
from requests import get
from bs4 import BeautifulSoup
from urllib.request import urlopen
from time import sleep
from telebot import types
import pdb

API_TOKEN = '1453127728:AAHQb3egcy_UcQpYN5M-VUIB0p-fTPcVoeM'

bot = telebot.TeleBot(API_TOKEN, parse_mode=None)

url = get('https://www.playground.ru/news').content
soup = BeautifulSoup(url, 'html.parser')
div = soup.find_all("div", {"class": "post-title"})
links = []

div_img = soup.find_all("article", {"class": "post"})
b = []

posts = []


for link in div:
    links.append(link.find('a')['href'])


for i in range(int(len(links))):
    post = {}
    j = div_img[i].find('img')['src']
    name_img = j.split('/')[-1]
    name = name_img[:-8]
    post['img'] = name
    url = links[i]
    page = get(links[i]).content
    soup = BeautifulSoup(page, 'html.parser')
    h1 = soup.h1.text
    p = soup.p.text
    post['h1'] = h1
    post['p'] = p
    posts.append(post)

print(posts)

@bot.message_handler(commands=['start', 'go'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("OK")
    item2 = types.KeyboardButton("STOP")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'hello, {0.first_name}!\nЯ игровой новостной паблик! \n Буду постить актуальные новости!'.format(message.from_user, bot.get_me(), parse_mode='html'), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(message):
    def send_post():
        for post in posts:
            bot.send_message(message.chat.id, 'https://i.playground.ru/e/' + post['img']  + "\n" + post['h1']+"\n \n"+post['p'])

    schedule.every(1).minutes.do(send_post)
    if message.chat.type == "private":
        while True:
            if message.text == 'OK':
                schedule.run_pending()
                time.sleep(100000)
            else:
                bot.send_message(message.chat.id, "Good bye")
                schedule.clear()
                time.sleep(100000)
                break

bot.polling()
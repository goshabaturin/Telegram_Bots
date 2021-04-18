	# -*- coding: utf-8 -*-
import requests
from lxml import html
import re
import telebot
from telebot import types
import operator 
import time
import botan as botan
import datetime

TOKEN = "422221988:AAEo9HHNHuqxJ9452cLR3_eUezur84Tgv9A"
bot = telebot.TeleBot(TOKEN)

botan_key = "bfae3c70-be9f-476e-9c34-62de269feee0"

@bot.message_handler(commands=['start'])
def start(m):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
	bot.send_message(m.chat.id, 'Бот показывает лучшие курсы обмена Валюты по Владивостоку.')
	bot.send_message(m.chat.id, 'Данный бот был действительно создан Георгием Батуриным. А Вы, скорее всего, узнали о нем через его резюме. Для связи с автором просто позвоните: +7(914)076-74-13')
	
	if m.chat.id !=222306228:
		bot.send_message(222306228,"Новый юзер с id {}".format(m.chat.id))

	msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
	bot.register_next_step_handler(msg, name)
	botan.track(botan_key, m.chat.id, m,"валюта")


def name(m):
	
	resp = requests.get('http://www.vl.ru/dengi/')
	parsed_body = html.fromstring(resp.text)
	bank = '//*[@class="link rates-desktop__bank-name"]/text()'#веделяем столбик 'название банка доллара'
	bank = parsed_body.xpath(bank)
		
#________________________________________ для Доллара_______________________________________________________________	
	if m.text == u"\u0024":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(*[types.KeyboardButton(name) for name in ['Купить $', 'Продать $']])
		msg = bot.send_message(m.chat.id, 'Хотите купить или продать?' ,reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)
		print ('user:{}  on {} and was interesting in {}'.format(m.chat.id, datetime.datetime.now(),u"\u0024"))

	if m.text == "Купить $":
		sell_dollars = {}
		try:
			for i in range(1,100):
				s_b = '//table[@class="rates-tablet__table"]/tbody[2]/tr['+str(i)+']/td[position()=1 and not(contains(@class, "disabled"))]/div[2]/span/text()'#веделяем столбик 'продажа доллара'
				try:
					s_b = parsed_body.xpath(s_b)
					sell_dollars[bank[i-1]]=re.sub(r'\s', '', s_b[0])
				except (IndexError):
					sell_dollars[bank[i-1]]=" "
		except(IndexError):
				sort = sorted(sell_dollars.items(),key = operator.itemgetter(1),reverse = True)
				sell_dollars_sort=[]
				
				for element in sort:
					if element[1]!=" ":
						sell_dollars_sort.append(element)
				
				bot.send_message(m.chat.id, 'Банк продаст доллары в лучшем случае по '+sell_dollars_sort[-1][1]+' ('+sell_dollars_sort[-1][0]+')')
				sort.clear()
				sell_dollars.clear()
				sell_dollars_sort.clear()
				botan.track(botan_key, m.chat.id, m,"купить доллары")
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)
		
	

	if m.text == "Продать $":
		buy_dollars = {}
		try:
			for i in range(1,100):
				b_b= '//table[contains(@class,"rates-tablet__table")]/tbody[2]/tr['+str(i)+']/td[position()=1 and not(contains(@class, "disabled"))]/div[1]/span/text()'#веделяем столбик 'продажа доллара'
				try:
					b_b = parsed_body.xpath(b_b)
					buy_dollars[bank[i-1]]=re.sub(r'\s', '', b_b[0])
				except (IndexError):
					buy_dollars[bank[i-1]]=" "
		except(IndexError):
			sort = sorted(buy_dollars.items(),key = operator.itemgetter(1),reverse = True)
			buy_dollars_sort=[]
			
			for element in sort:
				if element[1]!=" ":
					buy_dollars_sort.append(element)

			bot.send_message(m.chat.id, 'Банк купит доллары в лучшем случае по '+buy_dollars_sort[0][1]+' ('+buy_dollars_sort[0][0]+')')
			sort.clear()
			buy_dollars.clear()
			buy_dollars_sort.clear()
			botan.track(botan_key, m.chat.id, m,"продать доллары")
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		
		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)


#________________________________________ для ЕВРО_______________________________________________________________
	if m.text == u"\u20AC":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(*[types.KeyboardButton(name) for name in ['Купить '+u"\u20AC", 'Продать '+u"\u20AC" ]])
		msg = bot.send_message(m.chat.id, 'Хотите купить или продать?' ,reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)
		print ('user:{}  on {} and was interesting in {}'.format(m.chat.id, datetime.datetime.now(),u"\u20AC"))

	if m.text == "Купить "+u"\u20AC":
		sell_euro = {}
		try:
				for i in range(1,100):
					s_e = '//table[@class="rates-tablet__table"]/tbody[2]/tr['+str(i)+']/td[position()=2 and not(contains(@class, "disabled"))]/div[2]/span/text()'#веделяем столбик 'продажа доллара'
					try:
						s_e = parsed_body.xpath(s_e)
						sell_euro[bank[i-1]]=re.sub(r'\s', '', s_e[0])
					except (IndexError):
						sell_euro[bank[i-1]]=" "
		except(IndexError):
				sort = sorted(sell_euro.items(),key = operator.itemgetter(1),reverse = True)
				sell_euro_sort=[]
				
				for element in sort:
					if element[1]!=" ":
						sell_euro_sort.append(element)
				
				bot.send_message(m.chat.id, 'Банк продаст евро в лучшем случае по '+sell_euro_sort[-1][1]+' ('+sell_euro_sort[-1][0]+')')
				sort.clear()
				sell_euro.clear()
				sell_euro_sort.clear()
				botan.track(botan_key, m.chat.id, m,"купить евро")
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)	





	if m.text == "Продать "+ u"\u20AC":
		buy_euro = {}
		try:
			for i in range(1,100):
				b_euro = '//table[contains(@class,"rates-tablet__table")]/tbody[2]/tr['+str(i)+']/td[position()=2 and not(contains(@class, "disabled"))]/div[1]/span/text()'#веделяем столбик 'продажа доллара'
				try:
					b_euro = parsed_body.xpath(b_euro)
					buy_euro[bank[i-1]]=re.sub(r'\s', '', b_euro[0])
				except (IndexError):
					buy_euro[bank[i-1]]=" "
		except(IndexError):
			sort = sorted(buy_euro.items(),key = operator.itemgetter(1),reverse = True)
			buy_euro_sort=[]
			
			for element in sort:
				if element[1]!=" ":
					buy_euro_sort.append(element)

			bot.send_message(m.chat.id, 'Банк купит евро в лучшем случае по '+buy_euro_sort[0][1]+' ('+buy_euro_sort[0][0]+')')
			sort.clear()
			buy_euro.clear()
			buy_euro_sort.clear()
			botan.track(botan_key, m.chat.id, m,"продать евро")
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		
		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)


#________________________________________ для Юаня_______________________________________________________________
	if m.text == u"\u5713":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(*[types.KeyboardButton(name) for name in ['Купить '+u"\u5713", 'Продать '+u"\u5713" ]])
		msg = bot.send_message(m.chat.id, 'Хотите купить или продать?' ,reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)
		print ('user:{}  on {} and was interesting in {}'.format(m.chat.id, datetime.datetime.now(),u"\u5713"))
	
	if m.text == "Купить "+u"\u5713":
		sell_cny = {}
		try:
				for i in range(1,100):
					s_c = '//table[@class="rates-tablet__table"]/tbody[2]/tr['+str(i)+']/td[position()=3 and not(contains(@class, "disabled"))]/div[2]/span/text()'#веделяем столбик 'продажа доллара'
					try:
						s_c = parsed_body.xpath(s_c)
						sell_cny[bank[i-1]]=re.sub(r'\s', '', s_c[0])
					except (IndexError):
						sell_cny[bank[i-1]]=" "
		except(IndexError):
				sort = sorted(sell_cny.items(),key = operator.itemgetter(1),reverse = True)
				sell_cny_sort=[]
				
				for element in sort:
					if element[1]!=" ":
						sell_cny_sort.append(element)
				
				bot.send_message(m.chat.id, 'Банк продаст китайские юани в лучшем случае по '+sell_cny_sort[-1][1]+' ('+sell_cny_sort[-1][0]+')')
				sort.clear()
				sell_cny.clear()
				sell_cny_sort.clear()
				botan.track(botan_key, m.chat.id, m,"купить юани")
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)	

	if m.text == "Продать "+ u"\u5713":
		buy_cny = {}
		try:
			for i in range(1,100):
				b_cny = '//table[contains(@class,"rates-tablet__table")]/tbody[2]/tr['+str(i)+']/td[position()=3 and not(contains(@class, "disabled"))]/div[1]/span/text()'#веделяем столбик 'продажа доллара'
				try:
					b_cny = parsed_body.xpath(b_cny)
					buy_cny[bank[i-1]]=re.sub(r'\s', '', b_cny[0])
				except (IndexError):
					buy_cny[bank[i-1]]=" "
		except(IndexError):
			sort = sorted(buy_cny.items(),key = operator.itemgetter(1),reverse = True)
			buy_cny_sort=[]
			
			for element in sort:
				if element[1]!=" ":
					buy_cny_sort.append(element)

			bot.send_message(m.chat.id, 'Банк купит китайские юани в лучшем случае по '+buy_cny_sort[0][1]+' ('+buy_cny_sort[0][0]+')')
			sort.clear()
			buy_cny.clear()
			buy_cny_sort.clear()
			botan.track(botan_key, m.chat.id, m,"продать юани")
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	
		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)

#________________________________________ для Йены_______________________________________________________________
	if m.text == u"\uFFE5":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(*[types.KeyboardButton(name) for name in ['Купить '+u"\uFFE5", 'Продать '+u"\uFFE5" ]])
		msg = bot.send_message(m.chat.id, 'Хотите купить или продать?' ,reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)
		print ('user:{}  on {} and was interesting in {}'.format(m.chat.id, datetime.datetime.now(),u"\uFFE5"))
	
	if m.text == "Купить "+u"\uFFE5":
		sell_y = {}
		try:
				for i in range(1,100):
					s_y = '//table[@class="rates-tablet__table"]/tbody[2]/tr['+str(i)+']/td[position()=4 and not(contains(@class, "disabled"))]/div[2]/span/text()'#веделяем столбик 'продажа доллара'
					try:
						s_y = parsed_body.xpath(s_y)
						sell_y[bank[i-1]]=re.sub(r'\s', '', s_y[0])
					except (IndexError):
						sell_y[bank[i-1]]=" "
		except(IndexError):
				sort = sorted(sell_y.items(),key = operator.itemgetter(1),reverse = True)
				sell_y_sort=[]
				
				for element in sort:
					if element[1]!=" ":
						sell_y_sort.append(element)
				
				bot.send_message(m.chat.id, 'Банк продаст японские йены в лучшем случае по '+sell_y_sort[-1][1]+' ('+sell_y_sort[-1][0]+')')
				sort.clear()
				sell_y.clear()
				sell_y_sort.clear()
				botan.track(botan_key, m.chat.id, m,"купить йены")
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		
		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)	

	if m.text == "Продать "+ u"\uFFE5":
		buy_y = {}
		try:
			for i in range(1,100):
				b_y = '//table[contains(@class,"rates-tablet__table")]/tbody[2]/tr['+str(i)+']/td[position()=4 and not(contains(@class, "disabled"))]/div[1]/span/text()'#веделяем столбик 'продажа доллара'
				try:
					b_y = parsed_body.xpath(b_y)
					buy_y[bank[i-1]]=re.sub(r'\s', '', b_y[0])
				except (IndexError):
					buy_y[bank[i-1]]=" "
		except(IndexError):
			sort = sorted(buy_y.items(),key = operator.itemgetter(1),reverse = True)
			buy_y_sort=[]
			
			for element in sort:
				if element[1]!=" ":
					buy_y_sort.append(element)

			bot.send_message(m.chat.id, 'Банк купит японские йены в лучшем случае по '+buy_y_sort[0][1]+' ('+buy_y_sort[0][0]+')')
			sort.clear()
			buy_y.clear()
			buy_y_sort.clear()
			botan.track(botan_key, m.chat.id, m,"продать йены")
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		
		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)
		
#________________________________________ для Корейской Воны_______________________________________________________________
	if m.text == u"\u20A9":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(*[types.KeyboardButton(name) for name in ['Купить '+u"\u20A9", 'Продать '+u"\u20A9" ]])
		msg = bot.send_message(m.chat.id, 'Хотите купить или продать?' ,reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)
		print ('user:{}  on {} and was interesting in {}'.format(m.chat.id, datetime.datetime.now(),u"\u20A9"))
	
	if m.text == "Купить "+u"\u20A9":
		sell_w = {}
		try:
			for i in range(1,100):
				s_w = '//table[@class="rates-tablet__table"]/tbody[2]/tr['+str(i)+']/td[position()=5 and not(contains(@class, "disabled"))]/div[2]/span/text()'#веделяем столбик 'продажа доллара'
				try:
					s_w = parsed_body.xpath(s_w)
					sell_w[bank[i-1]]=re.sub(r'\s', '', s_w[0])
				except (IndexError):
					sell_w[bank[i-1]]=" "
		except(IndexError):
				sort = sorted(sell_w.items(),key = operator.itemgetter(1),reverse = True)
				sell_w_sort=[]
				
				for element in sort:
					if element[1]!=" ":
						sell_w_sort.append(element)
				
				bot.send_message(m.chat.id, 'Банк продаст южнокорейские воны в лучшем случае по '+sell_w_sort[-1][1]+' ('+sell_w_sort[-1][0]+')')
				sort.clear()
				sell_w.clear()
				sell_w_sort.clear()
				botan.track(botan_key, m.chat.id, m,"купить воны")
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		
		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5", u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)	

	if m.text == "Продать "+ u"\u20A9":
		buy_w = {}
		try:
			for i in range(1,100):
				b_w = '//table[contains(@class,"rates-tablet__table")]/tbody[2]/tr['+str(i)+']/td[position()=5 and not(contains(@class, "disabled"))]/div[1]/span/text()'#веделяем столбик 'продажа доллара'
				try:
					b_w = parsed_body.xpath(b_w)
					buy_w[bank[i-1]]=re.sub(r'\s', '', b_w[0])
				except (IndexError):
					buy_w[bank[i-1]]=" "
		except(IndexError):
			sort = sorted(buy_w.items(),key = operator.itemgetter(1),reverse = True)
			buy_w_sort=[]
			
			for element in sort:
				if element[1]!=" ":
					buy_w_sort.append(element)

			bot.send_message(m.chat.id, 'Банк купит корейские воны в лучшем случае по '+buy_w_sort[0][1]+' ('+buy_w_sort[0][0]+')')
			sort.clear()
			buy_w.clear()
			buy_w_sort.clear()
			botan.track(botan_key, m.chat.id, m,"продать воны")
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		
		keyboard.add(*[types.KeyboardButton(name) for name in [u"\u5713", u"\uFFE5",u"\u20A9", u"\u0024", u"\u20AC"]])
		msg = bot.send_message(m.chat.id, 'Какую валюту желаете?', reply_markup=keyboard)
		bot.register_next_step_handler(msg, name)

while True:
	try:
		bot.polling(none_stop=True)

	except: 
		time.sleep(5)


#resp = requests.get('http://www.vl.ru/dengi/')
#parsed_body = html.fromstring(resp.text)

#buy_dollars = {}
#bank = '//*[@class="link rates-desktop__bank-name"]/text()'#веделяем столбик 'продажа доллара'
#bank = parsed_body.xpath(bank)
##print(bank)
#try:
#	for i in range(1,100):
#		b_b = '//table[@class="rates-tablet__table"]/tbody[2]/tr['+str(i)+']/td[1]/div[1]/span/text()'#веделяем столбик 'продажа доллара'
#		b_b = parsed_body.xpath(b_b)
		
#		buy_dollars[bank[i-1]]=re.sub(r'\s', '', b_b[0])



##s_b = '//*[@class="link rates-desktop__bank-name"]/text()'#веделяем столбик 'продажа доллара'
##s_b = parsed_body.xpath(s_b)
##print(s_b)


#except(IndexError):
#	import operator 

#	for i in buy_dollars.keys():
#		 print(i, '-', buy_dollars[i], end='; \n')
#	print('___________________')	 
	

#	buy_dollars_sort = sorted(buy_dollars.items(),key = operator.itemgetter(1),reverse = True)
#	print('Лучший курс в  '+buy_dollars_sort[0][0]+'\n'+buy_dollars_sort[0][1])
	
	



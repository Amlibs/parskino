from bs4 import BeautifulSoup
import requests
import re
import bd_interface


def CountSeats(url, schedulesoup):
	#print('я работаю на вайлд ист!')
	#print(url + hreffilm)

	allSeats = 0
	notFreeSeats = 0
	allSchedule = schedulesoup.findAll('a', class_='a1DGomhf4lH5LTLg921s')

	for orderpage in allSchedule:

		if orderpage.get('href') is not None and re.fullmatch(r'/[a-zA-z]+/[0-9]+', orderpage.get('href')):
			hrefsorderpages = orderpage.get('href')
			orderpage = requests.get(url + hrefsorderpages)

			if orderpage.status_code != 200:
				print(orderpage.status_code)
				continue
			
			oredersoup = BeautifulSoup(orderpage.text, 'html.parser')
			allSeats += len(oredersoup.findAll('div', class_='tOBn8791Pc0pPlDUH7kq'))
			exampleSeats = len(oredersoup.findAll('div', class_='GRSsamfB2qf9kRFQSwe9'))
			allSeats -= exampleSeats
			notFreeSeats += len(oredersoup.findAll('div', class_='Qbd4PCPZ8SFFTdqiCqHJ')) - 1
			
	return [allSeats, notFreeSeats]


def parser():
	url = 'https://kinomax.ru'
	page = requests.get(url)

	soup = BeautifulSoup(page.text, 'html.parser')
	allFilms = []
	allFilms = soup.findAll('a', class_='SJ7_iJC5cQHgRsOlc3Z_')
	hrefFilmsPages = {}
	nameCountSeats = {}
	total = len(allFilms)
	current = 0

	for poster in allFilms:
		current += 1
		print('Собираю информацию по фильмам')
		print(f'{current} / {total}')
		if re.fullmatch(r'/[a-zA-z]+/[0-9]+', poster.get('href')):
			hreffilm = poster.get('href')
			schedulepage = requests.get(url + hreffilm)

			if schedulepage.status_code != 200:
				continue

			schedulesoup = BeautifulSoup(schedulepage.text, 'html.parser')

			if schedulesoup.find('h1', class_='mB9UeZRNnd7pyA0pAUx_') is not None:
				name = schedulesoup.find('h1', class_='mB9UeZRNnd7pyA0pAUx_')
				name = name.text

				if name in nameCountSeats:
					temp = CountSeats(url, schedulesoup)
					nameCountSeats[name][0] += temp[0]
					nameCountSeats[name][1] += temp[1]
				else:
					nameCountSeats[name] = CountSeats(url, schedulesoup)

	for i in nameCountSeats:
		print(f"В фильме {i} всего {nameCountSeats[i][0]} мест, занято из них {nameCountSeats[i][1]}")
		bd_interface.creareDB()
		bd_interface.writeToDB(str(i), nameCountSeats[i][0], nameCountSeats[i][1])

import requests
from bs4 import BeautifulSoup
import re

COMPANY_ID = {'皇家加勒比邮轮公司': 18702, '歌诗达邮轮': 18682, '美国公主邮轮': 18720, 'MSC地中海邮轮':18761, '天海邮轮公司' : 19501}

def get_lineMsg(s, company, page):
	url = 'http://www.lvmama.com/youlun/line-l660-s0-b' + str(COMPANY_ID[company]) + '-m0.html?' + 'p=' + str(page)
	content = s.get(url).content.decode('utf-8')

	date = re.findall(re.compile(r'开航日期：(\d+/\d+)'),content)

	if not date:
		print('未能抓取到数据，请重试')
		input('...')
		run()

	cruise = re.findall(re.compile(r'【(.*?)】'), content)
	hotel = []
	price = []
	link = []
	secPrice = []
	childPrice = []

	soup = BeautifulSoup(content, "html.parser")
	
	for header in soup.find_all("h4"):
		try:
			link.append(re.findall(re.compile(r'(href=")(.*?)("\s)'), str(header))[0][1])
		except IndexError as e:
			print("cannot find the link")

	print('访问网络中...')
	item = 1
	for l in link:
		tmp_hotel, tmp_price, tmp_secPrice, tmp_childPrice = [], [] ,[], []

		hotel_type = s.get(l).content.decode('utf-8')
		soup = BeautifulSoup(hotel_type, "html.parser")
		data = soup.find_all(class_ = re.compile('kefang'))

		for d in data:
			if d.has_attr('data-branchname'):
				tmp_hotel.append(d['data-branchname'])
			if d.has_attr('data-fstprice'):
				tmp_price.append(d['data-fstprice'])

			if d.has_attr('data-secprice'):
				tmp_secPrice.append(d['data-secprice'])
			else:
				tmp_secPrice.append('None')

			if d.has_attr('data-childprice'):
				tmp_childPrice.append(d['data-childprice'])
			else:
				tmp_childPrice.append('None')

		hotel.append(tmp_hotel)
		price.append(tmp_price)
		secPrice.append(tmp_secPrice)
		childPrice.append(tmp_childPrice)

		print("item {0} scaned".format(item))
		item += 1


	return date, cruise, hotel, price, secPrice, childPrice, link

def run():
	s = requests.session()	
	filename = input('请输入你想保存数据的文件名（format: xxx.csv）: ')
	all_page = int(input('请输入你需要抓取的页数 : '))
	company = input('请输入你想抓取的公司 : ')

	page = 1 	
	file = open(filename, 'w')
	file.write('日期, 航线,房型,第1.2人价格,第3.4成人价格,第3.4儿童价格' + '\n')

	while page <= all_page:
		dates, cruises, hotels, prices, secPrices, childPrices, links = get_lineMsg(s, company, page)

		for date, cruise, hotel, price, secPrice, childPrice, link in zip(dates, cruises, hotels, prices, secPrices, childPrices, links):
			for h, p, sec, c in zip(hotel, price, secPrice, childPrice):
				file.write(date + ',' + cruise + ',' + h + ',' + p + ',' + str(sec) + ',' + str(c) + ',' + link)
				file.write("\n")

		print('第 {0} 页爬虫结束...'.format(page))
		page += 1

	file.close()


if __name__ == '__main__':
	run()
	input('press any button to continue...')
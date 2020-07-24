# @ file Coupon.py
# @ brief Class Coupon Implementation

# Class Coupon contain four method get_farm(), get_efun(), get_don(), get_hakka()
# each method do http request to get data from website, return a dictionary as well ae write to json file

# @ auther Leo Chen
# @ date 2020/07/24

from bs4 import BeautifulSoup
import requests
import json
import os

class Coupon(object):

	url_farm = 'https://ezgo.coa.gov.tw/zh-TW/Front/ETicket/StoreDataJson'
	url_don = 'https://don500.sa.gov.tw/FOAS/actions/Vendor.action?search'
	url_efun = 'https://artsfungo.moc.gov.tw/promote_s/public/page'
	url_hakka = 'https://line.369hakka.com.tw/api/store/getShopList/'
	
	def __init__(self):
		super(Coupon, self).__init__()


	def get_farm(this):

		print('Excuting get_farm...')
		data_farm = { 'data': [] }

		# http request with header
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
		}
		stores = requests.get(this.url_farm, headers=headers).json()

		# reorganize the data and pick critical data
		for store in stores:
			new_json = {}
			new_json['name'] = store['N']
			new_json['address'] = store['A']
			new_json['tel'] = store['T'].replace('-', '')
			new_json['website'] = ''

			data_farm['data'].append(new_json)

		# write as json file
		with open(os.path.join('data', 'farm'), 'w', encoding='utf-8') as f:
			json.dump(data_farm, f, ensure_ascii=False)

		return data_farm
		

	def get_efun(this):

		print('Excuting get_efun...')
		data_efun = { 'data': [] }

		# get the number of stores
		headers = {
			'Content-Type': 'application/json; charset=UTF-8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
		}
		payload_data = {
		    "currentPage":1,
		    "pageSize":1,
		    "handler":"storeRepository#searchStore",
		    "params":{}
		}
		store_count = requests.post(this.url_efun, data=json.dumps(payload_data),headers=headers).json()['total']

		# get the whole store data
		payload_data['pageSize'] = store_count
		stores = requests.post(this.url_efun, data=json.dumps(payload_data),headers=headers).json()['result']
		
		# reorganize the data and pick critical data
		for store in stores:
			new_json = {}
			new_json['name'] = store['culName']
			new_json['address'] = store['city'] + store['area'] + store['address']
			# handle tel==None situation
			if store['tel'] != None:
				new_json['tel'] = store['tel'].replace('-', '')
			# if there is no website, replace by facebook link
			if store['website'] == '':
				new_json['website'] = store['fb']
			else:
				new_json['website'] = store['website']

			data_efun['data'].append(new_json)

		# write as json file
		with open(os.path.join('data', 'efun'), 'w', encoding='utf-8') as f:
			json.dump(data_efun, f, ensure_ascii=False)

		return data_efun


	def get_don(this):

		print('Excuting get_don, it may take a few minutes...')
		data_don = { 'data': [] }

		headers = {
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
		}

		# get the number of pages
		form_data = "page=1&cityCode=&keyword="
		store_count = requests.post(this.url_don, data=form_data, headers=headers).json()['countRow']
		page_count = int(store_count / 30) + 1


		for i in range(page_count):

			form_data = "page=" + str(i+1) +  "&cityCode=&keyword="
			stores = requests.post(this.url_don, data=form_data, headers=headers).json()['list']

			for store in stores:
				seqno = store['seqno']

				# get information from html page
				subpage_url = 'https://don500.sa.gov.tw/FOAS/actions/Vendor.action?productList&seqno=' + seqno
				html = requests.get(subpage_url).text
				html = BeautifulSoup(html, "lxml")
				store_info = html.select('.card-body.py-5')[0]

				new_json = {}
				new_json['name'] = store_info.select('.my-3.pt-1')[0].text
				new_json['address'] = store_info.select('.mb-0')[0].text[9:]
				new_json['tel'] = store_info.select('.mb-0')[1].text[5:].replace('-', '')
				new_json['website'] = store_info.select('.mb-0')[3].select('a')[0].text

				data_don['data'].append(new_json)

		# write as json file
		with open(os.path.join('data', 'don'), 'w', encoding='utf-8') as f:
			json.dump(data_don, f, ensure_ascii=False)

		return data_don


	def get_hakka(this):

		print('Excuting get_hakka, it may take a few minutes...')
		data_hakka = { 'data': [] }

		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
		}

		city_list, dist_list = [], []
		area_info = requests.get('https://line.369hakka.com.tw/campaign/hakka/assets/js/postalcode.json', headers=headers).json()

		# transform json in two lists(city_list, dist_list)
		for city in area_info.keys():
			city_list.append(city)
			temp_dist = []
			for dists in area_info[city]:
				temp_dist.append(dists['district'])
			dist_list.append(temp_dist)

		# go through all city and district
		for city in city_list:
			for district in dist_list[city_list.index(city)]:

				form_data =  {
				    'city': city,
				    'dist': district,
				    'start': '0',
				    'end': '50'
				}

				stores = requests.post(this.url_hakka, data=form_data, headers=headers).json()['query']
				for store in stores:
					new_json = {}
					new_json['name'] = store['store_name']
					new_json['address'] = store['city'] + store['dist'] + store['address']
					new_json['tel'] = ''
					new_json['website'] = ''

					data_hakka['data'].append(new_json)

		# write as json file
		with open(os.path.join('data', 'hakka'), 'w', encoding='utf-8') as f:
			json.dump(data_hakka, f, ensure_ascii=False)

		return data_hakka
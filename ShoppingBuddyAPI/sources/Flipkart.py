from bs4 import BeautifulSoup
import requests
import re
import json

class FlipkartScrapper():

	soup = None
	url = None

	def __init__(self, _url):
		self.url = _url
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
		response=requests.get(_url,headers=headers)
		self.soup=BeautifulSoup(response.content,'lxml')

	def get_features_css(self):
		'''
		@DeprecatedWarning
		Function to scrape products features using css selectors.
		Used earlier. Retained kept for reference. 
		Returns:
			features: dict
				Features of product.
		'''
		all_trs = self.soup.find_all(class_='_3_6Uyw row')[1:]

		specs = {self.get_key(row) : self.get_value(row) for row in all_trs}
		specs = {k: v for k, v in specs.items() if v is not None} # Remove Disclaimer and Important Notice info which have Null values and actual content as key
		return specs

	def get_features(self):
		'''
		Function to scrape products features using container id and no css selector.
		Returns: 
			features: dict
				Features of product
		'''
		feature_sections = self.soup.find(id="container").div.contents[2].contents[0].contents[1].contents[7].contents[4].div.contents[1].contents[0]
		specs = {}
		for feature_section in feature_sections:
			for row in feature_section.table.tbody:
				specs[self.get_key(row)]=self.get_value(row)
		specs = {k: v for k, v in specs.items() if v is not None} # Remove Disclaimer and Important Notice info which have Null values and actual content as key
		return specs

	def get_key(self, tr):
		'''
		Helper method to parse features.
		Returns:
			key:
				Name of feature in a features table row.
		'''
		td = tr.contents[0]
		key = td.contents[0]
		return key

	def get_single_value_if_singly_list(self, ul):
		'''
		Helper method to parse fatures.
		Returns:
			
		'''
		lis = ul.find_all("li")
		if len(lis) == 1:
			return lis[0].string
		return ul

	def get_value(self, tr):
		'''
		Helper method to parse features.Returns.
		Returns:
			value:
				Value of features in a features table row.
		'''
		if len(tr.contents) == 2 : # Rows corresponding to following are not key: values, but just description: In The Box, Disclaimer, Important Note etc
			td = tr.contents[1]
			value = td.contents[0]
			return self.get_single_value_if_singly_list(value)

	def get_title_css(self):
		'''
		@DeprecatedWarning
		Returns title  by scraping dom using css selector.
		Used earlier. Retained kept for reference. 
		'''
		return self.soup.find_all(class_='_35KyD6')[0].contents[0]
		
		
	def get_title(self):
		'''
        The function to scrape Title of the product.
        Returns:
            title: str
                Title of the product
        '''
		return self.soup.find(id="container").div.contents[2].contents[0].contents[1].contents[1].div.contents[0].h1.span.text


	def get_sales_price_css(self):
		'''
		@DeprecatedWarning
		Returns sales price by scraping dom using css selector.
		Used earlier. Retained kept for reference. 
		'''
		return self.soup.find_all(class_='_1vC4OE _3qQ9m1')[0].contents[0]
		#//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]

	def get_sales_price(self):
		'''
        The function to scrape price of the product.
		XPath = #//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]
        Returns:
            price: str
                Selling price of the product
        '''
		#return self.soup.find(id="container").div.contents[2].contents[0].contents[1].contents[1].div.contents[2].contents[0].div.contents[0].text
		return self.soup.find(id="container").div.contents[2].contents[0].contents[1].contents[1].div.contents[3].contents[0].div.contents[0].text

	def get_mrp_price_css(self):
		'''
		@DeprecatedWarning
		Returns mrp price by scraping dom using css selector.
		Used earlier. Retained kept for reference. 
		'''
		return self.soup.find_all(class_='_3auQ3N _1POkHg')[0].contents[2]

	def get_mrp_price(self):
		'''
        The function to scrape price of the product.
		XPath = //*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]
		FUll XPath = /html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]
        Returns:
            mrp: str
                M.R.P. of the product
        '''
		#Full XPath version:
		#return self.soup.html.body.contents[0].div.contents[2].contents[0].contents[1].contents[1].div.contents[2].contents[0].div.contents[1].text
		return self.soup.find(id="container").div.contents[2].contents[0].contents[1].contents[1].div.contents[3].contents[0].div.contents[1].text

	def get_number_of_ratings_css(self):
		'''
		@DeprecatedWarning
		Returns number of ratings by scraping dom using css selector.
		Used earlier. Retained kept for reference. 
		'''
		try:
			return str(self.soup.find_all(class_='_38sUEc')[0].contents[0].contents[0].contents[0].string).split()[0]
		except: #AttributeError: 'NavigableString' object has no attribute 'contents'
			try:
				return self.soup.find_all(class_='_38sUEc')[0].contents[0].contents[0].split()[0] 
			except:
				return ""
			
		# return str(self.soup.find_all(class_='_38sUEc')[0].contents[0].contents[0].contents[0].string).split()[0]

	def get_number_of_ratings(self):
		'''
		Returns number of ratings by scraping dom using container id and no css selector.
		XPath = //*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[1]
		FUll XPath = /html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[1]
		'''
		try:
			#Full XPath version:
			#return self.soup.html.body.contents[0].div.contents[2].contents[0].contents[1].contents[1].div.contents[1].div.div.contents[1].span.contents[0].text.split()[0]
			return  self.soup.find(id="container").div.contents[2].contents[0].contents[1].contents[1].div.contents[1].div.div.contents[1].span.contents[0].text.split()[0]
		except: #AttributeError: 'NavigableString' object has no attribute 'contents'
			try:
				return self.soup.find_all(class_='_38sUEc')[0].contents[0].contents[0].split()[0] 
			except:
				return ""
			
		# return str(self.soup.find_all(class_='_38sUEc')[0].contents[0].contents[0].contents[0].string).split()[0]
		

	def get_ratings_css(self):
		'''
		@DeprecatedWarning
		Returns ratings by scraping dom using css selector.
		Used earlier. Retained kept for reference. 
		'''
		return self.soup.find_all(class_='_2_KrJI')[0].contents[0].contents[0]

	def get_ratings(self):
		'''
		Function to scrape product ratings.
		XPath = //*[@id="productRating_LSTCOMFRZFDQRBETGKNJKSMLX_COMFRZFDQRBETGKN_"]/div
		FUll XPath = /html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[2]/div/div/span[1]/div

		Returns: ratings by scraping dom using container id and no css selector.
			ratings: str
				Rating of product
		'''
		#Full XPath version:
		#return self.soup.html.body.contents[0].div.contents[2].contents[0].contents[1].contents[1].div.contents[1].div.div.contents[0].div.text
		return self.soup.find(id="container").div.contents[2].contents[0].contents[1].contents[1].div.contents[1].div.div.contents[0].div.text
	
	def get_info(self):
		'''
		Function to scrape all product information.
		Returns:
			product_info: dict
				Disctionary of product information.
		'''
		product_info = {}
		product_info['URL'] = self.url
		product_info['features'] = self.get_features()
		product_info['Title'] = self.get_title()
		product_info['Price'] = self.get_sales_price()
		product_info['MRP'] = self.get_mrp_price()
		product_info['Ratings'] = self.get_ratings()
		product_info['Number Of Ratings'] = self.get_number_of_ratings()
		return product_info


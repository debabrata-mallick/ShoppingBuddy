import requests
from bs4 import BeautifulSoup

class AmazonScrapper:
    '''
    This is a class for scrapping product details from an Amazon website.
    ...
    Attributes:
        url: str
            The Amazon website URL of the product which needs to be scrapped.
        soup: BeautifulSoup object 
            BeautifulSoup object of the Amazon website.
    '''
    def __init__(self,url):
        '''
        The constructor of AmazonScrapper class.
        Parameters:
            url: str
                The Amazon website URL of the product which needs to be scrapped.
        '''
        HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
        page = requests.get(url, headers=HEADERS)
        self.url=url
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def get_title(self):
        '''
        The function to scrape Title of the product.
        Returns:
            title: str
                Title of the product
        '''
        try:
            prodtitle = self.soup.find("span", id = "productTitle")
            title = prodtitle.get_text().strip()
            return title
        except:
            return None

    def get_features(self):
        '''
        The function to scrape features of the product.
        Returns:
            features: Dictionary
                A key value dictionary of product features 
        '''
        prodtable = self.soup.find("table",{"class":'a-keyvalue prodDetTable'})
        features={}
        if prodtable is not None:
            for tr in prodtable.findAll("tr"):
                th=tr.find("th")
                td=tr.find("td")
                if th is not None and td is not None:
                    key = str(th.get_text())
                    val = str(td.get_text())
                    features[key.strip()]=val.strip()

        return features

    def get_price(self):
        '''
        The function to scrape price of the product.
        Returns:
            mrp: str
                M.R.P. of the product
            price: str
                Selling price of the product
        '''
        mrp="Not Available"
        price="Not Available"
        try:
            pricetable = self.soup.find("div",id="price").find("table")
        
            for tr in pricetable.findAll("tr"):
                td=tr.findAll("td")
                header = str(td[0].get_text())
                if  header== 'M.R.P.:':
                    val = td[1].findAll("span")
                    if val is not None:
                        mrp=val[0].get_text().strip()
                elif header == 'Price:' or header == 'Deal of the Day:':
                    val = td[1].findAll("span")
                    if val is not None:
                        price=val[0].get_text().strip()
        except:
            pass
        return mrp,price

    def get_ratings(self):
        '''
        The function to scrape user ratings of the product.
        Returns:
            rating: str
                Rating of the product
        '''
        try:
            ratingdiv=self.soup.find("div",id="averageCustomerReviews")
            ratingString= str(ratingdiv.get_text())
            rating= ratingString.strip().split()[0]
            return rating
        except:
            return 0
        
    def get_number_of_ratings(self):
        '''
        The function to scrape the number of users who have given rating of the product.
        Returns:
            n:str
                Number of ratings of the product
        '''
        try:
            ratingspan=self.soup.find("span",id="acrCustomerReviewText")
            n= str(ratingspan.string).strip().split()[0]
            return n
        except:
            return 0

    def get_info(self):
        '''
        The function to scrape all the information of the product.
        Returns:
            product_info: Dictionary
                Dictionary of all the information scraped of the product.
        '''
        product_info = {}
        product_info['URL'] = self.url
        product_info['features'] = self.get_features()
        product_info['Title'] = self.get_title()
        product_info['Price'], product_info['MRP'] = self.get_price()
        product_info['Ratings'] = self.get_ratings()
        product_info['Number Of Ratings'] = self.get_number_of_ratings()
        return product_info

    def get_category(self):
        '''
        The function to scrape the category of the product.
        Returns:
            category: str
                category of the product.
        '''
        try:
            detail = self.soup.find("div",id="prodDetails").find("h2").get_text()
            words = detail.split()
            print(words)
            return words[-2]
        except:
            return None
from flask import Blueprint
from flask import request
import json
import pandas as pd
from collections import OrderedDict

from  .sources.Amazon import AmazonScrapper
from .sources.Flipkart import FlipkartScrapper
from .sources.ProductFeature import ProductFeature 

AMAZON_URL='https://www.amazon.in/'
FLIPKART_URL='https://www.flipkart.com/'

bp = Blueprint('compare', __name__)

laptop_info_list = ['URL','Price','MRP','Ratings','Number Of Ratings']

@bp.route('/', methods=['POST'])
def compareProducts():
    req = request.json
    if req['urls'] is None or len(req['urls'])<2:
        return {
            "status": 403,
            "message": "Need at least 2 URLs to compare"
        }

    featureMapper = ProductFeature.getInstance()
    productList=[]
    features_list = []

    category=req['category']
    for url in req['urls']:
        if url.startswith(AMAZON_URL):
            scrapper = AmazonScrapper(url)
            site='Amazon'
        elif url.startswith(FLIPKART_URL):
            scrapper = FlipkartScrapper(url)
            site='Flipkart'
        product=scrapper.get_info()
        productList.append(product)
        product['features'], temp_feature_list = featureMapper.mapProductFeatures(category,product['features'],site)
        features_list.extend(temp_feature_list)

    features_list = list(dict.fromkeys(features_list))
    
    titles = []

    product_index = 1
    for product in productList:
        titles.append(product['Title'])
        product_index += 1

    tabledata = []

    for prod_info in laptop_info_list:
        od = OrderedDict()
        od['feature'] = str(prod_info)
        product_index = 1
        for product in productList:
            od['Product'+str(product_index)]=str(product[prod_info])
            product_index += 1
        tabledata.append(od)

    for prod_feature in features_list:
        od = OrderedDict() 
        od['feature']= str(prod_feature)
        prod_index = 1
        num_products_with_this_feature = 0

        for product in productList:
            pname='Product'+str(prod_index)
            if prod_feature in product['features'] :
                od[pname]=str(product['features'][prod_feature])
                num_products_with_this_feature+=1
            else:
                od[pname]=''

            prod_index += 1

        if num_products_with_this_feature > 0:
            tabledata.append(od)

    return {
            'status': 200,
            'url_count': len(productList),
            'products':tabledata,
            'titles': titles
    }
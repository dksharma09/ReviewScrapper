import requests
from bs4 import BeautifulSoup as bs
import logging
import time


try :
    fileName = str(time.time())
    logging.basicConfig(filename=f'log files/{fileName}.log', encoding='utf-8', level=logging.DEBUG)
except Exception as e :
    logging.error(f'{str(time.strftime)} : Error occurred , str({e})')
 
try :    
    productName = "samsunggalaxy"
    link = "https://www.flipkart.com/search?q=" + productName
    productData = requests.get(link).text
    
    productDataClear = bs(productData, "html.parser")

    productDataClear = productDataClear.find_all('div', {'class' : "_13oc-S"})
    quantity = len(productDataClear)
    print(quantity)
    
    for i in range(quantity) :
        getLink = productDataClear[i].div.div.a['href']
        
        productLink = "https://www.flipkart.com" + getLink
        
        particularProductData = requests.get(productLink).text
        
        particularProductData = bs(particularProductData, 'html.parser')
        
        #ProductName
        findProductName = particularProductData.find('div', {'class' : 'aMaAEs'})
        productName = findProductName.div.h1.span.text
        logging.info(f'{str(time.strftime)} : Product Name = {productName}')
        
        #ProductPrice
        findProductPrice = particularProductData.find('div', {'class' : 'dyC4hf'})
        productPrice = findProductPrice.div.div.div.text
        logging.info(f'{time.strftime} : Product Price = {productPrice}')
        
        findProductHighlights = particularProductData.find('div', {'class' : '_2418kt'})
        findProductHighlights = findProductHighlights.find_all('li', {'class' : '_21Ahn-'})
        for i in range(len(findProductHighlights)) :
            productHighlights = findProductHighlights[i].text
            logging.info(f'{time.strftime} : {i}. Product Highlights = {productHighlights}')
        
        findProductRating = particularProductData.find('div', {'class' : '_2d4LTz'})
        productRating = findProductRating.text
        logging.info(f'{time.strftime} : Product Rating = {productRating}')
        
        findProductReview = particularProductData.find_all('div', {'class' : 'col _2wzgFH'})
        # print(len(findProductReview))
        for i in range(len(findProductReview)) :
            productUserRating = findProductReview[i].div.div.text
            logging.info(f'{time.strftime} : Product User Rating = {productUserRating}')
            productUserReview = findProductReview[i].div.p.text
            logging.info(f'{time.strftime} : Product User Review = {productUserReview}')
    
except Exception as e :
    logging.error(f'{time.strftime} : Error occurred , str({e})')
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
import logging
import time

try :
    fileName = str(time.time())
    logging.basicConfig(filename=f'log files/{fileName}.log', encoding='utf-8', level=logging.DEBUG)
except Exception as e :
    logging.error(f'{str(time.strftime)} : Error occurred , str({e})')

flipkart = 'https://www.flipkart.com/search?q='
app = Flask(__name__)

@app.route("/")
def landingPage() :
    return render_template('index.html')

table_data = []
@app.route("/result", methods=['GET', 'POST'])
def resultPage():
    if request.method != 'POST':
        return render_template('output.html')
    deviceName = request.form['query']
    link = flipkart + deviceName
    # print(link)
    productData = requests.get(link).text

    productDataClear = bs(productData, "html.parser")

    productDataClear = productDataClear.find_all('div', {'class' : "_13oc-S"})
    quantity = len(productDataClear)
    # print(quantity)

    for i in range(quantity) :
        getLink = productDataClear[i].div.div.a['href']

        productLink = f'https://www.flipkart.com{getLink}'
        
        particularProductData = requests.get(productLink).text

        particularProductData = bs(particularProductData, 'html.parser')

        #ProductName
        findProductName = particularProductData.find('div', {'class' : 'aMaAEs'})
        # logging.info(f'{str(time.strftime)} : Product Name = {findProductName}')
        productName = findProductName.div.h1.span.text
        logging.info(f'{str(time.strftime)} : Product Name = {productName}')

        #ProductPrice
        findProductPrice = particularProductData.find('div', {'class' : 'dyC4hf'})
        productPrice = findProductPrice.div.div.div.text
        logging.info(f'{time.strftime} : Product Price = {productPrice}')

        findProductHighlights = particularProductData.find('div', {'class' : '_2418kt'})
        findProductHighlights = findProductHighlights.find_all('li', {'class' : '_21Ahn-'})
        productHighlightsList = []
        for i in range(len(findProductHighlights)) :
            productHighlights = findProductHighlights[i].text
            productHighlightsList.append(productHighlights)
            logging.info(f'{time.strftime} : {i}. Product Highlights = {productHighlights}')

        # findProductRating = particularProductData.find('div', {'class' : '_2d4LTz'})
        # productRating = findProductRating.text
        productRating = 5
        logging.info(f'{time.strftime} : Product Rating = {productRating}')

        findProductReview = particularProductData.find_all('div', {'class' : 'col _2wzgFH'})
        # print(len(findProductReview))
        productUserReviewList = []
        for i in range(len(findProductReview)) :
            productUserRating = findProductReview[i].div.div.text
            logging.info(f'{time.strftime} : Product User Rating = {productUserRating}')
            productUserReview = findProductReview[i].div.p.text
            productUserReviewList.append(productUserReview)
            logging.info(f'{time.strftime} : Product User Review = {productUserReview}')
        table_data.append({'productName':productName, 'productPrice':productPrice, 'productHighlightsList':productHighlightsList, 'productUserReviewList':productUserReviewList})

    return render_template('output.html',table_data=table_data)

if __name__ == "__main__" :
    app.run(debug=True)
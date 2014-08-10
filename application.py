import flask
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

import urllib
import re
import os

import dbutil
 
 
 
 

parks_para = {
'DBNAME': 'trip',
'USER': 'qqq',
'PASSWORD': 'PLMqaz123',
'HOST': 'cq.crfuupun11nn.us-west-1.rds.amazonaws.com',
'PORT': 3306,
}
get = dbutil.DBGet(db_name = parks_para['DBNAME'], db_url = parks_para['HOST'], usr = parks_para['USER'], pwd = parks_para['PASSWORD'])
#get = dbutil.DBGet(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')

application = flask.Flask(__name__) 
@application.route('/')
def index():
    # all_restaurants: what kind of information here? guess: 1 restuarant nm 2 restaurant picture    
    #get = dbutil.DBGet(db_name = parks_para['DBNAME'], db_url = parks_para['HOST'], usr = parks_para['USER'], pwd = parks_para['PASSWORD'])
    #get = dbutil.DBGet(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')
    all_restaurants = get.get_restaurants_park('60999') 
    all_names = [t[1] for t in all_restaurants]

    def get_img_html(restaurant_nm):
        # get = dbutil.DBGet(db_name = parks_para['DBNAME'], db_url = parks_para['HOST'], usr = parks_para['USER'], pwd = parks_para['PASSWORD']) 
        restaurant_id= get.restaurant_nm_id(restaurant_nm)
        url='/search.html?q='+urllib.quote(restaurant_nm)    
        try:
            path = 'yellowstone/%d.jpg' % restaurant_id
        except:
            path = 'no'
        return '<a href="%s" class = "thumbnail"><img src="%s" alt="%s" height = 20pt></a>' % (url, url_for('static', filename=path), restaurant_nm.replace('_', ''))

    
    all_img = [get_img_html(t) for t in all_names]
     
    return render_template('index.html', all_imgs = all_img)
 





@application.route('/search.html')
def search():

    restaurant_nm = request.args.get('q', None) 
    
    #get = dbutil.DBGet(db_name = parks_para['DBNAME'], db_url = parks_para['HOST'], usr = parks_para['USER'], pwd = parks_para['PASSWORD'])
    #get = dbutil.DBGet(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')

    restaurant_id= get.restaurant_nm_id(restaurant_nm)
    restaurant_address = get.restaurant_id_address(restaurant_id)    
    restaurant_phone = get.restaurant_id_phone(restaurant_id)    
    total_num_reviews = get.restaurant_num_reviews(restaurant_id)
    

    def get_thumbnail_url_html(restaurant_nm):
    # return a new webpage including 1 top_quotes and 2 picture 3 url 4 address 5 phone of this restaurant 6 # of reviews
        #get = dbutil.DBGet(db_name = parks_para['DBNAME'], db_url = parks_para['HOST'], usr = parks_para['USER'], pwd = parks_para['PASSWORD']) 
        #restaurant_id= get.restaurant_nm_id(restaurant_nm)
        url='/search.html?q='+urllib.quote(restaurant_nm)
        try:
            path = 'yellowstone/%d.jpg'%restaurant_id
        except:
            path = 'no'
        return '<a href="%s"><img class="img-polaroid" src="%s"></a>' % (url,url_for('static',filename = path))

    def format_quotes(Top_quotes):
    # top_quotes are list of dict. The dict has five keys: 1 top_quote_text 2 top_quote_number 3 top_quote_word 4 top_word_classification 5 quote_url

        formatted_quotes=[]

        for quote in Top_quotes:
        # word=strip_unicode(quote['top_quote_word'])
            statis = 'in ' + str(quote['top_quote_number']) + ' reviews' 
        #a_text = (quote['top_quote_text']).replace(highlighted_word, '<a href = "%s"> %s</a>' %(quote['quote_url'], quote['top_quote_word']))
            quote_html = '<span style="font-size:24px">"%s"</span>&#8212; %s' % (quote['top_quote_text'], statis)   
            quote_html = quote_html.replace(quote['highlighted_word'], '<a href = "%s"> %s</a>' %(quote['quote_url'], quote['highlighted_word']))
          
            formatted_quotes.append(quote_html)
        return formatted_quotes

    
    thumbnail_url_html = get_thumbnail_url_html(restaurant_nm)
    raw_top_quotes = get.get_top_quotes(restaurant_id)
    top_quotes = format_quotes(raw_top_quotes)

    
    restaurant_nm = restaurant_nm.replace('_',' ')
    if restaurant_id is not None:
        return render_template('search.html', 
                top_quotes=top_quotes,
                restaurant_nm=restaurant_nm,
                restaurant_id=restaurant_id,
                total_num_reviews= total_num_reviews,
                restaurant_address = restaurant_address,
                restaurant_phone = restaurant_phone,
                thumbnail_url_html = thumbnail_url_html)

    else:
        return render_template('search.html', 
                restaurant_nm=restaurant_nm,
                restaurant_id=restaurant_id,
                restaurant_address = restaurant_addess, 
                restaurant_phone = restaurant_phone
                ) 
    
 
@application.route('/NationalParks.html')
def national_parks():
    return render_template('NationalParks.html')

 

@application.route('/about.html')
def about():
    return render_template('about.html')




'''
if __name__ == '__main__':
    application.run(host= '0.0.0.0',port = 5000, debug = True) 

'''
 


if __name__ == '__main__':
    application.debug= False
    application.run(host = '0.0.0.0') 





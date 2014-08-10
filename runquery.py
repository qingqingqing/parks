# 12:27 pm of 6/12/14
# put data (get_geo_info) into db

import MySQLdb
import dbutil
# import get_geo_info
#import scrapeD
import os
import sys
import nltk
import numpy
import restaurants
 
# cnx = MySQLdb.Connect(charset = 'utf8', user='root', passwd='1', db = 'trip_reviews',host='localhost')


'''
# 16:39 pm of 6/12 put geo of 84 attractions @ yellowstone into mysql
put = dbutil.DBPut(db_name = 'trip_reviews', db_url = '10.0.0.129', usr = 'root', pwd = '1')
yellowstone_url = 'http://www.tripadvisor.com/AllLocations-g60999-c2-Attractions-Yellowstone_National_Park_Wyoming.html'
attr_urls = get_geo_info.urls_attractions_one_city(yellowstone_url)
for t in attr_urls:
    geo = get_geo_info.get_geo_attraction(t)
    # print geo
    put.put_geo_attraction(geo)
'''
 


 




'''
## prepare to put attractions_city to mysql
# 84 attractions @ yellowstone
# 12:22 pm of 6/13/2014, done
put = dbutil.DBPut(db_name = 'trip_reviews', db_url = '10.0.0.129', usr = 'root', pwd = '1')
yellowstone_url = 'http://www.tripadvisor.com/AllLocations-g60999-c2-Attractions-Yellowstone_National_Park_Wyoming.html'
attrs_city = scrapeD.get_attr_info(yellowstone_url)
for t in range(len(attrs_city)):
    put.put_attractions_city(attrs_city[t])

'''


'''
## prepare to put reviews_attr to mysql，there are 7232 reviews, and 781 of them are non-english reviews/  review_body = 'NA'
put = dbutil.DBPut(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')
yellowstone_url = 'http://www.tripadvisor.com/AllLocations-g60999-c2-Attractions-Yellowstone_National_Park_Wyoming.html'
urls_attr = scrapeD.urls_attractions_one_city(yellowstone_url)
    
for j in range(5, len(urls_attr)):
    reviews_temp = scrapeD.reviews_from_one_attr(urls_attr[j])
    for i in range(len(reviews_temp)):
        put.put_reviews_attraction(reviews_temp[i])
        print i, j
'''   





'''
# 6/21/2014
# prepre to put restaurant info in a park to mysql
put = dbutil.DBPut(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')
 

url_restaurants_1stpg = 'http://www.tripadvisor.com/Restaurants-g60999-Yellowstone_National_Park_Wyoming.html'
restaurants_url = restaurants.urls_all_restaurants_park(url_restaurants_1stpg)
 

for i in range(22,len(restaurants_url)):
    restaurant_info = restaurants.summary_restaurant(restaurants_url[16])
    put.put_restaurants_park(restaurant_info)
    print i
'''


'''
## 6/21/2014
## prepare to put reviews on restaurants to mysql 
put = dbutil.DBPut(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')
url = 'http://www.tripadvisor.com/Restaurants-g60999-Yellowstone_National_Park_Wyoming.html'
urls_restaurants = restaurants.urls_all_restaurants_park(url)
#print urls_restaurants[0]


 

for i in range(len(urls_restaurants)):
    reviews_temp = restaurants.reviews_from_one_restaurant(urls_restaurants[i])
    print len(reviews_temp)
    for j in range(len(reviews_temp)):
        put.put_reviews_restaurant(reviews_temp[j])
        print j,i
'''        
 


 
'''
#given review_id, has to know review_url
# review_id----restaurant_id (reviews_restaurant)-----restaurant_nm (table restaurants_park & get_restaurants_park)
put = dbutil.DBPut(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')
get = dbutil.DBGet(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')
 
review_id = 210957847
restaurant_id = get.reviewid_restaurantID(review_id)
restaurant_id = [int(t) for t in restaurant_id][0]
restaurant_nm = (get.restaurant_id_nm(restaurant_id))[0]

review_url = 'http://www.tripadvisor.com/ShowUserReviews-g60999-d'+str(restaurant_id)+'-r'+str(review_id)+'-'+restaurant_nm+'-Yellowstone_National_Park_Wyoming.html'
print review_url

reviews = get.get_review_id()
print reviews[0]
reviews_id = [int(t[0]) for t in reviews]
print type(reviews), len(reviews)
print reviews_id[:5]

 
 
for i in reviews_id:
    restaurant_id = get.reviewid_restaurantID(i)
    restaurant_id = [int(t) for t in restaurant_id][0]
    restaurant_nm = (get.restaurant_id_nm(restaurant_id))[0]
    review_url = 'http://www.tripadvisor.com/ShowUserReviews-g60999-d'+str(restaurant_id)+'-r'+str(review_id)+'-'+restaurant_nm+'-Yellowstone_National_Park_Wyoming.html'
    put.put_review_url({'review_id':i, 'review_url':review_url})
    print i
''' 


 









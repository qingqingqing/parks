# scrape pictures of all restaurants
import urllib2
import bs4
from bs4 import BeautifulSoup
import boto
import urllib
import os





def urls_all_restaurants_park(url_restaurant):
    # input: url of restaurants, 1st pg
    # output: urls of all restaurants in the park
    
    html = urllib2.urlopen(url_restaurant)
    soup = BeautifulSoup(html)
    nodes = soup.find_all('a', href = True, onclick = True, dir = True)
    urls_all_restaurants = ['http://www.tripadvisor.com'+ t.get('href') for t in nodes]
    return urls_all_restaurants





def grab_img_restaurants_park(url_restaurants_pg):
    # input 1st pg of all restaurants in a park
    # output one img for every restaurant in a park
    urls = urls_all_restaurants_park(url_restaurants_pg)
    srcs = [grab_img_one_restaurant(t) for t in urls]
    return srcs



def grab_img_one_restaurant(url_restaurant):
    #insert url of restuarnt, for example, 'http://www.tripadvisor.com/Restaurant_Review-g60999-d517927-Reviews-Roosevelt_Lodge-Yellowstone_National_Park_Wyoming.html'
    #output images and their links
    # note there are four images on the page of every restaurant
    
    url_split = url_restaurant.split('-')
    restaurant_id_part = (url_split[2]).encode('utf8') 
    restaurant_id = int(restaurant_id_part.replace('d',''))
    restaurant_nm = (url_split[4]).encode('utf8')
    
    html = urllib2.urlopen(url_restaurant)
    soup = BeautifulSoup(html)
    try:
        node = soup.find('div',{'class':'photo'})
        node_1 = node.find('a')
        link = 'http://www.tripadvisor.com'+ node_1.get('href')

    #find other imgs 
    #nodes = soup.find_all('div',{'class':'photo thumb'})
    #links = ['http://www.tripadvisor.com'+t.get('href') for t in nodes]

        flink = link
        content = urllib2.urlopen(link)
        soup1 = BeautifulSoup(content)
        try:
            img_node = soup1.find('img', {'class':'taLnk big_photo'})
            src = img_node.get('src')
        except AttributeError:
            img_node = soup1.find('img', {'class':'big_photo'})
            src = img_node.get('src')
    except AttributeError:
        src = 'na'
    
    return {'restaurant_id':restaurant_id,'restaurant_nm':restaurant_nm,'img_url':src}



 
def imgUlr_local(url_restaurants_pg):
    # url_restaurants_pg = 'http://www.tripadvisor.com/Restaurants-g60999-Yellowstone_National_Park_Wyoming.html'
    all_img = grab_img_restaurants_park(url_restaurants_pg)
    location = os.path.abspath('C:/Users/inception/Desktop/yellowstone/')
    for t in all_img:
        if t['img_url'] is not 'na':
            thisistest = os.path.join(location, str(t['restaurant_id'])+'.jpg')
            urllib.urlretrieve(t['img_url'], thisistest)
    return True

 

 

 

 
def get_thumbnail_url_html(restaurant_nm):
    # return a new webpage including 1 top_quotes and 2 picture 3 url 4 address 5 phone of this restaurant
    # assume pictures are stored in s3 bucket
    restaurant_id = dbutl.restaurant_nm_id(restaurant_nm)
    url='/search.html?q='+urllib.quote(restaurant_nm)
    path='https://s3.amazonaws.com/parks.com/imgs/%d.jpg' % restaurant_id
    
    return '<a href="%s"><img class="img-polaroid" src="%s"></a>' % (url,path)







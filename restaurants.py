 
 

# find out # of restaurants, # of reviews on restaurants
# find out # of attractions, # of reviews on attractions


import bs4
from bs4 import BeautifulSoup
import urllib2

 

# restaurants
def get_restaurants_park(park_url):
    # insert url of national park
    # output summary of restaurants of national park: url of restaurant, 2) # of restaurants 3) # of reviews on restaurants
    html = urllib2.urlopen(park_url)
    soup = BeautifulSoup(html)
    
    try:
        restaurant_node = soup.find('li',{'class':'restaurants twoLines'})
        node1 = restaurant_node.find('a')
        node3 = restaurant_node.find('span',{'class':'typeQty'})
        node2 = restaurant_node.find('span', {'class':'contentCount'})

        restaurants_url = 'http://www.tripadvisor.com'+ node1.get('href')

        num_reviews_restaurants = node2.text
        num_reviews_restaurants = int(((num_reviews_restaurants.split())[0]).replace(',',''))

        num_restaurants = node3.text
        num_restaurants = num_restaurants.replace('(','')
        num_restaurants = num_restaurants.replace(')','')
        num_restaurants = int(num_restaurants)

    except:
        restaurants_url = 'na'
        num_restaurants = 0
        num_reviews_restaurants = 0
        urls_all_restaurants = ['na']

    summary_restaurants_park = {}
    summary_restaurants_park['restaurants_url'] = restaurants_url
    summary_restaurants_park['num_restaurants'] = num_restaurants
    summary_restaurants_park['num_reviews_restaurants'] = num_reviews_restaurants
    #summary_restaurants_park['urls_all_restaurants'] = urls_all_restaurants 
    return summary_restaurants_park

 
 






def get_attractions_park(park_url):
    #input url of park
    #output summary of attractions in a national park: # of attractions 2) url of attractions 3) # of reviews on attractions
    html = urllib2.urlopen(park_url)
    soup = BeautifulSoup(html)
    
    try:
        attractions_node = soup.find('li',{'class':'attractions twoLines'})
        node1 = attractions_node.find('a')
        node3 = attractions_node.find('span',{'class':'typeQty'})
        node2 = attractions_node.find('span', {'class':'contentCount'})
        attractions_url = 'www.tripadvisor.com'+ node1.get('href')

        num_reviews_attractions = node2.text
        num_reviews_attractions = int((num_reviews_attractions.split())[0])

        num_attractions = node3.text
        num_attractions = num_attractions.replace('(','')
        num_attractions = num_attractions.replace(')','')
        num_attractions = int(num_attractions)
    except:
        attractions_url = 'na'
        num_attractions = 0
        num_reviews_attractions = 0

    summary_attractions_park = {}
    summary_attractions_park['attractions_url'] = attractions_url
    summary_attractions_park['num_attractions'] = num_attractions
    summary_attractions_park['num_reviews_attractions'] = num_reviews_attractions
    return summary_attractions_park


 



def summary_restaurant(url):
    # from url of one restaurant
    # output restaurant information: id, nm, rank, rate, address, phone, parkid, urls_allreviews
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html)
    
     
    node2 = soup.find('span',{'property':'v:count'})
    node4 = soup.find('img',{'property':'v:average'})
    node3 = soup.find_all('div', {'class':'detail'})
    node5 = soup.find('a', href = True, onclick = True, id = True)
    node8 = soup.find_all('a', href = True, onclick = True, id = True)

    try:
        node1 = soup.find('b',{'class':'rank_text'})
        restaurant_rank = int((((node1.text).split())[-1]).replace('#',''))
        num_reviews_restaurant = int(node2.text)
        restaurant_rate = float(node4['content'])
        review_1st_url_restaurant = 'www.tripadvisor.com'+ node5.get('href')

        reviews_10urls_pg = [url]+['-'.join((url.split('-'))[:3])+'-or'+ str(10*i) +'-'+ '-'.join((url.split('-'))[-2:]) for i in range(1, 1+ int(num_reviews_restaurant/10))]
 
        reviews_urls = []
        for i in reviews_10urls_pg:
            html = urllib2.urlopen(i)
            soup = BeautifulSoup(html)

            review_id_nodes = soup.find_all('div',{'class':'reviewSelector'})
            review_id_part = [t['id'] for t in review_id_nodes]
            review_id_part_split = [t.split('_') for t in review_id_part]
            review_id = [t[-1] for t in review_id_part_split]
            i_split = i.split('-')
            i_split[0] = (i_split[0]).replace('Restaurant_Review','ShowUserReviews')
            reviews_urls = reviews_urls + [i_split[0]+'-'+i_split[1]+'-'+i_split[2]+'-r'+t+'-'+i_split[-2]+'-'+i_split[-1] for t in review_id]

    except:
        restaurant_rank = 0
        num_reviews_restaurant = 0
        restaurant_rate = 0.0
        review_1st_url_restaurant = 'na'
        reviews_urls = []
        
    #restaurant_type = [t.text for t in node3]
     
    restaurant_nm = (url.split('-'))[-2]
    restaurant_id = int(((url.split('-'))[2]).replace('d',''))
    restaurant_parkid = int(((url.split('-'))[1]).replace('g',''))

    try:
        node6 = soup.find('div', {'class':'fl phoneNumber'})
        restaurant_phone = (node6.text).encode('utf8')
    except:
        restaurant_phone = 'na'

    try:
        node7 = soup.find('div',{'class':'addr'})
        restaurant_address = ((node7.text).encode('utf8')).replace('\n','')
    except:
        node9 = soup.find('span',{'class':'format_address'})
        restaurant_address = ((node9.text).encode('utf8')).replace('\n','')
        
     
    
     
    summary_one_restaurant = {}
    summary_one_restaurant['restaurant_id']= restaurant_id
    summary_one_restaurant['restaurant_nm']= restaurant_nm
    summary_one_restaurant['restaurant_rank']= restaurant_rank
    summary_one_restaurant['restaurant_rate']= restaurant_rate
    summary_one_restaurant['restaurant_numberReviews']= num_reviews_restaurant
    summary_one_restaurant['restaurant_phone']= restaurant_phone
    summary_one_restaurant['restaurant_address']= restaurant_address
    summary_one_restaurant['restaurant_parkID']= restaurant_parkid
    summary_one_restaurant['reviews_url']= reviews_urls
    return summary_one_restaurant


 




def urls_all_restaurants_park(url_restaurant):
    # input: url of restaurants, 1st pg
    # output: urls of all restaurants in the park
    
    html = urllib2.urlopen(url_restaurant)
    soup = BeautifulSoup(html)
    nodes = soup.find_all('a', href = True, onclick = True, dir = True)
    urls_all_restaurants = ['http://www.tripadvisor.com'+ t.get('href') for t in nodes]
    return urls_all_restaurants


def review_info_from_url_review(url):
    # output review as a dict: reivew_id, review_title, review_body, review_rate, review_restaurantID
    # input is url of one review: g*+d*+r*
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html)
      
    review_info = {'review_body':'','review_title':'', 'review_id':'', 'review_restaurantID':'', 'review_rate':''}

    url_review_split = url.split('-')
    review_attID_part = url_review_split[2]
    review_attrID = review_attID_part.replace('d','')
    review_info['review_restaurantID'] = int(review_attrID.encode('utf8'))
    
    review_id_part = url_review_split[3]
    review_id = review_id_part.replace('r','')
    review_info['review_id'] = int(review_id.encode('utf8'))

    title_node = soup.find('title')
    review_info['review_title'] = ((((title_node.text).encode('utf8')).split('-'))[0]).strip()
   
    #rate_node = soup.find_all('img',{'class':'sprite-rating_no_fill rating_no_fill no50'})
    #review_info['review_rate'] = float((rate_node[0]['alt']).encode('utf8'))
    try:
        rate_node = soup.find('img',{'property': 'v:rating'})
        review_rate = float(rate_node['content'])
        review_info['review_rate'] = review_rate
    except:
        review_info['review_rate'] = 0
        
    try:
        review_node = soup.find('p',id = True, property = True)
        review_info['review_body'] = (review_node.text).encode('utf8')    
    except AttributeError:
        review_info['review_body'] = 'NA' 
    return review_info

 


 

def reviews_from_one_restaurant(url):
    # step 1: url of restaurant
    # step 2: [get_infor(t) for t in urls_reviews], get_info(t) is a {'review_id':,'review_title':,'review_body':,'review_rate':,'review_restaurantID':}
    
    reviews_urls_restaurant = (summary_restaurant(url))['reviews_url']
    reviews_restaurant = [review_info_from_url_review(t) for t in reviews_urls_restaurant]
    return reviews_restaurant
 

 


#print reviews_from_one_restaurant('http://www.tripadvisor.com/Restaurant_Review-g60999-d517927-Reviews-Roosevelt_Lodge-Yellowstone_National_Park_Wyoming.html')
#reviews_urls_restaurant = (summary_restaurant('http://www.tripadvisor.com/Restaurant_Review-g60999-d517927-Reviews-Roosevelt_Lodge-Yellowstone_National_Park_Wyoming.html'))['reviews_url']
#print len(reviews_urls_restaurant) 
#url = 'http://www.tripadvisor.com/Restaurants-g60999-Yellowstone_National_Park_Wyoming.html'
#urls_restaurants = urls_all_restaurants_park(url)
#print len(urls_restaurants)

'''




def reviews_all_restaurants_one_park(url_park):
    # insert url of one national park
    # output all reviews of all restaurants

    # step 1 : from url_park---get url of restaurants 1st pg---with function (get_restaurants_park(park_url))['restaurants_url']
    # step 2:  from url of restaurants 1st pg ---get urls of all restaurants---with function urls_all_restaurants_park(url_restaurant)
    # step 3:  from urls of all restaurants --- get reviews of all restaurants ---- with function reviews_from_one_restaurant(url)

    url_restaurants_pg = (get_restaurants_park(url_park))['restaurants_url']
    urls_restaurants = urls_all_restaurants_park(url_restaurants_pg)
    reviews_all_restaurants_park = [reviews_from_one_restaurant(t) for t in urls_restaurants]
    return reviews_all_restaurants_park



url_park = 'http://www.tripadvisor.com/Tourism-g60999-Yellowstone_National_Park_Wyoming-Vacations.html'
a = reviews_all_restaurants_one_park(url_park)
print len(a)

'''


 
 

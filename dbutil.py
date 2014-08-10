
# 1:25 pm of 06/04/2014
# today: I need to store data into mysql database

import MySQLdb
import _mysql


 
## cnx = MySQLdb.Connect(charset = 'utf8', user='root', passwd='1', db = 'trip_reviews',host='10.0.0.129')
 
 



class DBAccess():
    # Access database
    def __init__(self, db_name, db_url, usr, pwd):
        self.db_name = db_name
        self.db_url = db_url
        self.usr = usr
        self.pwd = pwd

    def conncect(self):
        cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
        return cnx
        # db_name(database), usr(user), db_url(host), pwd(password): variables to store parameter for db_connection

  

    def close(self):
        self.cnx.cursor().close()
        self.cnx.close()

   

class DBPut(DBAccess):

    def __init__(self, db_name, db_url, usr, pwd):
        #usr = os.environ['usr_write']
        # pwd = os.environ['pwd_write']
        DBAccess.__init__(self, db_name, db_url, usr, pwd)
        ## super(): find the parent class of DBPut (which is DBAccess), and transform self_DBPut to self_DBAccess



    def put_geo_attraction(self, geo):
       #
       cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
       query = '''INSERT INTO geo_attraction (attr_id, attr_lat, attr_lng) VALUES (%s, %s, %s)'''
       params = (geo['attr_id'], geo['attr_lat'], geo['attr_lng'])
       cnx.cursor().execute(query, params)
       cnx.commit()
       cnx.cursor().close()
       cnx.close()
       return True


    def put_top_quotes(self, topQuoRestau):
       #
       cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
       query = '''INSERT INTO topq(restaurant_id, top_quote_text, top_quote_number, top_quote_word, top_word_classification,
                                                quote_url, highlighted_word) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
       params = (topQuoRestau['restaurant_id'],
                 topQuoRestau['top_quote_text'],
                 topQuoRestau['top_quote_number'],
                 topQuoRestau['top_quote_word'],
                 topQuoRestau['top_word_classification'],
                 topQuoRestau['quote_url'],
                 topQuoRestau['highlighted_word'])
       cnx.cursor().execute(query, params)
       cnx.commit()
       cnx.cursor().close()
       cnx.close()
       return True
    



    def put_attractions_city(self, attraction_city): 
       # attraction+city should be a dictionary
       cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
       query = ('''INSERT INTO attr_city (attr_id, attr_name, attr_rank, attr_cityID)
                   VALUES (%s, %s, %s, %s)
                    ''' )
       params = (attraction_city['attr_id'], attraction_city['attr_name'],attraction_city['attr_rank'], attraction_city['attr_cityID'])
       cnx.cursor().execute(query, params)

       cnx.commit()
       cnx.cursor().close()
       cnx.close()
       return True

 



    def put_restaurants_park(self, restaurants): 
       # 
       cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
       query = ('''INSERT INTO restaurants_park (restaurant_id, restaurant_nm, restaurant_rank, restaurant_rate, restaurant_numberReviews,restaurant_phone, restaurant_address, restaurant_parkID)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ''' )
       params = (restaurants['restaurant_id'], restaurants['restaurant_nm'], restaurants['restaurant_rank'], restaurants['restaurant_rate'], restaurants['restaurant_numberReviews'], restaurants['restaurant_phone'], restaurants['restaurant_address'], restaurants['restaurant_parkID'])
       
       
       cnx.cursor().execute(query, params)
       cnx.commit()
       cnx.cursor().close()
       cnx.close()
       return True
   
   
    
    def put_review_id_url(self, reviews_url): 
       # 
       cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
       query = ('''INSERT INTO review_id_url(review_id, review_url)
                   VALUES (%s, %s)
                    ''' )
       params = (reviews_url['review_id'], reviews_url['review_url'])
       
       cnx.cursor().execute(query, params)
       cnx.commit()
       cnx.cursor().close()
       cnx.close()
       return True

    def put_review_url(self, reviews_url): 
       # 
       cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
       query = ('''insert into review_id_url
                    values (%s, %s)  
                    ''' )
       params = (reviews_url['review_id'], reviews_url['review_url'])
       
       cnx.cursor().execute(query, params)
       cnx.commit()
       cnx.cursor().close()
       cnx.close()
       return True


    def put_reviews_attraction(self, review):
        
       # review_attraction should be a dictionary too
       cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
       query = ('''INSERT INTO reviews_attraction (review_id, review_title, review_body, review_attrID)
                   VALUES (%s, %s, %s, %s)''')
       params = (review['review_id'],review['review_title'], review['review_body'], review['review_attrID'])
       cnx.cursor().execute(query, params)
       cnx.commit()
       cnx.cursor().close()
       cnx.close()
       return True

    def put_reviews_restaurant(self, reviews_restaurant):
        # review_restaurant should be a dictionary
       cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
       query = ('''INSERT INTO reviews_restaurant (review_id, review_title, review_body, review_rate, review_restaurantID)
                   VALUES (%s, %s,%s, %s, %s)''')
       params = (reviews_restaurant['review_id'],reviews_restaurant['review_title'], reviews_restaurant['review_body'] , reviews_restaurant['review_rate'], reviews_restaurant['review_restaurantID'])
       cnx.cursor().execute(query, params)
       cnx.commit()
       cnx.cursor().close()
    
       cnx.close()
       return True

 


 



    def remove_attractions_city(self, attraction_id):
        ## delete all information of an attraction the in table 'attra_city' and 'reviews_attr', given attraction_id
        '''remove all data of one attraction'''
        query = ('''DELETE FROM attractions_city WHERE attr_id = %s''' (attraction_id))
        params = attraction_id
        self.cursor.execute(query, params)
        self.cnx.commit()
        return True



    def remove_geo_attraction(self, attraction_id):
        query = '''DELETE FROM geo_attraction WHERE attr_id = %S attraction_id'''
        params = attraction_id
        self.cursor.execute(query, params)
        self.cnx.commit()
        return True





class DBGet(DBAccess):

    def _init_(self):
        usr = 'root'
        super(DBGet, self)._init_('yellowstone',usr)


    def get_attractions_city(self, cityID):
        # get all attractions from a city
        cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
        query = ('''
               SELECT attr_id, attr_name, attr_rank, attr_type, attr_NumReviews
               FROM attr_city
               WHERE attr_cityID = %s
               ''')
        cur = cnx.cursor()
        cur.execute(query, cityID)
        attractions = [t for t in cur.fetchall()]
        return attractions




    def get_restaurants_park(self, park_id):
        # get all restaurants information from a park
        cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
        query = ('''
               SELECT restaurant_id, restaurant_nm, restaurant_rank, restaurant_rate, restaurant_numberReviews,restaurant_phone, restaurant_address, restaurant_parkID
               FROM restaurants_park
               WHERE restaurant_parkID = %s
               ''')
        cur = cnx.cursor()
        cur.execute(query,park_id)
        restaurants = [t for t in cur.fetchall()]
        return restaurants


    def restaurant_nm_id(self, restaurant_nm):
        # insert name of a restaurant; output id of restaurant
        cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
        query = ('''
                 SELECT restaurant_id
                 FROM restaurants_park
                 WHERE restaurant_nm = %s
                 ''')
        cur = cnx.cursor()
        cur.execute(query, restaurant_nm)
        restaurant_id = cur.fetchone()
        restaurant_id = [int(t) for t in restaurant_id][0]
        return restaurant_id


    def restaurant_id_nm(self, restaurant_id):
        # insert name of a restaurant; output id of restaurant
        cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
        query = ('''
                 SELECT restaurant_nm
                 FROM restaurants_park
                 WHERE restaurant_id = %s
                 ''')
        cur = cnx.cursor()
        cur.execute(query, restaurant_id)
        restaurant_nm = cur.fetchone()
        return restaurant_nm
    
    
    def restaurant_id_address(self, restaurant_id):
        # insert restaurant_id, output restaurant_address
        cnx = MySQLdb.Connect(user= self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8' )
        query = ('''
                 SELECT restaurant_address 
                 FROM restaurants_park
                 WHERE restaurant_id = %s
        ''')
        cur = cnx.cursor()
        cur.execute(query, restaurant_id)
        restaurant_address = cur.fetchone()
        restaurant_address = [t.encode('utf8') for t in restaurant_address][0]
        return restaurant_address
    
    
    def restaurant_num_reviews(self, restaurant_id):
        # insert restaurant_id, output restaurant_address
        cnx = MySQLdb.Connect(user= self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8' )
        query = ('''
                 SELECT restaurant_numberReviews 
                 FROM restaurants_park
                 WHERE restaurant_id = %s
        ''')
        cur = cnx.cursor()
        cur.execute(query, restaurant_id)
        Restaurant_numberReviews = cur.fetchone()
        restaurant_numberReviews = [int(t) for t in Restaurant_numberReviews][0]
        return restaurant_numberReviews
    

    def restaurant_id_phone(self, restaurant_id):
        # insert restaurant_id, output restaurant_address
        cnx = MySQLdb.Connect(user= self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8' )
        query = ('''
                 SELECT restaurant_phone 
                 FROM restaurants_park
                 WHERE restaurant_id = %s
        ''')
        cur = cnx.cursor()
        cur.execute(query, restaurant_id)
        restaurant_phone = cur.fetchone()
        restaurant_phone = [t.encode('utf8') for t in restaurant_phone][0]
        restaurant_phone = restaurant_phone.replace(' ','-')
        restaurant_phone = restaurant_phone.replace('/','-')
        return restaurant_phone
    
    
    
    def review_id_url(self, review_id):
        # insert restaurant_id, output restaurant_address
        cnx = MySQLdb.Connect(user= self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8' )
        query = ('''
                 SELECT review_url 
                 FROM review_id_url 
                 WHERE review_id = %s
        ''')
        cur = cnx.cursor()
        cur.execute(query, review_id)
        review_url = cur.fetchone()
        return review_url



    def get_review_id(self):
        cnx = MySQLdb.Connect(user= self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8' )
        query = ('''
                 SELECT distinct review_id 
                 FROM reviews_restaurant
        ''')
        cur = cnx.cursor()
        cur.execute(query)
        review_id = cur.fetchall()
        return review_id
    

    def reviewid_restaurantID(self, review_id):
        # insert restaurant_id, output restaurant_address
        cnx = MySQLdb.Connect(user= self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8' )
        query = ('''
                 SELECT review_restaurantID 
                 FROM reviews_restaurant
                 WHERE review_id = %s
        ''')
        cur = cnx.cursor()
        cur.execute(query, review_id)
        review_url = cur.fetchone()
        return review_url


    def get_reviews_attraction(self, attractionID):
        # get all reviews from an attraction
        cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
        query = ('''
            SELECT review_ID, review_title, review_body, review_attrID
            FROM reviews_attraction
            WHERE review_attrID = %s  
            ''')
        cur = cnx.cursor()
        cur.execute(query, attractionID)
        reviews = [t for t in cur.fetchall()]
        return reviews



    def get_reviews_restaurant(self, restaurantID):
        # get all reviews from an attraction
        cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
        query = ('''
            SELECT review_id, review_title, review_body, review_rate, review_restaurantID
            FROM reviews_restaurant
            WHERE review_restaurantID = %s  
            ''')
        cur = cnx.cursor()
        cur.execute(query, restaurantID)
        reviews = [t for t in cur.fetchall()]
        return reviews




    def get_top_quotes(self, restaurant_id):
        cnx = MySQLdb.Connect(user = self.usr, passwd = self.pwd, db = self.db_name, host = self.db_url, charset = 'utf8')
        query = ('''
            SELECT top_quote_text, top_quote_number, top_quote_word, highlighted_word, top_word_classification, quote_url
            FROM topq
            WHERE restaurant_id = %s  
            ''')
        cur = cnx.cursor()
        cur.execute(query, restaurant_id)
        quotes = [{'top_quote_text':t[0].encode('utf8'),'top_quote_number':int(t[1]),'top_quote_word':t[2].encode('utf8'),
                   'highlighted_word':t[3].encode('utf8'),'top_word_classification':t[4].encode('utf8'),'quote_url':t[5].encode('utf8')} for t in cur.fetchall()]
        return quotes

   
 



 
 


 






















    
    

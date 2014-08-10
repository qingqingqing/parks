import dbutil

import nltk
import string
import random
import math
import re
 
from nltk.corpus import stopwords
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk import stem
st = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()



parks_para = {
'DBNAME': 'trip',
'USER': 'qqq',
'PASSWORD': 'PLMqaz123',
'HOST': 'cq.crfuupun11nn.us-west-1.rds.amazonaws.com',
'PORT': 3306,
}




def get_reviews_restaurant(parkID):
    # get all reviews of all restaurants in a park from mysql
    # input parkID
    #get = dbutil.DBGet(db_name = parks_para['DBNAME'], db_url = parks_para['HOST'], usr = parks_para['USER'], pwd = parks_para['PASSWORD'])  
    get = dbutil.DBGet(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')
    restaurants_park = get.get_restaurants_park(parkID)
    restaurantsID = [t[0] for t in restaurants_park]
    
    reviews = []
    for i in restaurantsID:
        reviews = reviews + get.get_reviews_restaurant(i)  
        
    rs = []
    for i in range(len(reviews)):
        review_id_url = get.review_id_url(reviews[i][0])        
        rs.append({'review_id':reviews[i][0],
                   'review_title':(reviews[i][1]).encode('utf8'),
                   'review_body':((reviews[i][2]).encode('utf8')).replace('\n',''),
                   'review_rate':reviews[i][3],'review_restaurantID':reviews[i][4], 
                   'review_url':review_id_url})
    return rs
 


def split_data(rs, perc = 0.6):
    # split all reviews @ a park to trn and tst, trn is for _build_classifier(), tst is for get_top_quotes()
    size = len(rs)
    numb = int(math.floor(size*perc))
    pick = random.sample(range(size),numb)
    data_1 = [rs[t] for t in pick]
    data_2 = [rs[t] for t in range(size) if t not in pick]
    return data_1, data_2



def clean_text(raw_string):
    # insert string and output string by removing ['?<>:;!@#$%^&*,.], and removing stopwords
    stopwords = nltk.corpus.stopwords.words('english') +['na', 'NA']+ [t for t in string.punctuation]
    punc = [t for t in string.punctuation]
    #string = [string.replace('t',' ') for t in punc]
    r_string = re.findall(r'\w+', raw_string.lower())
    tokens = [t for t in r_string if t not in stopwords]
    clean_string = ' '.join(tokens)
    for i in range(len(punc)):
        clean_string = clean_string.replace(punc[i],'')
    return clean_string



def clean_tokens_from_string(raw_string):
    # remove #s
    # remove stopwords
    # remove punctuations
    # st.stem()
    # lower
    stopwords = nltk.corpus.stopwords.words('english') +['na', 'NA']
    tokens = re.findall(r'\w+',raw_string.lower())
    clean_tokens = [st.stem(t) for t in tokens if t not in stopwords]
    
    return clean_tokens

 

def _build_classifier(rs, n = 1000):
    # insert reviews as list of dictionaries, with two keys: 'review_rate', 'reivew_text'
    # insert n: it is the cutoff point, the frequency of words in trn set
    # output NB classifier
    # how to extract features and y to form the trn set?
    
    # use rate of every review to lable 'pos' or 'neg' as y (binary)
    good_rs = [rs[t] for t in range(len(rs)) if rs[t]['review_rate'] == 5]
    bad_rs  = [rs[t] for t in range(len(rs)) if rs[t]['review_rate'] < 3]

       # good/bad_reviews_text: rs['review_body'] & rs['review_title']
       # good/bad_reviews_lable: good/bad
    good_reviews_text = [t['review_title'] + t['review_body'] for t in good_rs]
    bad_reviews_text = [t['review_title']+t['review_body'] for t in bad_rs]

       # Clean_text(): is to remove stopwords; remove [!,:,',?,;].   insert string, output string
    good_reviews_clean_text = [clean_text(t) for t in good_reviews_text]
    bad_reviews_clean_text = [clean_text(t) for t in bad_reviews_text]

       # take the most common/frequent words as features, 0/1
    good_reviews_split = [nltk.word_tokenize(t) for t in good_reviews_clean_text]
    bad_reviews_split = [nltk.word_tokenize(t) for t in bad_reviews_clean_text]
       # flatter list of lists
    words_good_reviews = [w for t in good_reviews_split for w in t]
    words_bad_reviews  = [w for t in bad_reviews_split for w in t]
    words_trn = words_good_reviews + words_bad_reviews
    
        # count words with list function list.count()
    frequent_words = [t for t in words_trn if words_trn.count(t) > n]
              # construct x made by features, i.e., the frequent words. for good_reviews_split[i], pick those only in frequent_words 
              # construct y 'pos'/'neg'
              # the way below is how to shuffle list of tuples
    #good_records = [([s for s in t if s in frequent_words],'pos') for t in good_reviews_split]
    #bad_records  = [([s for s in t if s in frequent_words],'neg') for t in bad_reviews_split]
    #trn = sorted(good_records + bad_records, key = lambda k:random.random())    
    # reason: do I need to x_trn should be as shape of array, m*n, m records and n features
    #x_trn = numpy.asarray([t[0] for t in trn]).reshape(len(trn), ?)
    #y_trn = numpy.asarray([t[1] for t in trn]).reshape(len(trn), 1)
    #clf = sklearn.naive_bayes.BernoulliNB()
    #clf.fit(x_trn, y_trn)
    #print 'Accuracy in trn set: %f' %clf.score(x_trn, y_trn)
    #print clf._show_informative_features()
    # the most informative_features are the features with the biggest odds ratio

    def get_hsT(list_tuples):
        # insert list of tuples, output hashtables
        # for example: insert [(['out','sky', 'hands','good']],'pos'),(['bad'],'neg')]
        #           ---output [({'out': True,'sky':True,'hands':True,'good':True,'bad':False},'pos'),({'out': False,'sky':False,'hands':False,'good':False,'bad':True},'neg')]
        whole_list = [s for t in list_tuples for s in t[0]]
        hsT = []
        for t in list_tuples:
            temp = {}
            for i in range(len(whole_list)):
                temp[whole_list[i]] = whole_list[i] in t[0]
            hsT.append((temp,t[1])) 
        return hsT
    
    good_records = [([s for s in t if s in frequent_words],'pos') for t in good_reviews_split]
    bad_records  = [([s for s in t if s in frequent_words],'neg') for t in bad_reviews_split]
    good_x = get_hsT(good_records)
    bad_x = get_hsT(bad_records)
    trn_set = good_x + bad_x
    random.shuffle(trn_set)
        # use nltk.NaiveBayesClassifier. Note that trn_set is list of tuples and x is hashtable, not a list
    clf = nltk.NaiveBayesClassifier.train(trn_set)
    #print 'Accuray', nltk.classify.accuracy(clf, trn_set)
    #clf.show_most_informative_features(20)

    #a = len(good_records)
    #b = len(bad_records)
    #c = len([t for t in good_records if 'delicious' in t[0]])
    #d = len([t for t in bad_records if 'delicious' in t[0]])
    #e = float(c)/a
    #f = float(d)/b
    #k = float(e)/f

    #cc = len([t for t in good_records if 'poor' in t[0]])
    #dd = len([t for t in bad_records if 'poor' in t[0]]) 
    #ee = float(cc)/a
    #ff = float(dd)/b
    #kk = float(ff)/float(ee)
    
    #print '# of good reviews:',a  
    #print '# of bad reviews',b  
    #print '# of good reviews containing delicious',c  
    #print '# of bad reviews containing delicious', d          
    #print 'odds ratio of delicious:', k
    #print 'odds ratio of poor:', kk
    #print float(kk)/k
    
    Inf_features = clf.most_informative_features
    
    return clf, Inf_features



 

def get_most_informative_features(classifier, n=10, column_prefix=''): 
    """ Classifier is of type nltk.classify.naivebayes.NaiveBayesClassifier
    """

    cpdist = classifier._feature_probdist
    results = []

    for i,(fname, fval) in enumerate(classifier.most_informative_features(n)):
        #print (fname, fval)
        
        def labelprob(l): 
            return cpdist[l,fname].prob(fval) 
        labels = sorted([l for l in classifier._labels 
                         if fval in cpdist[l,fname].samples()], 
                        key=labelprob) 
        if len(labels) == 1: continue 
        l0 = labels[0] 
        l1 = labels[-1] 
        if cpdist[l0,fname].prob(fval) == 0: 
            ratio = 'INF' 
        else: 
            ratio = '%8.1f' % (cpdist[l1,fname].prob(fval) / 
                              cpdist[l0,fname].prob(fval))

        results.append({'feature_name':fname,'classification':l1,'odds_ratio':ratio,'informative_ranking':i})
    
    return results



 

def short_quotes(review, n):
    # insert one review, n is the cutoff point, max length of short quotes
    # output short quotes in the review
    # tech: split the reviews to sentences---count the tokens of every sentence---pick short sentences---store in a list

    short_quotes = {}

    # there are two ways to split the review to sentences/quotes. The two ways have the same result.
    '''punkt_param = PunktParameters()
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    short_quotes = sentence_splitter.tokenize(review)'''
    quotes = (nltk.data.load('tokenizers/punkt/english.pickle')).tokenize(review)

    short_quotes_text = [t for t in quotes if len(nltk.word_tokenize(t)) < n]
    short_quotes_words = [nltk.word_tokenize(t) for t in short_quotes_text]

    short_quotes['short_quotes_text'] = short_quotes_text
    short_quotes['short_quotes_words'] = short_quotes_words
    return short_quotes





def _find_top_quotes(restaurantID, classifier, n = 5):
    # insert reviews of one restaurant, 2) n is the # of top quotes
    # output top_n_quotes for every restaurant(1 top_quotes 2 url 4 total # of similar quotes 3 informative words)

    # part 1: 
    # reviews is a list of dict, with keyes 1'review_body', 2 'review_rate' 3 'review_title', 4'review_id' 5 'review_restaurantID'
    # re-write reviews to rs, also list of dict, with two keys: review & short_quotes. Review itself is a dict, so is the short_quotes.
    # use all reviews of the restaurant as the entry of _find_top_quotes
    # question? our goal is to find the most important words for classifying 'good' or 'bad'. we do not need to predict. does this mean we do not need to apply this classifier on test set.
    #           does this mean we can use part of reviews for training the classfier, and use all the rest to _find_top_quotes()?

    all_data = get_reviews_restaurant('60999')
    reviews = [t for t in all_data if t['review_restaurantID'] in [restaurantID]]

    #print 'there are total reviews in db'
    #print len(all_data)
    
    #print 'there are %f reviews of this restaurant' %len(reviews)
    
    rs = []
    for i in range(len(reviews)):
        temp = reviews[i]['review_body'] + ' '+ reviews[i]['review_title']
        #clean_temp = clean_text(temp) 
        score = reviews[i]['review_rate']
        if score > 3: classification = 'pos'
        if score <3.5: classification = 'neg'
        
        rs.append({'review':{'raw': temp,
                             'clean_tokens': clean_tokens_from_string(temp),
                             'classification':classification},
                    'quotes': {'list_raw_quotes':(nltk.data.load('tokenizers/punkt/english.pickle')).tokenize(temp),
                               'list_list_quotes_tokens':[clean_tokens_from_string(t) for t in (nltk.data.load('tokenizers/punkt/english.pickle')).tokenize(temp)],
                               'url':reviews[i]['review_url']}}
                   )


    #print 'here is rs[0]'
    #print rs[0]
    #print
    #print 'length of rs[]'
    #print len(rs)
    #print 

    
    all_words_reviews = []
    for i in range(len(rs)):
        all_words_reviews.extend(rs[i]['review']['clean_tokens'])
    #print 'all_words_reviews'
    #print all_words_reviews



        
    
    # part 2: find the most important words in test set
    # find which quotes are top_quotes from short_quotes.
    #First of all, we need to find the informative words of the dataset. Note that: the informative words are from trn set. 
    # how to find important words in tst set? step1: use the most informative features from the classifier, i.e., from the trn.
    #                                         step2: find the total number of every informative feature in short_quotes in all reviews, as #_occurance
    #                                         step3: use #_occurance (frequency in tst set) * log(odd ratio) of every feature
    #                                         step4: use the results of step3 to sort, find the most important words/features in tst set
    # how to find important features? we use 1 word frequency together with 2 odds ratio
    # in this project, we do not care much about the accurary, but to find the most important features/words. in this situation, 1 word frequency together with 2 odds ratio is good way for feature selection.
    # in other situations, feature selelctions such as chi-test and so on are better ways.
    
    def get_important_words(rs, n):

        top_features = get_most_informative_features(classifier, n+40)
         
        occur = []
        for i in range(len(top_features)):
            word_nm = top_features[i]['feature_name']
            classification = top_features[i]['classification']
            odds_ratio = top_features[i]['odds_ratio'] 
 
             
            count_tst = all_words_reviews.count(st.stem(word_nm))
            if len(reviews) > 50:
                weighted_occu = float(count_tst) * math.log(float(odds_ratio))
            else:
                weighted_occu = count_tst

            occur.append({'word_nm':word_nm,'classification': classification,'weighted_occu': weighted_occu})

        top_words = sorted(occur, key = lambda x: x['weighted_occu'], reverse = True)        
        return top_words[:n]
    
    
    # part 3: 
    # based on top n(=5) informative words, find top_quotes,
    # tech: if top_words in review['short_qutoes']['short_quotes_words']
    # construct top quotes as list of dictionaries
    top_words = get_important_words(rs, n)

    #print 
    #print 'top words'
    #print top_words
    
    top_quotes = []
    for i in range(n):
        top_quotes_word = top_words[i]['word_nm']
        top_word_classification = top_words[i]['classification']
         
        #why do we need to compare 'word_classification' == 'review_classification'? because for example, if a review has words 'not good' and the top word is 'good', then we do not count this review.
        # why do we need to compare st.stem(t) because if the word is 'greatest' and words such as 'great' or 'greater' count too.
        top_quotes_number = 0
        for i in range(len(rs)):
            if top_word_classification == rs[i]['review']['classification']:
                if st.stem(top_quotes_word) in rs[i]['review']['clean_tokens']:
                    top_quotes_number +=1
        
        quotes_list = []
        for i in range(len(rs)):
            for j in range(len(rs[i]['quotes']['list_raw_quotes'])):
                if st.stem(top_quotes_word) in rs[i]['quotes']['list_list_quotes_tokens'][j]:
                    if rs[i]['review']['classification'] is top_word_classification:
                        quotes_list.append([rs[i]['quotes']['url'], 
                                            rs[i]['quotes']['list_raw_quotes'][j], 
                                            len(re.findall(r'\w+', rs[i]['quotes']['list_raw_quotes'][j])),
                                           rs[i]['quotes']['list_list_quotes_tokens'][j]])

        #print quotes_list
     
        sort_quotes_list = sorted(quotes_list, key= lambda x: x[2])
        print sort_quotes_list
        
        if len(sort_quotes_list)>4:
            top_quotes_text= sort_quotes_list[4][1]
            Top_quotes_url = sort_quotes_list[4][0]
            # print type(Top_quotes_url): tuple. (
            # u'http://www.tripadvisor.com/ShowUserReviews-g60999-d3337448-r210957847-Grant_Village_Lakehouse_Restaurant-Yellowstone_National_Park_Wyoming.html',)
            # print Top_quotes_url
            top_quotes_url = (Top_quotes_url[0]).encode('utf8')
             
            top_quotes_tokens = top_quotes_text.split()
            for i in range(len(top_quotes_tokens)):
                for k in string.punctuation:
                    temp = ((top_quotes_tokens[i]).replace(k,'')).lower() 
                    if temp == top_quotes_word:
                        Highlighted_word = top_quotes_tokens[i]
            
            top_quotes.append({'top_quote_text': top_quotes_text,
                           'top_quote_number':top_quotes_number,
                           'top_quote_word':top_quotes_word,
                           'highlighted_word': Highlighted_word,
                           'top_word_classification':top_word_classification,
                           'quote_url': top_quotes_url})
        elif len(sort_quotes_list) ==0:
            pass
        else:
            top_quotes_text= sort_quotes_list[-1][1]
            Top_quotes_url = sort_quotes_list[-1][0]
            top_quotes_url = (Top_quotes_url[0]).encode('utf8')
            
            top_quotes_tokens = top_quotes_text.split()
            for i in range(len(top_quotes_tokens)):
                for k in string.punctuation:
                    temp = ((top_quotes_tokens[i]).replace(k,'')).lower() 
                    if temp == top_quotes_word:
                        Highlighted_word = top_quotes_tokens[i]
                    
            top_quotes.append({'top_quote_text': top_quotes_text,
                           'top_quote_number':top_quotes_number,
                           'top_quote_word':top_quotes_word,
                           'highlighted_word':Highlighted_word,
                           'top_word_classification':top_word_classification,
                           'quote_url': top_quotes_url})
                                  
    return top_quotes





 
 
 





 

 
 # build a classifier---find the most informative features on tst
                  
 # 
 
#print rs[0]
#print 'short quotes of 1st review'
#print short_quotes(rs[0]['review_body'], 10)
#print data_2[0]
#print clf
#print
#print inforamtive_featu

#results = get_most_informative_features(clf)
#print
#print 'Here are the results'
#print results


'''
#rs = get_reviews_restaurant('60999')
#data_1, data_2 = split_data(rs, perc = 0.6)
#clf, inforamtive_featu= _build_classifier(data_1, 50)

get = dbutil.DBGet(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')
restaurants = get.get_restaurants_park('60999')
restaurantsIDs_park = [t[0] for t in restaurants]

for i in range(23):
    print _find_top_quotes(restaurantsIDs_park[i], clf, n = 5)
    print i
    print
    print





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
 

''' 
 




# put all top quotes into mysql, 8/5/2014, to increase the speed

  

def all_quotes_db(id):

    # get = dbutil.DBGet(db_name = parks_para['DBNAME'], db_url = parks_para['HOST'], usr = parks_para['USER'], pwd = parks_para['PASSWORD'])
    get = dbutil.DBGet(db_name = 'trip_reviews', db_url = 'localhost',usr = 'root',pwd = '1')
    put = dbutil.DBPut(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')

    # feature all reviews from table: rs include 1)review_id 2)review_title 3)review_body 4)review_rate 5) review_url
    rs = get_reviews_restaurant(id)
    data_1, data_2 = split_data(rs, perc = 0.6)
    clf, inforamtive_featu=_build_classifier(data_1, 50)

    # table of restaurants_park: id, nm, rank, rate, numberReviews, phone, address, parkID
    topQuoRestau = [] 
    restaurants_park = get.get_restaurants_park(id)
    #for i in restaurants_park:
    for restaurant_id in [1818651, 1524609, 1077889, 4985908, 6387346, 4929015, 3412330, 532458]:
        raw_top_quotes = _find_top_quotes(restaurant_id, clf, n = 5)
        for j in range(len(raw_top_quotes)):
            '''topQuoRestau.append({'restaurant_id':restaurant_id,
                                                'top_quote_text':raw_top_quotes[j]['top_quote_text'],
                                                'top_quote_number': raw_top_quotes[j]['top_quote_number'],
                                                'top_quote_word': raw_top_quotes[j]['top_quote_word'],
                                                'highlighted_word': raw_top_quotes[j]['highlighted_word'],
                                                'top_word_classification': raw_top_quotes[j]['top_word_classification'],
                                                'quote_url': raw_top_quotes[j]['quote_url']})'''
            a = {'restaurant_id':restaurant_id,
                 'top_quote_text':raw_top_quotes[j]['top_quote_text'],
                 'top_quote_number': raw_top_quotes[j]['top_quote_number'],
                 'top_quote_word': raw_top_quotes[j]['top_quote_word'],
                 'highlighted_word': raw_top_quotes[j]['highlighted_word'],
                 'top_word_classification': raw_top_quotes[j]['top_word_classification'],
                 'quote_url': raw_top_quotes[j]['quote_url']}
            put.put_top_quotes(a)
            print restaurant_id, j
    
    return topQuoRestau
 
 
 

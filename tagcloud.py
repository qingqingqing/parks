
# wordcloud on reviews @ one city covering all attractions
## tech to get (word, freq) of all reviews
## get all reviews at a city from mysql
## pre_process_text() returns [[word, word, ..., word],[],[],...,[]]
## return (word, freq) of the reviews


import sys
from os import path
import re
import nltk
from nltk.probability import FreqDist
import dbutil
import math
import time

import pytagcloud
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts


 



def get_reviews_city(cityID):
    # get all reviews at a city from mysql server
    
    get = dbutil.DBGet(db_name = 'trip_reviews', db_url = 'localhost', usr = 'root', pwd = '1')
    attractions = get.get_attractions_city(cityID)
    attractions_id = [t[0] for t in attractions]
    # notice that the table attraction_city is stored by list of tuples.

    reviews_records = []
    for attrID in attractions_id:
        reviews_records = reviews_records + get.get_reviews_attraction(attrID)
    reviews = [t[2] for t in reviews_records]

    return reviews





def pre_process_reviews(list_reviews):
    # 1 encode the text 2) remove numbers; remove \n, ; and etc 
    list_reviews = [(t.encode('utf8')).lower() for t in list_reviews]
    clean_text = [re.findall(r'[a-zA-Z]+', t) for t in list_reviews]

    stopwords = nltk.corpus.stopwords.words('english') + ['na']+['yellowstone']
    text = [[a for a in t if a not in stopwords] for t in clean_text]

    #st = nltk.PorterStemmer()
    #st_text = [[st.stem(a) for a in t] for t in text]    
    return text

 
def flat_list(st_text):
    voc = []
    for t in text:
        voc = voc + t
    return voc


def count_words(flat_text):
    # input reviews
    # return (word, count) with nltk.FreqDist

    words_count = nltk.probability.FreqDist(flat_text)
    words = [(key, words_count[key]) for key in words_count]
    # note that it returns a list of tuples, which is requred by module pytagcloud
    return words


cityID = '60999'
reviews_text = get_reviews_city(cityID)
text = pre_process_reviews(reviews_text)
flat_text0 = flat_list(text)

#tune nns to nn

kk = [('geysers','geyser'),('falls','fall'),('saw','see'),('seeing','see'),('seen','see'),('springs','spring'),('viewing','view'),('hiking','hike'),('looking','look')]
for t in flat_text0:
    for j in kk:
        if t ==j[0]:
            t.replace(j[0],j[1])
print  flat_text0       


words = count_words(flat_text0)
words_cut = [t for t in words if t[1] > 100]
print len(words_cut)
# set bar = 200, there are 240 tokens
 
words_cut_list = [t[0] for t in words_cut]
# pos is list of tuples
pos = nltk.pos_tag(words_cut_list)
 
 

words_cut_pos = []
for i in words_cut:
    for j in pos:
        if i[0]==j[0]:
            words_cut_pos.append((i, j[1]))
#(('early', 615),'RB')
 
tupe_K = set([t[1] for t in pos])
print tupe_K
# set(['MD', 'VB', 'VBG', 'RB', 'NN', 'VBD', 'RBR', 'JJS', 'JJR', 'CD', 'VBP', 'VBN', 'PRP', 'JJ', 'IN', 'VBZ', 'DT', 'PRP$', 'NNS'])
## adj: JJ, JJS, JJR
##verb: VB, VBG, VBN, VBZ, VBD, VBP
## nonn: NN, NNS
## MD ('would')
## RB ('never'), RBR ('better','less'),  CD ('one'),  PRP ('us', 'tour'),  IN ('though'), DT ('a')?
 
words_cut_noun = [t[0] for t in words_cut_pos if t[1] in ['NN','NNS']]
words_cut_adj = [t[0] for t in words_cut_pos if t[1] in ['JJ','JJS','JJR']]
words_cut_verb = [t[0] for t in words_cut_pos if t[1] in ['VB','VBG','VBD','VBZ','VBP','VBN']]
 
print len(words_cut_noun), len(words_cut_adj), len(words_cut_verb)

create_tag_image(make_tags(words_cut, maxsize = 200), 'yellowstone_all.png', size=(1300,1150), background=(0, 0, 0, 255),layout=3, fontname='Molengo', rectangular=True)


create_tag_image(make_tags(words_cut_noun, maxsize = 200), 'yellowstone_noun.png', size=(1300,1150), background=(0, 0, 0, 255),layout=3, fontname='Molengo', rectangular=True)

create_tag_image(make_tags(words_cut_verb, maxsize = 200), 'yellowstone_verb.png', size=(1300,1150), background=(0, 0, 0, 255),layout=3, fontname='Molengo', rectangular=True)

create_tag_image(make_tags(words_cut_adj, maxsize = 200), 'yellowstone_adj.png', size=(1300,1150), background=(0, 0, 0, 255),layout=3, fontname='Molengo', rectangular=True)


'''
#if more time, will consider bi-gram, t-gram
stopwords = nltk.corpus.stopwords.words('english')
#print stopwords
rs = []
flat_text_tokens = []
for i in reviews_Text:
    for t in ['\n','.','-',',','&','*','%','^','(','(','!','@','#','$','%']:
        i = i.replace(t,'')
        raw_tokens = re.findall(r'[a-zA-Z]+', i.lower())
        clean_text = ' '.join([t for t in raw_tokens if t not in stopwords])
        tokens = clean_text.split(' ')
        #bg = nltk.ngrams(tokens, 2)
        #b_tokens = [' '.join(list(t)) for t in bg]
        #tg = nltk.ngrams(tokens,3)
        #t_tokens = [' '.join(list(t)) for t in tg]
        #rs.append({'review_raw_text': i,'review_clean_text':clean_text,'review_tokens':tokens,'review_bg':b_tokens,'review_tg':t_tokens})
        rs.append({'review_raw_text': i,'review_clean_text':clean_text,'review_tokens':tokens})
        flat_text_tokens = flat_text_tokens + tokens


 
#print rs[0]['review_bg']
#tokens_c = nltk.probability.FreqDist(flat_text_tokens)
#print tokens_c[:5]
#create_tag_image(make_tags(ng_words, minsize = 100, maxsize = 4000), 'yellowstone_4.png', size=(1300,1150), background=(0, 0, 0, 255),layout=3, fontname='Molengo', rectangular=True)

'''


 



 

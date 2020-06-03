from model import collection_movie
import pandas as pd
# from model import collection_movie,collection_keyword
# jinja control .py
# jinja int형 str형으로 filter
def basename(text):
    return str(text)

def filter_content(text): # print(text) # {'title': {'26': '아이언맨', '27': '아이언맨 3', '85': '앤트맨...
    t = text.values() # print(t) # dict_values([{'26': '아이언맨', '27': '아이언맨 3', '85': '앤트맨...
    test = [list(i.values()) for i in list(t)] # print(test) # [['아이언맨', '아이언맨 3', '앤트맨과 와스프', '아이
    te = [i for i in test[0]]

    movie_ = []
    for index in te:
        find_movie = collection_movie.find_one({'movie_code':index},{'_id':0, 'set_keywords':0})
        try:
            movie_content = [
                find_movie['title']
                ,find_movie['img_src']
                ,find_movie['movie_code']
                ,find_movie['actor']
                ,find_movie['director']
                ,find_movie['story']
                ]
        except TypeError:
            pass
        movie_.append(movie_content)   
    return movie_
    

def movie_content(test):
    data = pd.DataFrame(test)
    movie_list = data.values.tolist()
    return movie_list

def round_filter_zero(text):
    return round(text)

def round_filter(text):
    return round(text,2)

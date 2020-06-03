from pandas import Series,DataFrame
import pandas as pd
import numpy as np
from scipy import sparse
from glob import glob
import json
from scipy.sparse import hstack
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings; warnings.filterwarnings('ignore')

import pymongo
from pymongo import MongoClient
from model import collection_keyword, collection_user
from bson import json_util
import io

doc_list = list(collection_keyword.find({},{'_id':0}))
j_dump = json.dumps(doc_list, default=json_util.default)
j_load = json.loads(j_dump)

movies_info_kw = pd.DataFrame(j_load)

def countv():
    count_vect_genre = CountVectorizer(min_df=3, ngram_range=(1,1))
    genres_mat = count_vect_genre.fit_transform(movies_info_kw['genres_vec'].apply(lambda x: np.str_(x)))
    
    count_vect_actor = CountVectorizer(min_df=3, ngram_range=(1,1))
    actor_mat = count_vect_actor.fit_transform(movies_info_kw['actor_vec'].apply(lambda x: np.str_(x)))
    
    count_vect_director = CountVectorizer(min_df=3, ngram_range=(1,2))
    director_mat= count_vect_director.fit_transform(movies_info_kw['director_vec'].apply(lambda x: np.str_(x)))
    
    count_vect_keyword = CountVectorizer(min_df=0, ngram_range=(1,2))
    set_keyword_mat= count_vect_keyword.fit_transform(movies_info_kw['set_keyword_vec'].apply(lambda x: np.str_(x)))
    
    sim_mat = hstack((actor_mat, genres_mat, director_mat, set_keyword_mat))
    vec_sim = cosine_similarity(sim_mat, sim_mat)
    vec_sim_sorted_ind = vec_sim.argsort()[:, ::-1]
    return vec_sim_sorted_ind

vec_sim_sorted_ind = countv()

def find_sim_movie(df, sorted_ind, title_name, top_n=10):
    
    # 검색문자열을 포함하는 title index 출력
    title_movie = df.loc[df['title_vec'].str.contains(title_name.replace(' ',''), na=False)]
    title_index = title_movie.index.values
    print(title_movie)

    # top_n의 2배에 해당하는 쟝르 유사성이 높은 index 추출 
    similar_indexes = sorted_ind[title_index, :(top_n*2)]
    similar_indexes = similar_indexes.reshape(-1)
    # 뽑힌 데이터 프레임에서 중복을 제거함 -> 중복 영화 추천을 막기 위해서
    movies_info_kw_set = movies_info_kw.iloc[similar_indexes].drop_duplicates()[:top_n]

    return movies_info_kw_set.sort_values('weighted_vote', ascending=False)

def input_movie(movie_name):
    similar_movies = find_sim_movie(movies_info_kw, vec_sim_sorted_ind, movie_name ,10)
    recom_movies = similar_movies[['movie_code','title','actor','mean_rating','director','genre', 'set_keywords', 'weighted_vote','story']]
    return recom_movies

# input_movie('아이언맨')

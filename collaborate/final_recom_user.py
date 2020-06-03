from pandas import Series, DataFrame
import pandas as pd
import numpy as np
# import requests
import json
import glob
# from bs4 import BeautifulSoup
import warnings; warnings.filterwarnings('ignore')
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from pandas.api.types import CategoricalDtype
from scipy.sparse import csr_matrix
from model import collection_user_info

final_user_data= pd.read_csv('./csv/users_super_final.csv')

with open('./collaborate/item_sim_df.pickle', 'rb') as f:
    item_sim_df = pickle.load(f)


def predict_rating(ratings_arr, item_sim_arr ):
    ratings_pred = ratings_arr.dot(item_sim_arr)/ np.array([np.abs(item_sim_arr).sum(axis=1)])
    return ratings_pred


def collab_recomm(user_id, top_n=10):
    user_scored = final_user_data.loc[final_user_data['user_id']==user_id, ['movie_code','score']]
    
    user_final= pd.Series(
                   index=item_sim_df.columns
                    ).fillna(user_scored.set_index('movie_code')['score']).fillna(0)
    predicted = pd.Series(
          predict_rating(user_final.values, item_sim_df.values)[0]
        , index=item_sim_df.columns
    )
    
    unseen_movie = [
        movie 
        for movie in user_final.index 
        if movie not in user_scored['movie_code']
    ]
    
    recomm_movies = predicted[unseen_movie].sort_values(ascending=False, axis=0)[:top_n]
    return recomm_movies


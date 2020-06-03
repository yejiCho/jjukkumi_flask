from flask import Blueprint, jsonify, session
from flask import request, render_template, redirect
from pymongo import MongoClient
from passlib.hash import sha256_crypt
from model import collection_user, collection_movie
from bson import json_util
import json, random
import numpy as np
import pandas as pd
import collaborate.final_recom_user as re_user

collaborate = Blueprint('coll', __name__, template_folder='templates')

# movie_total_count = collection_movie.count_documents({}) # 20228 영화갯수
movie_total_count = 20
random.seed=123

@collaborate.route('/recommand',methods=['GET'])
def coll():
    if request.method =='GET':
        userid = session.get('userid',None)
        if userid:
            recom_list = re_user.collab_recomm(userid).index.tolist()

            recom_movie_list = []

            for movie_code in recom_list:

                recom_movie = list(collection_movie.find({'movie_code':movie_code},{'_id':0}))
                
                recom_movie_list.append(recom_movie)

            return render_template('recom.html',movie_list=recom_movie_list)


@collaborate.route('/movie', methods=['GET','POST'])
def movie(charset='utf-8'):
    if request.method == 'GET':
        random_movie = []
        random_list = np.random.choice(range(1,movie_total_count+1),10,replace=False)
        for random_index in random_list.tolist():
            test1 = collection_movie.find({},
            {
                '_id':0
                ,'movie_code':random_index
                ,'title':random_index
                ,'img_src':random_index
                ,'genre':random_index
                ,'director':random_index
                ,'actor':random_index
                ,'mean_rating':random_index
                ,'story':random_index
                ,'prd_year':random_index
            })
            random_movie.append(test1[random_index])
        return render_template('movie.html', random_movie=random_movie)     
    else:
        userid = session.get('userid')
        data = request.form['rating']
        print(userid)
        print(data)
        return redirect('/coll/movie')
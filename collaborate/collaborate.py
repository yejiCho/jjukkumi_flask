from flask import Blueprint, jsonify, session
from flask import request, render_template, redirect
from pymongo import MongoClient
from passlib.hash import sha256_crypt
from model import collection_user, collection_movie,collection_user_info
from bson import json_util
import json, random
import numpy as np
import pandas as pd
import collaborate.final_recom_user as re_user
import json

collaborate = Blueprint('coll', __name__, template_folder='templates')

# movie_total_count = collection_movie.count_documents({}) # 20228 영화갯수
movie_total_count = 20228
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
    if request.method == 'GET': # 랜덤 영화 별점 매기기 페이지 보여줌
        userid = session.get('userid',None) # 사용자 이름 갖고오기
        
        if userid: # 유저가 있을 경우
            
            user_data = list(collection_user_info.find({'user_id':userid},{'_id':0})) # 해당유저의 정보를 갖고오자
            find_movie_json = json.dumps(user_data, default=json_util.default) #userid가 평가한 movie // string -> json
            find_movie = json.loads(find_movie_json) # unicode_error 변환 

            movie_code_list = []
            for mv_code in find_movie: #[{},{},{}]
                movie_code_list.append(int(mv_code['movie_code'])) # dict 안에서 key값이 movie_code인 value값을 찾아가지고, movie_code_list에 넣어줌
            
            # index_range : np.random.choice안에 iterable한 변수를 넣는데, 이제 시작값이 0부터가지고 range함수써서 1부터 시작하게 만듬
            # range함수는 마지막인덱스가 제외되니깐 +1해줌
            index_range = list(range(1,movie_total_count+1))

            # 평가한 영화가 존재할 경우
            if movie_code_list:
                for data in movie_code_list:
                    if data in index_range: # 범위안에 평가한 영화코드가 있을 경우
                        index_range.remove(data)  # 평가한 영화코드를 제거해줌
            # 평가한 영화가 없을 경우
            else:
                index_range = range(1,movie_total_count+1)

            random_movie = []
            random_list = np.random.choice(index_range,10,replace=False)
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

            return render_template('movie.html', random_movie=random_movie,userid=userid) 
        
        return render_template('movie.html')    # 유저가 없을 경우
    
    else:
        userid = session.get('userid',None)
        # data = request.form
        data = request.form['rating']
        info_data = data.split(',')
        print(userid)
        print(info_data[0])
        print(info_data[1])
        total = {
            'movie_code':info_data[0],
            'user_id' : userid,
            'score' : info_data[1]
        }

        collection_user_info.insert_one(total)
        
        return redirect('/coll/movie')
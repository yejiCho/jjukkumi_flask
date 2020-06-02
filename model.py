from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client['movie']
collection_user = db['users'] # 회원가입 table
collection_movie = db['movie_info'] # 영화정보 table
collection_user_info = db['user_info'] # 영화별 유저 리뷰 table
collection_keyword = db['movie_info_keyword'] # keyword
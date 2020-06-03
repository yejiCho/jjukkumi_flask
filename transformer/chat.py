from flask import Blueprint, render_template, jsonify, request, redirect, g
from bson import json_util
import json
from recom.content_recom import input_movie
from model import (
    collection_keyword,collection_movie
    ,collection_review,collection_user
    )
# 해지 추가
from recom.content_recom import input_movie

chat = Blueprint('chat', __name__, template_folder='templates')

json_test_content =""
@chat.route('/chat',methods=['GET','POST'])
def chat_sentence():
    if request.method == 'POST':
        global json_test_content
        data = request.get_json()
        movie_name = data.get('sentence')
        movie_code = input_movie(movie_name)
        json_test_code = movie_code.to_json()
        json_test_content = json.loads(json_test_code)
        return json_test_content # 덮어씀 json_movie_content

    elif request.method == 'GET':

        return render_template('chat.html',json=json_test_content) 
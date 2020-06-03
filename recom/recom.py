from flask import Blueprint, render_template, jsonify, request, redirect, session
from bson import json_util
import json
from recom.content_recom import input_movie
from model import (
    collection_keyword,collection_movie
    ,collection_user_info,collection_user
    )

recom = Blueprint('recom', __name__, template_folder='templates')
json_movie_content = ''


@recom.route('/test',methods=['GET','POST'])
def content():
    if request.method == 'POST':
        global json_movie_content
        data = request.get_json()
        movie_name = data.get('movie')
        movie_content = input_movie(movie_name)
        json_movie = movie_content.to_json()
        json_movie_content = json.loads(json_movie)
        return json_movie_content # 덮어씀 json_movie_content
    elif request.method == 'GET':

        userid = session.get('userid',None)

        if userid:

            return render_template('content.html',json=json_movie_content,userid=userid)

        else:
            return render_template('content.html')

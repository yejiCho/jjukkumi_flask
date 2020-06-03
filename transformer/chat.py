from flask import Blueprint, render_template, jsonify, request, redirect
from bson import json_util
import json
from recom.content_recom import input_movie
# from transformer.main import predict

chat = Blueprint('chat', __name__, template_folder='templates')

json_test_content =""
movie_name = ""
@chat.route('/chat',methods=['GET','POST'])
def chat_sentence():
    if request.method == 'POST':
        global json_test_content
        global movie_name
        data = request.get_json()
        # data = request.form
        print(data)
        movie_name = data.get('sentence')
        # print(movie_name)
        movie_code = input_movie(movie_name)
        json_test_code = movie_code.to_json()
        json_test_content = json.loads(json_test_code)
        return json_test_content # 덮어씀 json_movie_content

    elif request.method == 'GET':

        return render_template('chat_test.html',question=movie_name,answer=json_test_content)
 
from flask import Blueprint, render_template, jsonify, request, redirect
from bson import json_util
import json
from transformer.main import predict

chat = Blueprint('chat', __name__, template_folder='templates')

answer =""
question = ""
@chat.route('/chat',methods=['GET','POST'])
def chat_sentence():
    if request.method == 'POST':
        global answer
        global question
        data = request.get_json()
        question = data.get('sentence')
        answer = predict(question)
        return answer # 덮어씀 json_movie_content

    elif request.method == 'GET':

        return render_template('chat_test.html',question=question,answer=answer)
 
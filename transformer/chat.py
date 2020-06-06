from flask import Blueprint, render_template, jsonify, request, redirect,session
from bson import json_util
import json
from transformer.main import predict


chat = Blueprint('chat', __name__, template_folder='templates')


question = []
answer = []
@chat.route('/chat',methods=['GET','POST'])
def chat_sentence():
    if request.method == 'POST':
        global answer
        global question
        data = request.get_json()
        sentence = data.get('sentence')
        question.append(sentence)
        bot_answer = predict(sentence)
        answer.append(bot_answer)
        return answer # 덮어씀 json_movie_content

    elif request.method == 'GET':
        userid = session.get('userid',None)
        
        return render_template('transformer.html',question=question,answer=answer,zip=zip,userid=userid)
 
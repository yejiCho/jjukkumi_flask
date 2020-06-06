from flask import Blueprint, render_template, jsonify, request, session
from seq2seq.main import run

seq_chat = Blueprint('seq_chat',__name__,template_folder='templates')

question = []
answer = []
@seq_chat.route('/',methods=['GET','POST'])
def chat_sentence():
        
    if request.method == 'POST':
        global answer
        global question

        data = request.get_json()
        sentence = data.get('sentence')
        bot_answer = run(sentence)
        question.append(sentence)
        bot_answer = run(sentence)
        answer.append(bot_answer)

        answer_bot = {
            'answer' : bot_answer
        }

        return jsonify(answer_bot)
        
    
    elif request.method == 'GET':

        userid = session.get('userid',None)

        return render_template('seq2seq.html',question=question,answer=answer,zip=zip,userid=userid)
        
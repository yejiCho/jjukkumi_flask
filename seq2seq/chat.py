from flask import Blueprint, render_template, jsonify, request, session

seq_chat = Blueprint('seq_chat',__name__,template_folder='templates')

question = []
answer = []
@seq_chat.route('/',methods=['GET','POST'])
def chat_sentence():
    if request.method == 'POST':
        from seq2seq.main import run
        import seq2seq.main

        global answer
        global question
        data = request.get_json()
        sentence = data.get('sentence')
        print(type(sentence))
        question.append(sentence)
        print(question)
        # bot_answer = run('hi')
        bot_answer = run(sentence)
        print(type(bot_answer))

        answer.append(bot_answer)
        print(answer)
        return answer
    
    elif request.method == 'GET':

        userid = session.get('userid',None)

        return render_template('seq2seq.html',question=question,answer=answer,zip=zip,userid=userid)
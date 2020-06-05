# -- coding: utf-8 --
from flask import Flask, render_template, session, app
from flask import Blueprint, jsonify, request, redirect
from passlib.hash import sha256_crypt
from datetime import timedelta
from users.users import users, login
from model import collection_movie,collection_user
from control_jinja import basename, filter_content,movie_content, round_filter, round_filter_zero
from recom.recom import recom
from collaborate.collaborate import collaborate
from transformer.chat import chat

app = Flask(__name__)

app.register_blueprint(users, url_prefix='/user')
app.register_blueprint(recom, url_prefix='/recom')
app.register_blueprint(collaborate, url_prefix='/coll')
app.register_blueprint(chat, url_prefix='/chat')
app.jinja_env.globals.update(zip=zip)


app.add_template_filter(basename)
app.add_template_filter(filter_content)
app.add_template_filter(movie_content)
app.add_template_filter(round_filter)
app.add_template_filter(round_filter_zero)

app.config['SECRET_KEY'] = 'THIS_IS_SECRET_KEY'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


@app.route('/',methods=['GET'])
def home():
    userid = session.get('userid',None)
    if userid:
        return render_template('home.html',userid=userid)
    else:
        return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    if session.get('userid'):
        del session['userid']
        return redirect('/')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/content',methods=['GET','POST'])
def content():
    return render_template('content.html')
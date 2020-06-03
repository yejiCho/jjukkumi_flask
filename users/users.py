from flask import Blueprint
from flask import jsonify, session
from flask import request, render_template, redirect
from pymongo import MongoClient
from passlib.hash import sha256_crypt
from model import collection_user,collection_movie
from bson import json_util
import json, random

users = Blueprint('users',__name__, template_folder='templates')


# register 회원가입
@users.route('/regist', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        userid = data.get('userid')
        username = data.get('username')
        password = data.get('password')
        re_password = data.get('re_password')
        
        if not (userid and username and password and re_password):
            return jsonify({'error':'No args'}),400
        
        if password != re_password:
            return jsonify({'error':'wrong password'}),400

        password = sha256_crypt.encrypt(password)
        total = {
            'userid':userid,
            'username':username,
            'password':password
            }

        collection_user.insert_one(total)

        return jsonify(),201
        
    elif request.method == 'GET':

        doc_list = list(collection_user.find())

        return json.dumps(doc_list, default=json_util.default)

@users.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        userid = data.get('userid')
        password = data.get('password')
        coll = collection_user.find_one({'userid':userid},{'_id':0, 'username':0})
        if coll is None:
            return jsonify({'error':'no id'})
        else:
            hash_password = sha256_crypt.verify(password,coll['password'])
            if hash_password:
                session['userid'] = userid
                return jsonify()
            else:
                return jsonify({'error':'wrong password'}),201


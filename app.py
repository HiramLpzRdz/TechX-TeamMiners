# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ---- YOUR APP STARTS HERE ----
# -- Import section --
import os
from flask import Flask
from flask import render_template, url_for, make_response
from flask import request, redirect, session, url_for
from flask_pymongo import PyMongo
import secrets
import pymongo
import certifi
from bson import ObjectId
from datetime import datetime
import thread
import bcrypt
from model import get_preview
import requests
# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'unit4'

# URI of database
app.config['MONGO_URI'] = "mongodb+srv://admin:3sAW1DQEaqpfDtqz@cluster0.ma4v1.mongodb.net/lab9database?retryWrites=true&w=majority"

#Initialize PyMongo
mongo = PyMongo(app)

# -- Session data --
app.secret_key = secrets.token_urlsafe(16)

client = pymongo.MongoClient("mongodb+srv://admin:3sAW1DQEaqpfDtqz@cluster0.ma4v1.mongodb.net/lab9database?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.unit4
users = db.user
comments = db.comments
threads = db.thread

# -- verifies thread info --
thread_checker = thread.Thread()


# -- Routes section --
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in request.cookies:
        return redirect(url_for('main_feed'))
    if request.method == "POST":
        #search for username in database
        login_user = users.find_one({'email_address': request.form['email']})

        #if username in database
        if login_user:
            db_password = login_user['password']
            #encode password
            password = request.form['password'].encode("utf-8")
            #compare username in database to username submitted in form
            if bcrypt.checkpw(password, db_password):
                # store username in cookie
                resp = make_response(redirect(url_for('main_feed')))
                resp.set_cookie('username', login_user['name'])
                return resp
            else:
                return 'Invalid username/password combination.'
        else:
            return 'User not found.'
    else:
        return render_template('login.html')

#SIGNUP Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        #users = mongo.db.unit4.user
        #search for username in database
        existing_user = users.find_one({'name': request.form['username']})

        #if user not in database
        if not existing_user:
            username = request.form['username']
            #encode password for hashing
            password = request.form['password'].encode("utf-8")
            email_address = request.form['email']
            classification = request.form['classification']

            #hash password
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password, salt)
            #add new user to database
            users.insert_one({'name': username, 'password': hashed, 'email_address': email_address, 'classification': classification, 'profile_image': "https://png.pngitem.com/pimgs/s/22-223968_default-profile-picture-circle-hd-png-download.png"})
            #store username in cookies
            resp = make_response(redirect(url_for('main_feed')))
            resp.set_cookie('username', request.form['username'])
            return redirect(url_for('main_feed'))
        else:
            return 'Username already registered.  Try logging in.'
    
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    #clear username from session data
    resp = make_response(redirect('login'))
    resp.delete_cookie('username')
    return resp

@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    '''
    sets up user page
    :param user_id: str - id of user profile
    :return renders user.html
    '''
    if 'username' not in request.cookies:
        return render_template('login.html')
    threads_by_user = threads.find({'author': username})
    comments_by_user = comments.find({'author': username})
    user_info = users.find_one({'name': username})
    print(type(user_info))
    print('**&&&&***&&**&*&')
    return render_template('user.html', threads=threads_by_user,
                           comments=comments_by_user, username=username, cookie = request.cookies,
                           user_info=user_info)

@app.route('/change_profile', methods=['GET', 'POST'])
def change_profile():
    if request.method == 'GET':
        return "you shouldn't be here"
    new_link = request.form['new_link']
    user_info = {'name': request.cookies.get('username')}
    new_address = {"$set": {"profile_image": new_link}}
    users.update_one(user_info, new_address)
    return redirect('/user/' + request.cookies.get('username'))

@app.route('/thread/<thread_number>', methods=['GET', 'POST'])
def thread(thread_number):
    '''
    sets up thread page
    :param user_id: str - id of thread
    :return renders thread.html
    '''
    if 'username' not in request.cookies:
        return render_template('login.html')
    if request.method == 'POST':
        comment_info = thread_checker.create_comment(request.cookies.get('username'),
                                                     request.form['new_comment'],
                                                     thread_number,
                                                     request.form['image_link'])
        parent_thread = threads.find_one(ObjectId(thread_number))
        comment_info['thread_title'] = parent_thread['title']
        temp_user = users.find_one({'name': request.cookies.get('username')})
        comment_info['profile_image'] = temp_user['profile_image']
        comments.insert_one(comment_info)
    thread_info = threads.find_one(ObjectId(thread_number))
    comment = comments.find({"thread_id": thread_number})
    return render_template('thread.html', thread_info=thread_info, comments=comment,
                           thread_number=thread_number, cookie = request.cookies)

@app.route('/new_thread', methods=['GET', 'POST'])
def new_thread():
    '''
    renders template to create new thread
    :return renders new_thread.html
    '''
    return render_template('new_thread.html', cookie = request.cookies)

@app.route('/create_thread', methods=['GET', 'POST'])
def create_thread():
    '''
    sets up gets post info from /new_thread and
    created a new thread in MONGO DB
    :return renders thread.html with the new thread
    id that was just created
    '''
    if request.method == 'GET':
        return 'you should not be here'
    if request.method == 'POST':
        thread_info = thread_checker.check_new_thread(
            request.form['title'],
            request.form['text'],
            request.form['tags'],
            request.cookies.get('username'),
            request.form['video_link'],
            request.form['image_link']
        )
        _id = threads.insert_one(thread_info)
        path = '/thread/' + str(_id.inserted_id)
        return redirect(path)

@app.route('/main_feed', methods=['GET', 'POST'])
def main_feed():
    threads_info = threads.find({})
    return render_template('main_feed.html', threads = threads_info, get_preview=get_preview, cookie = request.cookies)

@app.route('/add_like/<thread_number>', methods = ['GET', 'POST'])
def add_like(thread_number):
    thread_info = threads.find_one(ObjectId(thread_number))
    likes = thread_info['likes'] + 1
    threads.update_one(thread_info, { "$set": { "likes": likes } })
    return redirect(url_for('main_feed'))
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
from flask import Flask
from flask import render_template
from flask import request, redirect
from flask_pymongo import PyMongo
import pymongo
import certifi
from bson import ObjectId
from datetime import datetime

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'unit4'

# URI of database
app.config['MONGO_URI'] = "mongodb+srv://admin:3sAW1DQEaqpfDtqz@cluster0.ma4v1.mongodb.net/lab9database?retryWrites=true&w=majority"

#Initialize PyMongo
mongo = PyMongo(app)

client = pymongo.MongoClient("mongodb+srv://admin:3sAW1DQEaqpfDtqz@cluster0.ma4v1.mongodb.net/lab9database?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.unit4
user = db.user
comments = db.comments
threads = db.thread


# -- Routes section --
# INDEX Route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/thread/<thread_number>', methods=['GET', 'POST'])
def thread(thread_number):
    if request.method == 'POST':
        comment_info = {'text': request.form['new_comment'],
                        'author': 'lenin_lover69',
                        'date_time': datetime.now().strftime("%m/%d/%Y %H:%M"),
                        'thread_id': thread_number}
        comments.insert_one(comment_info)
    thread_info = threads.find_one(ObjectId(thread_number))
    #comment = comments.find_one(ObjectId("62572533e6569223cc720c62"))
    comment = comments.find({"thread_id": thread_number})
    return render_template('thread.html', thread_info=thread_info, comments=comment,
                           thread_number=thread_number)

@app.route('/new_thread', methods=['GET', 'POST'])
def new_thread():
    return render_template('new_thread.html')

@app.route('/create_thread', methods=['GET', 'POST'])
def create_thread():
    if request.method == 'GET':
        return 'wrong'
    if request.method == 'POST':
        thread_info = {
            'title': request.form['title'],
            'text': request.form['text'],
            'author': 'fidel',
            'date_time': datetime.now().strftime("%m/%d/%Y %H:%M")
        }
        _id = threads.insert_one(thread_info)
        path = '/thread/' + str(_id.inserted_id)
        return redirect(path)
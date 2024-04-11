import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://egip3961:kuYAbaTOX@cluster0.ouoabdi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    
    today =datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    
    file_image = request.files['file_give']
    image_extension = file_image.filename.split('.')[-1]
    image_filename = f'static/post-{mytime}.{image_extension}'
    file_image.save(image_filename)

    file_profile = request.files['profile_give']
    profile_extension = file_profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{profile_extension}'
    file_profile.save(profilename)
    
    time = today.strftime('%Y.%m.%d')
    
    doc = {
        'file': image_filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time': time,
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'data was saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    
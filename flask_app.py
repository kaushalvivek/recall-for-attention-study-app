'''
A flask application for controlled experiment on
the attention on clickbait healdines

Models stored in model.py

Left to code : 
- grey screen
'''

# imports
from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import random , string
import json

# initializing the App and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///store.db'
db = SQLAlchemy(app)
sequence = 0
articles_visited = []

#-------------------------------------------------
# model for storage of page transactions
class Transactions(db.Model):
  tran_id = db.Column(db.String, primary_key=True)
  u_id = db.Column(db.String)
  article_id = db.Column(db.String)
  position = db.Column(db.Integer)
  time_before_click = db.Column(db.String)
  time_on_page = db.Column(db.String)
  sequence = db.Column(db.Integer)
#-------------------------------------------------
articles = []

# read recall questions json file
with open('questions.json') as file:
  json_file = file.read()
  json_questions = json.loads(json_file)

# app route : root
@app.route('/')
def index():
  return render_template('index.html')

# app route : launch
@app.route('/launch')
def launch():
  global articles
  if request.args.get('law') == '1':
    articles.append('law')
  if request.args.get('delhi') == '1':
    articles.append('delhi')
  if request.args.get('volcano') == '1':
    articles.append('volcano')
  if request.args.get('apple') == '1':
    articles.append('apple')
  if request.args.get('justice') == '1':
    articles.append('justice')
  if request.args.get('train') == '1':
    articles.append('train')
  print(articles)
  return render_template('launch.html')

@app.route('/get_uid')
def get_uid():
  global u_id
  u_id = request.args.get('u_id')
  return redirect('/recall_test')

# app route : end
@app.route('/end')
def end():
  return render_template('end.html')

# app route : recall_test
@app.route('/recall_test')
def recall_test():
  global articles
  questions_list = []
  for i in articles:
    questions_list.append(json_questions[i])
  questions = [j for i in questions_list for j in i]
  return render_template('recall.html', questions=questions)

if __name__ == "__main__":
  app.run(debug=True)
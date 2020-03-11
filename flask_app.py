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

# function for generation of random string
def generate_random_string(stringLength=10):
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(stringLength))

# to generate 6 news objects
def generate_news_objects():
  global news_objects
  news_objects = []
  choices = [0,0,0,1,1,1]
  random.shuffle(choices)
  for i in range(0,6):
    if(choices[i] == 0) :
      headline = json_data['articles'][i]['cb_headline']
      article_id = str(i)+'0'
    else:
      headline = json_data['articles'][i]['ncb_headline']
      article_id = str(i)+'1'
    paragraphs = json_data['articles'][i]['paragraphs']
    news_objects.append({
      'headline':headline,
      'paragraphs':paragraphs,
      'article_id':article_id
    })
  random.shuffle(news_objects)
  return

# read data json file
with open('data.json') as file:
  json_file = file.read()
  json_data = json.loads(json_file)

# read recall questions json file
with open('questions.json') as file:
  json_file = file.read()
  json_questions = json.loads(json_file)

# app route : root
@app.route('/')
def index():
  # u_id = generate_random_string(10)
  return render_template('index.html')

# app route : launch
@app.route('/launch')
def launch():
  generate_news_objects()
  return render_template('launch.html')

@app.route('/get_uid')
def get_uid():
  global u_id
  u_id = request.args.get('u_id')
  generate_news_objects()
  return redirect('/headlines')


# app route : headlines
@app.route('/headlines')
def headlines():
  h0 = news_objects[0]['headline']
  h1 = news_objects[1]['headline']
  h2 = news_objects[2]['headline']
  h3 = news_objects[3]['headline']
  h4 = news_objects[4]['headline']
  h5 = news_objects[5]['headline']
  return render_template('headlines.html', h0=h0, h1=h1, h2=h2, h3=h3, h4=h4, h5=h5)

# app route : article
@app.route('/article')
def article():
  global position
  global time_spent
  global article_id
  global transaction_id
  global articles_visited
  
  # generate transaction id
  transaction_id = generate_random_string(15)
  # position of news link on web matrix
  position = request.args.get('position')
  # time spent on page before clicking on news link
  time_spent = request.args.get('time_spent')
  news_piece = news_objects[int(position)]
  article_id = news_piece['article_id']
  headline = news_piece['headline']
  paragraphs = news_piece['paragraphs']
  # add article id to visited array, for recall test
  articles_visited.append(article_id)
  return render_template('article.html', headline=headline, paragraphs=paragraphs)

# app route : log_transactions
@app.route('/log_transaction')
def log_transaction():
  global sequence
  sequence+=1
  read_time = request.args.get('read_time')
  new_transaction = Transactions(tran_id=transaction_id,u_id=u_id,article_id=article_id,\
  position=position,time_before_click=time_spent,time_on_page=read_time, sequence=sequence)
  db.session.add(new_transaction)
  db.session.commit()
  print(sequence)
  if sequence == 3:
    return redirect('/end')
  else:
    return redirect('/headlines')

# app route : end
@app.route('/end')
def end():
  global articles_visited
  recall_items = []
  for i in articles_visited:
    if i == '00' or i == '01':
      recall_items.append('train')
    elif i == '10' or i == '11':
      recall_items.append('law')
    elif i == '20' or i == '21':
      recall_items.append('justice')
    elif i == '30' or i == '31':
      recall_items.append('apple')
    elif i == '40' or i == '41':
      recall_items.append('volcano')
    elif i == '50' or i == '51':
      recall_items.append('delhi')
  return render_template('end.html', articles=recall_items)

# app route : recall_test
# @app.route('/recall_test')
# def recall_test():
#   global articles_visited
#   print(articles_visited)
#   recall_items = []
#   for i in articles_visited:
#     if i == '00' or i == '01':
#       recall_items.append('train')
#     elif i == '10' or i == '11':
#       recall_items.append('law')
#     elif i == '20' or i == '21':
#       recall_items.append('justice')
#     elif i == '30' or i == '31':
#       recall_items.append('apple')
#     elif i == '40' or i == '41':
#       recall_items.append('volcano')
#     elif i == '50' or i == '51':
#       recall_items.append('delhi')
#   questions_list = []
#   print(recall_items)
#   for i in recall_items:
#     questions_list.append(json_questions[i])
#   questions = [j for i in questions_list for j in i]
#   return render_template('recall.html', questions=questions)

if __name__ == "__main__":
  app.run(debug=True)
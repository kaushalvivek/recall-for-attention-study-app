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
class Recall(db.Model):
  u_id = db.Column(db.String, primary_key=True)
  article_1 = db.Column(db.String)
  score_1 = db.Column(db.Integer)
  article_2 = db.Column(db.String)
  score_2 = db.Column(db.Integer)
  article_3 = db.Column(db.String)
  score_3 = db.Column(db.Integer)
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
  global questions
  questions = []
  questions_list = []
  for i in articles:
    questions_list.append({'id': i, 'questions': json_questions[i]})
  for i in questions_list:
    for j in range(0,4):
      questions.append({'id':i['id']+str(j),'question':i['questions'][j]['question'],\
       'options':i['questions'][j]['options'],'correct':i['questions'][j]['correct']})
  random.shuffle(questions)
  for i in questions:
    random.shuffle(i['options'])
  return render_template('recall.html', questions=questions, articles=articles)

@app.route('/save_to_log')
def save_to_log():
  incoming_ids = []
  score = [0 for i in range(0,len(articles))]
  for i in articles:
    for j in range(0,4):
      incoming_ids.append(i+str(j))
  responses = []
  for i in incoming_ids:
    responses.append(request.args.get(i))
  for i in range (len(articles)):
    for j in range (len(incoming_ids)):
      if articles[i] in incoming_ids[j] and responses[j] == '0':
        score[i]+=1

  new_recall = Recall(u_id=u_id,article_1=articles[0],\
  score_1=score[0],article_2=articles[1],score_2=score[1], article_3 = articles[2], score_3 = score[2])
  db.session.add(new_recall)
  db.session.commit()
  return redirect('/end')


if __name__ == "__main__":
  app.run(debug=True)
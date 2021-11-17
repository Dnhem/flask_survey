from flask import Flask, request, render_template, redirect 
# Flask session will be used for further study
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_sauce'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_homepage():
  """Go to start page and clear responses list"""
  responses = []
  return render_template('start.html', survey=survey) 

@app.route('/begin')
def begin_survey():
  return redirect('/question/0')

@app.route('/question/<int:id>')
def current_question(id):
  """Handle URLs to display current question"""
  question = survey.questions[id]
  return render_template('question.html', question_id=id, question=question)

@app.route('/answer')
def post_continue():
  """Append answer to list and proceed to next question"""
  answer = request.args['answer']
  responses.append(answer)
  if (len(responses) == len(survey.questions)):
    return render_template('completed.html')
  else:
    return redirect(f'/question/{len(responses)}')

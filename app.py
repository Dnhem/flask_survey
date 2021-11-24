from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension 
from surveys import satisfaction_survey as survey, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_sauce'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

@app.route('/')
def show_homepage():
  return render_template('start.html', survey=survey) 

@app.route('/begin', methods=["POST"])
def begin_survey():
  "Clear out responses"
  session[RESPONSES_KEY] = []
  """Redirect to first question"""
  return redirect('/question/0')

@app.route('/answer', methods=["POST"])
def post_continue():

  # get the response choice
  answer = request.form['answer']

  """Add response to session"""
  responses = session[RESPONSES_KEY]
  responses.append(answer)
  print(session[RESPONSES_KEY])
  session[RESPONSES_KEY] = responses

  """All questions answered"""
  if (len(responses) == len(survey.questions)):
    return redirect('/completed')
  else:
    return redirect(f'/question/{len(responses)}')

# This route handles all questions using a path variable
# Also compares length of data in session to length of survey questions
# To make sure questions are being answered in proper order
# Lastly it validates that all questions are answered before sending
# A thank you page to customer
@app.route('/question/<int:id>')
def current_question(id):
  responses = session.get(RESPONSES_KEY)

  """If session is empty go to beginning of page"""
  if (responses == None):
    return redirect('/')

  """They answered all the questions"""
  if (len(responses) == len(survey.questions)):
    return redirect('/completed')

  """Attempting to access questions out of order"""
  if (len(responses) != id):
    flash('Please DO NOT SKIP AHEAD, answer the questions in order!')
    return redirect(f'/question/{len(responses)}')

  """Handle URLs to display current question"""
  question = survey.questions[id]

  return render_template('question.html', question_id=id, question=question)

@app.route('/completed')
def thank_user():
  return render_template('completed.html')
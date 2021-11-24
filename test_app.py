from app import RESPONSES_KEY, app
from unittest import TestCase
from flask import session

class CheckSessionData(TestCase):

  def test_session_data(self):
    with app.test_client() as client:
      with client.session_transaction() as change_session:
        change_session['responses'] = 1

      resp = client.get('/question/<int:id>')

      self.assertEqual(session[RESPONSES_KEY], 1)

  def test_redirection(self):
    with app.test_client() as client:
      resp = client.get('/question/0')

      self.assertEqual(resp.status_code, 302)
      # self.assertEqual(resp.location, 'http://localhost:5000/begin')
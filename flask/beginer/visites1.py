from flask import Flask
from markupsafe import escape
import time, os

app = Flask(__name__)

valor=0

@app.route('/visites')
def visites():
  global valor
  valor=valor+1
  return 'visites: %d' % valor

@app.route('/data')
def data():
  global valor
  valor=valor+1
  data=time.strftime("%d-%m-%Y %H:%M.%s")
  return '(visites:%d) %s' % (valor,data)

@app.route('/hostname')
def hostname():
  global valor
  valor=valor+1
  data=os.getenv('HOSTNAME')
  #socket.gethostname()
  return '(visites:%d) %s' % (valor,data)

@app.route('/all')
def peer():
  global valor
  valor=valor+1
  nom=os.getenv('HOSTNAME')
  data=time.strftime("%d-%m-%Y %H:%M.%s")
  html = "<h3>Hello World!</h3>" \
         "<b>Visits:</b> {visites}<br/>" \
         "<b>Hostname:</b> {nom}<br/>" \
         "<b>Date:</b> {data}"
  return html.format(nom=nom,data=data,visites=valor)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/bye')
def hello_world():
    return 'Godbye, Cruel World!'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

from flask import Flask
from redis import Redis, RedisError
from markupsafe import escape
import time, os

redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


@app.route('/visites')
def visites():
  try:
    valor = redis.incr("counter")
  except RedisError:
    valor = "<i>cannot connect to Redis, counter disabled</i>"
  return 'visites: %s' % valor

@app.route('/data')
def data():
  try:
    valor = redis.incr("counter")
  except RedisError:
    valor = "<i>cannot connect to Redis, counter disabled</i>"
  data=time.strftime("%d-%m-%Y %H:%M.%S")
  return '(visites:%s) %s' % (valor,data)

@app.route('/hostname')
def hostname():
  try:
    valor = redis.incr("counter")
  except RedisError:
    valor = "<i>cannot connect to Redis, counter disabled</i>"
  data=os.getenv('HOSTNAME')
  #socket.gethostname()
  return '(visites:%s) %s' % (valor,data)

@app.route('/all')
def peer():
  try:
    valor = redis.incr("counter")
  except RedisError:
    valor = "<i>cannot connect to Redis, counter disabled</i>"
  nom=os.getenv('HOSTNAME')
  data=time.strftime("%d-%m-%Y %H:%M.%S")
  html = "<h3>Hello World!</h3>" \
         "<b>Visits:</b> {visites}<br/>" \
         "<b>Hostname:</b> {nom}<br/>" \
         "<b>Date:</b> {data}"
  return html.format(nom=nom,data=data,visites=valor)

@app.route('/llistahosts')
def llistahosts():
  nom=os.getenv('HOSTNAME')
  data=time.strftime("%d-%m-%Y %H:%M.%S")
  try:
    valor = redis.incr("counter")
    redis.rpush("lhosts",nom)
  except RedisError:
    valor = "<i>cannot connect to Redis, counter disabled</i>"
  lhb=redis.lrange("lhosts",0,-1)
  lhs=[ x.decode() for x in lhb ]
  lhosts=" ".join(lhs)
  html = "<h3>Hello World!</h3>" \
         "<b>Visits:</b> {visites}<br/>" \
         "<b>Hostname:</b> {nom}<br/>" \
         "<b>Date:</b> {data}<br/>" \
         "<b>Llista hosts:{lhosts}</b>"
  return html.format(nom=nom,data=data,visites=valor,lhosts=lhosts)

@app.route('/llistavisites')
def llistavisites():
  nom=os.getenv('HOSTNAME')
  data=time.strftime("%d-%m-%Y %H:%M.%S")
  try:
    valor = redis.incr("counter")
    redis.rpush("lhosts",nom)
    redis.zadd("lvisits",{nom:valor})
  except RedisError:
    valor = "<i>cannot connect to Redis, counter disabled</i>"
  lvb=redis.zrange("lvisits",0,-1)
  lvs=[ str((x.decode(),y)) for x,y in lvb ]
  lvisits=" ".join(lvs)
  html = "<h3>Hello World!</h3>" \
         "<b>Visits:</b> {visites}<br/>" \
         "<b>Hostname:</b> {nom}<br/>" \
         "<b>Date:</b> {data}<br/>" \
         "<b>Llista hosts:{lvisits}</b>"
  return html.format(nom=nom,data=data,visites=valor,lvisits=lvisits)


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

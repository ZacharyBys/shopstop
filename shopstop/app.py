import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'shopstop.db'),
    SECRET_KEY='jeinx2903jnfkknd29102jsn',
    USERNAME='admin',
    PASSWORD='ShopStop123'
))
app.config.from_envvar('SHOPSTOP_SETTINGS', silent=True)

@app.route('/')
def hello_world():
    return 'Welcome to Shop Stop!'

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
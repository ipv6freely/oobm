#!.venv/bin/python

""" 
ADD VIA PIP:
pip install requests
pip install flask
pip install flask-sqlalchemy
pip install Flask-WTF
"""

from flask import Flask, request, flash, url_for, redirect, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField
from wtforms import validators, ValidationError
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oobm.sqlite3'
app.config['SECRET_KEY'] = "$#@J32342#$3j4j3j4j32rjfsdFSDfj320umsdf"

db = SQLAlchemy(app)

class modemtable(db.Model):
    id = db.Column('model_id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    ipaddress = db.Column(db.String(15))
    sim = db.Column(db.String(20))

    def __init__(self, name, ipaddress, sim):
        self.name = name
        self.ipaddress = ipaddress
        self.sim = sim

class NewModemForm(Form):
   name = TextField('Modem Hostname',[validators.DataRequired(message='Please enter the modem hostname.'), validators.length(max=50)])
   ipaddress = StringField('IPv4 Address', [validators.IPAddress(message='Sorry, not a valid IPv4 Address.')], default='127.0.0.1')
   sim = TextField('SIM ID', [validators.regexp('^\d{20}$', message='Not a valid SIM ID')])
   submit = SubmitField('Add')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/newmodem', methods = ['GET', 'POST'])
def newmodem():
    form = NewModemForm(request.form)
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            modem = modemtable(form.name.data, form.ipaddress.data, form.sim.data)
            db.session.add(modem)
            db.session.commit()
            flash('Record was successfully added.', 'success')
            return redirect(url_for('modems'))
        else:
            flash('Ooopsie! You have the following errors: ','error')
    return render_template('new.html', form=form)

@app.route('/modems')
def modems():
    return render_template('modems.html', modems = modemtable.query.all() )

if __name__ == "__main__":
    db.create_all()
    app.run(debug=False,host='127.0.0.1', port=8000)
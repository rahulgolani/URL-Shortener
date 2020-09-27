from flask import Flask,render_template,request
# request for working with post requests
from flask_mail import Mail
from flask_mail import Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json','r') as c:
    params=json.load(c)["params"]

local_server=params["local_server"]

app=Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL='True',
    MAIL_USERNAME=params["gmail-username"],
    MAIL_PASSWORD=params["gmail-password"]
)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["production_uri"]

db = SQLAlchemy(app)
mail = Mail(app)

class Contact(db.Model):
    # sno,name, email,phone,message,date
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.String(10), unique=False, nullable=False)
    message = db.Column(db.String(1000), unique=False, nullable=False)
    date = db.Column(db.String(120))

@app.route('/')
def home():
    return render_template('index.html',params=params)

@app.route('/about')
def about():
    return render_template('about.html',params=params)

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        # fetching the values from the form
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        date=datetime.now()

        '''Add entry to the database'''
        entry=Contact(name=name,email=email,phone=phone,date=date,message=message)
        db.session.add(entry)
        db.session.commit()
        msg = Message('New Communication from '+email,
                  sender=email,
                  recipients=[params["gmail-username"]],
                  body=message)
        mail.send(msg)

    return render_template('contact.html',params=params)

@app.route('/post')
def post():
    return render_template('post.html',params=params)

app.run(debug=True)

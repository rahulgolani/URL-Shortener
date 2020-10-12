from flask import Flask,render_template,request, session, redirect, url_for
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
app.secret_key = '123456789'
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


class Posts(db.Model):
    # sno,name, email,phone,message,date
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=False, nullable=False)
    slug = db.Column(db.String(25), unique=False, nullable=False)
    content = db.Column(db.String(1000), unique=False, nullable=False)
    tagline = db.Column(db.String(35), unique=False, nullable=False)
    date = db.Column(db.String(120))
    img_file = db.Column(db.String(20), unique=False, nullable=False)

@app.route('/')
def home():
    posts=Posts.query.filter_by().all()[0:params["no-of-posts"]]
    return render_template('index.html',params=params,posts=posts)

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

@app.route('/post/<string:post_slug>',methods=['GET'])
def post(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post)


@app.route('/dashboard')
def dashboard():
    posts=Posts.query.all()
    if 'username' in session and session['username']==params['admin_username']:
        return render_template('dashboard.html',params=params,posts=posts)
    return render_template('login.html',params=params)

@app.route('/login', methods=['GET','POST'])
def login():
    posts=Posts.query.all()

    if 'username' in session and session['username']==params['admin_username']:
        # return redirect(url_for('dashboard',params=params,posts=posts))
        return render_template('dashboard.html',params=params,posts=posts)

    if request.method=='POST':
        # redirect to admin panel
        username=request.form.get('uname');
        userpass=request.form.get('upass');
        if (username==params['admin_username'] and userpass==params['admin_password']):
            session['username']=username# this user is logged in
            # return redirect(url_for('dashboard',params=params,posts=posts))
            return render_template('dashboard.html',params=params,posts=posts)
    return render_template('login.html',params=params)

app.run(debug=True)

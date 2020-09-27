from flask import Flask,render_template,request
# request for working with post requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/myblog'
db = SQLAlchemy(app)

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
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

    return render_template('contact.html')

@app.route('/post')
def post():
    return render_template('post.html')

app.run(debug=True)

from flask import Flask, render_template,request, redirect, url_for, flash,  abort, session
import json
import os.path

app=Flask(__name__)
app.secret_key="hello"

@app.route('/')
def index():
    return render_template('index.html', codes=session.keys())

@app.route('/about')
def about():
    return "<h1>My name is Rahul Golani</h1>"

@app.route('/your-url',methods=['GET','POST'])
def yourUrl():
    if request.method=='POST':
        code=request.form.get('code')
        urls={}

        if os.path.exists("url_file.json"):
            with open("url_file.json") as file:
                urls=json.load(file)

        if code in urls:
            # flash("This short name has already been taken. Please use another one!")
            # return redirect(url_for('index'))
            session[request.form.get('code')]=True
            return render_template('yourUrl.html',code=code)

        urls[code]={"url":request.form.get('url')}
        with open("url_file.json",'w') as file:
            json.dump(urls,file)
            session[request.form.get('code')]=True

        return render_template('yourUrl.html',code=code)
    else:
        # If user is directly putting the get request then we send invalid
        # return "<h1>This get request is not valid</h1>"

        # instead of returning some text we can redirect the user to the homepage
        return redirect(url_for('index'))

@app.route('/<string:code>')
def redirectToUrl(code):
    if os.path.exists("url_file.json"):
        with open("url_file.json") as file:
            urls=json.load(file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])

    return abort(404)

#for which error you want to create a handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"),404





app.run(debug=True)

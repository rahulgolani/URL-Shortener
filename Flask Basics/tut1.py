# First flask application

# importing the flask class from flask module
from flask import Flask
# creating an app
app=Flask(__name__)


# defining an endpoint
@app.route("/")
def hello():
    # when user goes to / endpoint, this function will run and the return value wil be displayed on the screen
    return "hello world"

# to run the app
app.run(debug=True)
# debug= True automatically reloads the page on the changes

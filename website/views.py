import json
from flask import Flask, render_template, request,redirect,url_for,Blueprint,jsonify

# //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


# ToDO : finish front end (loading and formatting), hide keys , launch , add ads. 


# input a video and get it to translate the text then summarize the text



views = Blueprint('views', __name__) 



@views.route('/')
def index():
    return render_template('index.html')

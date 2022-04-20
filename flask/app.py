import flask
from flask import Flask, render_template, request, redirect

from wsbsentiment import *
from wsbsentiment.wsbsentiment import wsbsentiment as wsb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action')
def action():
    action = str(flask.request.args.get('action'))
    if action == 'tendies':
        return flask.jsonify({"result": 'this free tendies module isn\'t ready yet.'})
    elif action == 'decode':
        outstr = """
        <div class="wsblingowrapper">
            <label for="wsblingo">enter your r/wallstreetbets lingo here.</label><br>
            <textarea id="wsblingo"></textarea><br>
            <button onclick="wsblingo()">submit</button>
            <div class="wsblingoresult"></div>
        </div>
        """
        return flask.jsonify({"result": outstr})
    elif action == '':
        return flask.jsonify({"result": 'it looks like you did\'nt select an option.'})

@app.route('/wsblingo')
def wsblingo():
    encoded = str(flask.request.args.get('wsblingotext'))
    sentiment = wsb.wsblingo(data = encoded)        
    if sentiment == "positive":
        return flask.jsonify({"wsblingoresult": "got: " + encoded + "<br>r/wallstreetbets probably thinks this will send you to the moon - positive."})
    elif sentiment == "negative":
        return flask.jsonify({"wsblingoresult": "got: " + encoded + "<br>r/wallstreetbets probably doesn't think this gives you free tendies - negative."})
    else:
        return flask.jsonify({"wsblingoresult": sentiment})

if __name__ == '__main__':
    app.run()
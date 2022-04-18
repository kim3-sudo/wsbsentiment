import flask
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action')
def action():
    action = str(flask.request.args.get('action'))
    if action == 'tendies':
        return flask.jsonify({"result": 'this free tendies module isn\'t ready yet.'})
    elif action == 'advice':
        return flask.jsonify({"result": 'this free advice module isn\'t ready yet.'})
    elif action == 'decode':
        return flask.jsonify({"result": 'enter your r/wallstreetbets lingo here.<div><textarea id="wsblingo"></textarea></div><div class="wsblingoresult"><button class="wsblingosubmit">submit</button></div>'})

@app.route('/wsblingo')
def wsblingo():
    encoded = str(flask.request.args.get('wsblingotext'))
    
if __name__ == '__main__':
    app.run()
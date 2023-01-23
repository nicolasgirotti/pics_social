from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'

@app.route("/", methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route("/account", methods=['GET','POST'])
def account():
    return render_template('account.html')

@app.route("/registration", methods=['GET','POST'])
def registration():
    return render_template('registration.html')

@app.route("/login", methods=['GET','POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
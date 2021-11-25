import os
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username=='admin' and password=='password':
            session['user'] = username
            return render_template('login.html', message="Login Succesful")
        else:
            return render_template('login.html', error="Invalid username")
    return render_template('login.html')
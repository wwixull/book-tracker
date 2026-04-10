from flask import Flask, request, redirect, url_for, render_template, session

app = Flask(__name__)
app.secret_key = "oidjwoiqj./uqj0q9/871d23hqd45f6"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
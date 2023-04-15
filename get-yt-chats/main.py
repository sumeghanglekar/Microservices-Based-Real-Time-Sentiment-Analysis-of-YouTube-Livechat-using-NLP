from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

@app.route('/getChats')
def main():
    return 'Hi'



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
from flask import Flask, request
from fastText import load_model



app = Flask(__name__)

@app.route('/')
def test():
    return 'Hello'

@app.route('/fastSentiment',methods=["POST"])

def main():
    classifier = load_model("model_tweet.bin")
    msg = request.json['msg']
    labels = classifier.predict(msg)
    if(labels[0][0] == '__label__0'):
        return 'negative'

    elif(labels[0][0] == '__label__4'):
        return 'positive'

    else:
        return 'neutral'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
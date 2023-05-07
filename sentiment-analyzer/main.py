from flask import Flask, request
from fasttext import load_model
import time



app = Flask(__name__)

@app.route('/')
def test():
    return 'Hello'

@app.route('/fastSentiment',methods=["POST"])
def main():
    start_time = time.time()

    classifier = load_model("model_tweet.bin")
    msg = request.json['msg']
    labels = classifier.predict(msg)
    print(labels)
    if(labels[0][0] == '__label__0'):
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: ", elapsed_time)
        return 'negative'

    elif(labels[0][0] == '__label__4'):
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: ", elapsed_time)
        return 'positive'

    else:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: ", elapsed_time)
        return 'neutral'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
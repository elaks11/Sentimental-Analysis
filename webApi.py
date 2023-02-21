from flask import Flask, request, render_template
from sentimental import TwitterClient

app = Flask(__name__)


@app.route('/')
def home():
    dataDict = {'value': '', 'buttonDisable': '', 'isDisplay': False}
    return render_template('index.html', data=dataDict)


@app.route('/result', methods=['POST'])
def result():
    data = request.form
    api = TwitterClient()

    tweets = api.get_tweets(query=data['nameInput'], count=200)

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    nntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    dataDict = {'value': data['nameInput'],
                'buttonDisable': 'disabled',
                'isDisplay': True,
                'pvalue': 100 * len(ptweets) / len(tweets),
                'nvalue': 100 * len(ntweets) / len(tweets),
                'nnvalue': 100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets),
                }

    return render_template('index.html', data=dataDict)


if __name__ == '__main__':
    app.run(debug=True)

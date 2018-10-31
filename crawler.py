import sys
import tweepy
from pymongo import MongoClient
import nltk

consumer_key = 'cMlGmUqVEl0LHsURqmg3KFJ06'
consumer_secret = 'pY5AFjmpSt9u511H8Pg6n7bh0njFxIaSzxONwXqqXtzmJGBXQv'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
access_token = "954173457851273216-4o9v5zh8yeEeRTXOGI9kcPv24fUQ7rz"
access_token_secret = "3Lre0L0kppXvuZ9tvLco4z0eN6GoJHNkpeqHt0EFOH4Kx"
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
client = MongoClient()
db = client['word2vec']
collection = db.tweet


class Listener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            txt = status.extended_tweet['full_text']
        except:
            txt = status.text
        if 'https' in txt:
            res = txt.split('https')
            txt = res[0]

        if status.lang == 'en':
            try:
                coordinate = status.place.bounding_box.coordinates[0][0]
                created_at = status.created_at
                post = {"text": txt.lower(), "coordinate": coordinate, "created_at": created_at}
                print(txt)
                collection.insert(post)
            except Exception as e:
                print(e.args)
                print("DB Error")
                return True

    def on_error(self, status_code):
        print(sys.stderr, "Encountered error with status code:", status_code)
        return True

    def on_timeout(self):
        print(sys.stderr, "Timeout")
        return True


if __name__ == '__main__':
    ct = tweepy.streaming.Stream(auth, Listener())
    ct.filter(locations=[-123.915252, 31.991705, -67.665251, 49.068417])

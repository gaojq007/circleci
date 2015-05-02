import os
from flask import Flask
from redis import Redis


app = Flask(__name__)
redis = Redis(host="redis_1", port=6379)

@app.route('/')
def hello():
    redis.incr('views')
    return 'Bonjour! Cette page a été vue {0} fois.'.format(
        redis.get('views'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

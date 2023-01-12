from flask import Flask, Response
from threading import Thread

from apscheduler.schedulers.background import BackgroundScheduler

from libs.my_feed import MyFeed

app = Flask(__name__)


@app.route("/")
def home():
    return "076bei-bot is running."


@app.route("/rss")
def feed():
    with open("feed/rss.xml") as f:
        xml = f.readlines()
    r = Response(response=xml, status=200, mimetype="application/xml")
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r


@app.route("/feed/rss.xml")
def feed_old():
    with open("feed/rss.xml") as f:
        xml = f.readlines()
    r = Response(response=xml, status=200, mimetype="application/xml")
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r


# def deploy():
#     import subprocess

#     exec_cmd = '''npx surge ./_site --domain "$SURGE_DOMAIN" --token "$SURGE_TOKEN"'''

#     # if update_feed:
#     MyFeed().update_feed()

#     process = subprocess.Popen(exec_cmd.split(), stdout=subprocess.PIPE)
#     output, error = process.communicate()


scheduler = BackgroundScheduler()
scheduler.add_job(MyFeed().update_feed, "interval", minutes=30)
scheduler.start()


def run():
    MyFeed().update_feed()
    app.run(host="0.0.0.0", port=1337)


def keep_alive():
    t = Thread(target=run)
    t.start()

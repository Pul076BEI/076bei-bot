import os

import pendulum
from pymongo import MongoClient
from feedgen.feed import FeedGenerator

import libs.config as config

####################
# String variables #
####################
s_feed_info = config.get_string("feed_info")
s_mongodb = os.environ["MONGODB_URI"]


class MyFeed(FeedGenerator):
    def __init__(self):
        super().__init__()
        self.mongo_client = MongoClient(s_mongodb, tls=True)
        self.server_db = self.mongo_client[os.environ["mongodb_name"]]
        self.updates = self.server_db[os.environ["collection_name"]]

        self.title(s_feed_info["feed_title"])
        self.subtitle(s_feed_info["feed_subtitle"])
        self.logo(s_feed_info["feed_logo"])
        self.link(href=s_feed_info["feed_url"])

        self.feed_manager = s_feed_info["feed_manager"]

        self.author(
            {
                "name": self.feed_manager["name"],
                "email": self.feed_manager["email"],
                "uri": self.feed_manager["url"],
            }
        )
        self.webMaster(webMaster=s_feed_info["feed_manager"]["url"])

    def update_feed(self):
        for entry in self.updates.find():
            fe = self.add_entry()
            fe.title(entry["channel_name"])
            fe.link(href=entry["message_url"])
            fe.description(f"""{entry["message"]}<br><br>- @{entry["author"]}""")
            fe.published(
                pendulum.from_format(
                    entry["publish_date"], "YYYY-MM-DD HH:mm:ss ZZ", tz="UTC"
                )
            )  # Get date-time as datetime object

        self.rss_str(pretty=True)  # Get the RSS feed as string
        self.rss_file("feed/rss.xml")  # Write the RSS feed to a file

    def add_feed(self, msg, attachment):
        channel_id = str(msg.channel.id)
        channel_name = msg.channel.name

        message = (
            f"{msg.content} <br><br>Attachment: {str(attachment).split()[3][5:-3]}"
            if len(attachment) > 0
            else msg.content
        )

        message_id = str(msg.id)

        author = (
            f"{msg.author.name} | {msg.author.nick}"
            if msg.author.nick is not None
            else msg.author.name
        )

        publish_date = pendulum.now(tz="UTC")
        str_date = publish_date.format("YYYY-MM-DD HH:mm:ss ZZ")

        new_update = {
            "message_url": f"https://discord.com/channels/758544148121780226/{channel_id}/{message_id}",
            "channel_name": channel_name,
            "message": message,
            "author": author,
            "publish_date": str_date,
        }

        self.updates.insert_one(new_update)

        self.update_feed()

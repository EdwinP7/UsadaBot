import parserz
import praw
import configparser
import config
import random

class Comment(object):
    def __init__(self, id, body):
        self.id = id
        self.body = body

def client_login():
    reddit = praw.Reddit(
        client_secret=config.CLIENT_SECRET,
        client_id=config.CLIENT_ID,
        username=config.USERNAME,
        password=config.PASSWORD,
        user_agent=config.USER_AGENT,
    )
    return reddit


def whos_hot(reddit):

    parser = configparser.ConfigParser()
    parser.read(config.CONFIG_FILE)
    for comment in reddit.subreddit('test').comments(limit=25):
        body = comment.body
        
        if not parser.has_option('REPLIES', str(comment.id)):
            if body.lower() == 'bad bot' and comment.parent().author.name == reddit.user.me():
                bite = random.randint(0, len(parserz.fun_bites['bad bot']) - 1)
                reply = parserz.fun_bites['bad bot'][bite]
                comment.reply(reply.format(user=comment.author.name))
                parser['REPLIES'][str(comment.id)] = 'True'

            elif 'usadabot' in body and body.split()[0] == 'usadabot':
                reply = parserz.get_bot_response(comment.body)
                comment.reply(reply)
                parser['REPLIES'][str(comment.id)] = 'True'

    with open(config.CONFIG_FILE, 'w') as configfile:
        parser.write(configfile)

reddit = client_login()
print(whos_hot(reddit))

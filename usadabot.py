import parserz
import praw
import configparser
import config
import random
import re

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
    """
    Browse /r/MMA
    Respond to comments requesting USADA info on a fighter,
    Respond to comments being cheeky little basterds
    """

    parser = configparser.ConfigParser() 
    parser.read(config.CONFIG_FILE)

    for comment in reddit.subreddit('MMA').comments(limit=1000):
        body = comment.body
        author = comment.author.name

        if not parser.has_option('REPLIES', str(comment.id)):
            reply = None
            if body.lower() == 'bad bot' and comment.parent().author.name == reddit.user.me():
                # Make a cute response
                bite = random.randint(0, len(parserz.fun_bites['bad bot']) - 1)
                reply = parserz.fun_bites['bad bot'][bite]
            elif re.search('usadabot', body, re.IGNORECASE) and body.split()[0].lower() == 'usadabot' and author != reddit.user.me():
                # Make a juicy response
                try:
                    reply = parserz.get_bot_response(body)
                except:
                    reply = 'Ya broke it...try something like:\n\nusadabot ronda rousey'

            if reply is not None:
                reply = reply + '\n\n^(summoned by: {summoner})'.format(summoner=author)
                comment.reply(reply.format(user=author))
                parser['REPLIES'][str(comment.id)] = 'True'

    with open(config.CONFIG_FILE, 'w') as configfile:
        parser.write(configfile)


if __name__ == '__main__':
    reddit = client_login()
    while True:
        whos_hot(reddit)
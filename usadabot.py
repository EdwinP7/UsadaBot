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
    for comment in reddit.subreddit('MMA').comments(limit=1000):
        body = comment.body
        
        if not parser.has_option('REPLIES', str(comment.id)):
            if body.lower() == 'bad bot' and comment.parent().author.name == reddit.user.me():
                bite = random.randint(0, len( parserz.fun_bites['bad bot']) - 1)
                reply = parserz.fun_bites['bad bot'][bite]
                reply = reply + '\n\n^(summoned by: {summoner})'.format(summoner=comment.author.name)
                comment.reply(reply.format(user=comment.author.name))
                parser['REPLIES'][str(comment.id)] = 'True'
            elif 'usadabot' in body and body.split()[0] == 'usadabot' and comment.author.name != reddit.user.me():
                try:
                    reply = parserz.get_bot_response(comment.body)
                    reply = reply + '\n\n^(summoned by: {summoner})'.format(summoner=comment.author.name)
                except:
                    reply = 'Ya broke it...try something like:\nusadabot ronda rousey\n\n^(summoned by: {summoner})'.format(summoner=comment.author.name)
                comment.reply(reply)
                parser['REPLIES'][str(comment.id)] = 'True'

    with open(config.CONFIG_FILE, 'w') as configfile:
        parser.write(configfile)


if __name__ == '__main__':
    reddit = client_login()
    while True:
        whos_hot(reddit)
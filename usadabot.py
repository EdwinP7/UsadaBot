import praw
import configparser
import config
import random
import re
import urllib.request
from parserz import *
from bs4 import BeautifulSoup

# Name of section where replied-to comment ids are listed in
# ini file
REPLIES_SECTION = 'REPLIES'

# Footer used to display author of comment which summoned
# the usadabot
SUMMONED_BY_FOOTER = '\n\n^(summoned by: {summoner})'

ERROR_MESSAGE = 'Ya broke it...try something like:\n\nusadabot Jon Jones'


def client_login():
    """
    Reddit object initialization
    """

    login = praw.Reddit(
        client_secret=config.CLIENT_SECRET,
        client_id=config.CLIENT_ID,
        username=config.USERNAME,
        password=config.PASSWORD,
        user_agent=config.USER_AGENT,
    )
    return login


def has_usadabot_inquiry(reddit, text, author):
    if not re.search('usadabot', text, re.IGNORECASE):
        return False
    elif text.split()[0].lower() == 'usadabot' and author != reddit.user.me():
        return True


def mark_comment_as_replied(parser, comment_id):
    parser[REPLIES_SECTION][comment_id] = 'True'
    with open(config.CONFIG_FILE, 'w') as configfile:
        parser.write(configfile)


def run_bot(reddit):
    """
    Browse /r/MMA
    Respond to comments requesting USADA info on a fighter,
    Respond to comments being cheeky little basterds
    """

    parser = configparser.ConfigParser() 
    parser.read(config.CONFIG_FILE)

    for comment in reddit.subreddit('test').comments(limit=1000):
        body = comment.body
        author = comment.author.name
        bot_response = None

        if not parser.has_option(REPLIES_SECTION, comment.id):
            
            if body.lower() == 'bad bot' and comment.parent().author.name == reddit.user.me():
                bot_response = get_random_response(parserz.fun_bites['bad bot'])
            elif has_usadabot_inquiry(reddit, body, author):
                try:
                    bot_response = get_bot_response(body)
                except Exception as exc:
                    print(exc)
                    bot_response = ERROR_MESSAGE

            if bot_response is not None:
                bot_response = bot_response.format(user=author) + SUMMONED_BY_FOOTER.format(summoner=author)
                comment.reply(bot_response)
                mark_comment_as_replied(parser, comment.id)


def get_easter_egg_message(body): 
    for key in easter_egg_names:
        if re.search(key, body, re.IGNORECASE):
            return easter_egg_names[key]
    return None


def build_juicy_response(reasons_list, terms, name, start_date, end_date):

    if name.lower() in fun_bites:
        header = fun_bites[name.lower()]
    elif 'Non-Analytical' in reasons_list:
        header = '[Ehhhh..](https://imgur.com/gallery/BDjhxfJ)'
    elif terms in non_fault:
        header_bite = random.randint(0, (len(non_juicy_responses) - 1))
        header = non_juicy_responses[header_bite]
    else:
        header_bite = random.randint(0, (len(juicy_responses) - 1))
        header = juicy_responses[header_bite]

    reasons = re.sub(r'[^\w]', ' ', reasons_list).lower().split(' ')
    for key in reasons_fun_bites:
        if key in reasons:
            bite = random.randint(0, (len(reasons_fun_bites[key]) - 1))
            header = reasons_fun_bites[key][bite]

    name = re.sub(r'[\n]', '', name)
    markdown = '{header}\n\nName|Reasons|Terms|Sanction Start|Sanction End\n:---|:---|:---|:---|:---\n\{name}|{reason}|{terms}|{start}|{end}\n'.format(
            header=header,
            name=name,
            reason=reasons_list,
            terms=terms,
            start=start_date,
            end=end_date
            )

    return markdown


def get_random_response(responses):
    """
    Get a random response from a list
    """

    bite = random.randint(0, len(responses) - 1)
    reply = responses[bite]
    return reply


def get_bot_response(body, bad_bot=False):
    """
    Creates a response for a sanctioned athlete,
    for a non-sanctioned athlete,
    or a generic help message if the command is wrong
    """

    if bad_bot:
        return get_random_response(fun_bites['bad bot'])

    name = re.sub('usadabot', '', body, re.I)
    easter_egg = get_easter_egg_message(name)
    if easter_egg is not None:
        return easter_egg

    body_content = body.split(' ')
    if len(body_content) > 2:
        sanctions = get_sanctions(body_content[1].lower(), body_content[2].lower())
        if sanctions is None:
            random_non_juicy = random.randint(0, (len(non_juicy_responses) - 1))
            message = non_juicy_responses[random_non_juicy]
        else:
            message = build_juicy_response(*sanctions)
    else:
        message = 'Try again. Like so: usadabot Jon Jones'

    return message


def get_sanctions(firstname, lastname):
    """
    Check first and last names against USADA Sanction table database
    Return the sanctioned athlete's sanction row from table
    """
    table = get_usada_table()
    results = table.find_all('a',
                             string=lambda x: x and x.lower() == '{0}, {1}'.format(lastname, firstname))
    # Results of basic lastname, firstname check
    if results:
        name = results[0].text
        row_contents = results[0].parent.parent.contents
        sanction_start = row_contents[5].text
        sanction_end = row_contents[6].text
        reasons = row_contents[3].text
        terms = row_contents[7].text
        return (reasons, terms, name, sanction_start, sanction_end)
    # Take a deeper look at the Sanctions table for a firstname, lastname match
    else:
        name_cells = table.find_all('a')
        result = match_first_and_last(name_cells, firstname, lastname)
        if result is not None:
            name = result.text
            row_contents = result.parent.parent.contents
            sanction_start = row_contents[5].text
            sanction_end = row_contents[6].text
            reasons = row_contents[3].text
            terms = row_contents[7].text
            return (reasons, terms, name, sanction_start, sanction_end)

    return None

  
def match_first_and_last(name_cells, firstname, lastname):
    for name in name_cells:
        if name.text and re.search(firstname, name.text.lower()) and re.search(lastname, name.text.lower()):
            return name
    return None

    
def get_usada_table():
    """
    Returns USADA's Sanctions Table as a beautiful soup
    """

    url = 'https://ufc.usada.org/testing/results/sanctions/'
    with urllib.request.urlopen(url) as sanctions:
        html = sanctions.read()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='tablepress-2').find('tbody')

    return table


if __name__ == '__main__':
    reddit = client_login()
    while True:
        run_bot(reddit)
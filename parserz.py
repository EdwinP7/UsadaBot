import urllib.request
import random
import re
from bs4 import BeautifulSoup

juicy_responses = [
    'Juiced up feck.',
    'Juiced to the gills.',
    'Juicy little slut',
    '👀👀👀👀👀👀👀👀👀👀',
    '💉💉💉💉💉💉💉💉💉💉',
    '🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀'
]

non_juicy_responses = [
    'It\'s just the angle, bro.',
    'I didn\'t find anything.',
    'Either this person hasn\'t been sanctioned (yet) or you misspelled their name.',
]

fun_bites = {
    'lesnar, brock': 'He\'s just a jacked up white boy. Deal with it.',
    'bad bot': [
        'How bout u go an fuck off my page then u peice of shit u think \
         I need a stupid fuckwitt like u telling me about being bad who the \
         fuck are u take your worthless advice and get the fuck out of here',
        '[Okay](https://j.gifs.com/VPZxyX.gif)',
        'u/{user} I\'m Sitting on about $8 million bitcoin, I have $2 million in \
        reddit gold. I won the UFC belt nine times. I\'m internationally famous. \
        I\'m 6\'4. You on the other hand: i\'m guessing 5 feet flat, I\'m guessing \
        with the net worth of $100,000. Never won any titles, can walk around \
        without anyone giving a fuck who you are or what you do. my point is, \
        you and I as redditors are not even close to being on the same level. \
        I\'m guessing that\'s why you are constantly attacking me, it\'s \
        understandable. You\'re literally and figuratively like a boy \
        compared to someone like me. I\'m actually questioning myself as \
        I\'m writing this thinking "why am I even giving you the time of day" \
        every time I turn around you are writing me some bullshit, why do \
        you try so hard to get my attention?',
        'that\'s funny coming from a juicy little slut like u would love u \
        to say anything to my face fucken cheating little betch u another \
        steroid usin bitch look at your pathetic bitch ass',
        'Lol you wear turtlenecks',
    ],
    'diaz, nick': '[A gentleman never tells. ^(A gentleman never tells, nah...)](https://www.youtube.com/watch?v=piEb_XdZsMQ&feature=youtu.be&t=27)',

}

reasons_fun_bites = {
    'cannabidiol': [
        '[🚭🚭🚭...](http://i.imgur.com/WY3lX.gif)',
        '[🌲🌲🌲...](https://i.imgur.com/ICbfkUY.gifv)',
    ],
    'carboxy': [
        '[🚭🚭🚭...](http://i.imgur.com/WY3lX.gif)',
        '[🌲🌲🌲...](https://i.imgur.com/ICbfkUY.gifv)',
    ],
    'thc': [
        '[🚭🚭🚭...](http://i.imgur.com/WY3lX.gif)',
        '[🌲🌲🌲...](https://i.imgur.com/ICbfkUY.gifv)',
    ]
}

non_fault = [
    'No Fault or Negligence',
]

def build_juicy_response(sanctions):
    reasons_list = sanctions[0]
    terms = sanctions[1]
    name = sanctions[2]

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
    markdown = '{header}\n\nName|Reasons|Terms\n:---|:---|:---\n{name}|{reason}|{terms}\n'.format(
        header=header,
        name=name, 
        reason=reasons_list,
        terms=terms)

    return markdown


def get_bot_response(body):
    
    body_content = body.split(' ')
    if len(body_content) >= 2:
        sanctions = get_sanctions(body_content[1].lower(), body_content[2].lower())
        if sanctions is None:
            random_non_juicy = random.randint(0, (len(non_juicy_responses) - 1))
            message = non_juicy_responses[random_non_juicy]
        else:
            message = build_juicy_response(sanctions)
    else:
        message = 'Try again. Like so: usadabot Jon Jones'

    return message


def get_sanctions(firstname, lastname):
    """
    Check first and last names against USADA Sanction table database
    """
    name = '{0} {1}'.format(firstname, lastname)
    table = get_usada_table()
    results = table.find_all('a',
                             string=lambda x: x and x.lower() == '{0}, {1}'.format(lastname, firstname))
    if results:
        name = results[0].text
        row_contents = results[0].parent.parent.contents
        reasons = row_contents[3].text
        terms = row_contents[7].text
        return [reasons, terms, name]
    else:
        links = table.find_all('a')
        result = check_string(links, firstname)
        if result is not None:
            name = result.text
            row_contents = result.parent.parent.contents
            reasons = row_contents[3].text
            terms = row_contents[7].text
            return [reasons, terms, name]
        else:
            return None
    
def check_string(links, firstname):
    for link in links:
        if link.text and re.search(firstname, link.text.lower()):
            return link
    return None

    

def get_usada_table():
    """
    Returns USADA's Sanctions Table as soup
    """

    url = 'https://ufc.usada.org/testing/results/sanctions/'
    with urllib.request.urlopen(url) as sanctions:
        html = sanctions.read()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='tablepress-2').find('tbody')

    return table

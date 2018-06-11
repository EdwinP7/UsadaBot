import urllib.request
import random
import re
from bs4 import BeautifulSoup


RESPONSE_FOR_VITOR = 'You\'ll have to talk to Jesus Christ.' 
RESPONSE_FOR_DANA = '[Dana White USADA Results]\(http://assets.sbnation.com/assets/946296/Screen_shot_2012-02-10_at_11.25.26_PM.png)'
RESPONSE_FOR_UBER = '🏇'
RESPONSE_FOR_CORMIER = 'Do you think I\'m just gunna sit there and let you test me USADA?'
RESPONSE_FOR_GSP = 'Definitely just the angle, bro.'
RESPONSE_FOR_BUZZ = '[...](https://i.imgur.com/NUkLn6c.jpg)'
RESPONSE_FOR_DERN = '🍔🍔🍔🍔🍔🍔🍔🍔'
RESPONSE_FOR_HUNT = 'that\'s funny coming from a juicy little slut like u would love u \
        to say anything to my face fucken cheating little betch u another \
        steroid usin bitch look at your pathetic bitch ass'

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
    'diaz, nick': '[A gentleman never tells. ^(A gentleman never tells, nah...)](https://streamable.com/3p3o3)',

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


easter_egg_names = {
    'dana white': RESPONSE_FOR_DANA,
    'vitor': RESPONSE_FOR_VITOR,
    'trtor': RESPONSE_FOR_VITOR,
    'belfort': RESPONSE_FOR_VITOR,
    'ubereem': RESPONSE_FOR_UBER,
    'overeem': RESPONSE_FOR_UBER,
    'alistair': RESPONSE_FOR_UBER,
    'cormier': RESPONSE_FOR_CORMIER,
    'gsp': RESPONSE_FOR_GSP,
    'pierre': RESPONSE_FOR_GSP,
    'mark hunt': RESPONSE_FOR_HUNT,
    'dern': RESPONSE_FOR_DERN,
    'buzznight': RESPONSE_FOR_BUZZ,
}

non_fault = [
    'No Fault or Negligence',
]
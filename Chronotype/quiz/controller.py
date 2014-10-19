'''
Created on 5 Oct 2014

@author: Ed
'''
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.templatetags.static import static
from django.template.loader import render_to_string

from django.contrib.sites.models import get_current_site

from quiz.models import Delegate, Printer
import urllib2, urllib

logger = logging.getLogger(__name__)

#URL = 'http://remote.bergcloud.com/playground/direct_print/P3WPAOFL3FDN'
URL = 'http://127.0.0.1:8010/'

class Choice(object):
    def __init__(self, text, score):
        self.text = text
        self.score = score
        
class Question(object):
    def __init__(self, question, choices):
        self.question = question
        self.choices = choices
    
    def score(self, answer):
        """return the score for this question"""
        if answer > 0 and answer <= len(self.choices):
            scores = [choice.score for choice in self.choices]
            return scores[answer - 1]
        else:
            raise AssertionError('answer number ({0}) not valid for the number of choices for this question ({1})'.format(len(self.choices)))
    
                
QUESTIONS = [
    Question('What time would you get up if you were entirely free to plan your day?',
             [Choice('Between 5am and 6.30am', 5),
              Choice('Between 6.30 and 8am', 4),
              Choice('Between 8am and 9.30am', 3),
              Choice('Between 9.30am and 11am', 2),
              Choice('Between 11am and noon', 1)]),
    Question('During the first half hour after having woken in the morning, how tired do you feel?',
             [Choice('Very tired', 1),
              Choice('Fairly tired', 2),
              Choice('Fairly refreshed', 3),
              Choice('Very refreshed', 4)]),
    Question('At what time in the evening do you feel tired and, as a result, in need of sleep?',
             [Choice('Between 8pm and 9pm', 5),
              Choice('Between 9pm and 10.30pm', 4),
              Choice('Between 10.30pm and 12.30am', 3),
              Choice('Between 12.30am and 2am', 2),
              Choice('Between 2am and 3am', 1)]),
    Question('At what time of day do you think that you reach your "feeling best" peak?',
             [Choice('Between 5am and 8am', 5),
              Choice('Between 8am and 10am', 4),
              Choice('Between 10am and 5pm', 3),
              Choice('Between 5pm and 10pm', 2),
              Choice('Between 10pm and 5am', 1)]),
    Question('Which one of these types do you consider yourself to be?',
             [Choice('Definitely a "morning" type', 6),
              Choice('Rather more a "morning" than "evening" type', 4),
              Choice('Rather more an "evening" than a "morning" type', 2), 
              Choice('Definitely an "evening" type', 0)]),
    Question('Which is your favourite pie?',
             [Choice('Pork Pie', 0),
              Choice('Steak and Kidney Pie', 0),
              Choice('Homity Pie (v)', 0),
              Choice('Apple Pie', 0),
              Choice('Mince Pie', 0),])
            ]

image = {5: 'extremelarksmall.jpg',
         4: 'larksmall.jpg',
         3: 'owlarksmall.jpg',
         2: 'owlsmall.jpg',
         1: 'extremeowlsmall.jpg'}

image_highres = {5: 'extremelark.jpg',
               4: 'lark.jpg',
               3: 'owlark.jpg',
               2: 'owl.jpg',
               1: 'extremeowl.jpg'}

chronotype = {5: 'Extreme Lark',
              4: 'Lark',
              3: 'Owlark',
              2: 'Owl',
              1: 'Extreme Owl',}

def print_badge(delegate):
    name = delegate.first_name + ' ' + delegate.last_name
    organisation = delegate.organisation
    badge_html = render_to_string('quiz/badge.html', 
                                  {'name': name.upper(),
                                   'organisation': organisation,
                                   'image': 'http://' + 
                                        get_current_site(None).domain + 
                                        static('quiz/images') + 
                                        '/' + 
                                        image[delegate.quiz_result]})
    logger.debug(badge_html)
    post_data = [('html', badge_html)]
    printer = Printer.objects.all().first()
    if printer is None:
        raise ValueError('No Little Printer URL configured. Check Database.')
    url = printer.url
    handle = urllib2.urlopen(url, urllib.urlencode(post_data))
    content = handle.read()
    if content == "Sorry, I'm offline right now!":
        logger.info("Little printer offline, unable to print.")
        return False
    elif content == "OK":
        return True
    else:
        logger.error("Unexpected response from Little Printer: '{0}'".format(content))
        return False
        
def calculate_quiz_result(responses):
    """Calculate the chronotype based on the responses. 
       Returns the chronotype as a score between 1 and 5."""
    assert len(responses) == len(QUESTIONS), 'number of responses ({0}) != number of questions ({1})'.format(len(responses), len(QUESTIONS))
    score = 0
    for index, question in enumerate(QUESTIONS):
        score += question.score(responses[index])
    assert score >= 4 and score <= 26, 'illegal score ({0})'.format(score)
    if score >= 4 and 7 >= score:
        return 1
    elif score >= 8 and 11 >= score:
        return 2
    elif score >= 12 and 17 >= score:
        return 3
    elif score >= 18 and 21 >= score:
        return 4
    elif score >= 22 and 25 >= score:
        return 5
    else:
        raise AssertionError('illegal score ({0})'.format(score))

def process_print_queue():
    okay_to_print = False
    delegate = Delegate.objects.filter(printed=False).order_by('created').first()
    if delegate is not None:
        last_printed = Delegate.objects.filter(printed=True).order_by('created').first()
        if last_printed is not None:
            time_since_last_request = datetime.now() - last_printed.created
            if time_since_last_request < timedelta(seconds=settings.MIN_PRINT_INTERVAL):
                logger.info('Ignored print badge request because previous request was {0} seconds ago. Setting MIN_PRINT_INTERVAL={1} seconds.'.format(
                                                                                                    time_since_last_request, settings.MIN_PRINT_INTERVAL))
                message = 'Nothing to do.'
            else:
                okay_to_print = True
        else:
            okay_to_print = True
    else:
        message = 'No more badges to print.'

    if okay_to_print:
        success = print_badge(delegate)
        if success:
            delegate.printed = True
            delegate.save()
            message = 'Printing badge for {0}.'.format(str(delegate))
        else:
            message = 'Printer offline. Badge will be printed when printer is connected.'
    logger.info(message)
    return message

# calculateResult: function () {
# var e,
# t = this.result,
# n = 0;
# for (var i in t) t.hasOwnProperty(i) && (n += parseInt(t[i], 10));
# return n >= 4 && 7 >= n ? e = 'result5' : n >= 8 && 11 >= n ? e = 'result4' : n >= 12 && 17 >= n ? e = 'result3' : n >= 18 && 21 >= n ? e = 'result2' : n >= 22 && 25 >= n && (e = 'result1'),
# e
# }, 
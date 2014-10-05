'''
Created on 5 Oct 2014

@author: Ed
'''

#from quiz.models import Delegate, Printer, Badge
import urllib2, urllib


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
            ]

image = {1: 'extremelarksmall.jpg',
         2: 'larksmall.jpg',
         3: 'owlarksmall.jpg',
         4: 'owlsmall.jpg',
         5: 'extremeowlsmall.jpg'}

chronotype = {1: 'Extreme Lark',
              2: 'Lark',
              3: 'Owlark',
              4: 'Owl',
              5: 'Extreme Owl',}

def print_badge(delegate):
    name = delegate.first_name + ' ' + delegate.last_name
    organisation = delegate.organisation
    post_data = [('html', '<html><head><meta charset="utf-8">' +
                '''<style type="text/css">
body {
background: #fff;
color: #000;
width: 384px;
margin: 0px;
padding: 20px 0px;
}
h1 {
word-wrap: break-word;
text-align: center;
font-family: 'Quicksand';
font-size: 325%;
font-weight: bold;
}
h2 {
word-wrap: break-word;
text-align: center;
font-family: 'Quicksand';
font-size: 250%;
font-weight: normal;
}
h3 {
word-wrap: break-word;
text-align: center;
font-family: 'Latin Modern Mono Prop;
font-size: 125%;
font-weight: normal;
}
</style>''' +
                '</head><body>' +
                '<h1>' + name.upper() + '</h1>' +
                '<h2>' + organisation + '</h2>' +
                '<img src="http://data-badge.appspot.com/static/quiz/images/{0}"></img>'.format(image[delegate.quiz_result]) +
                '<h3>made by theotherwayworks.co.uk</h3>' +
                '</body></html>')]
    result = urllib2.urlopen('http://remote.bergcloud.com/playground/direct_print/P3WPAOFL3FDN', urllib.urlencode(post_data))
    content = result.read()
    if content == 'OK':
        print('Successfully printed badge: ' + name)
    else:
        print('Unexpected response from remote.bergcloud.com:')
        print content

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
    elif score >= 25 and 26 >= score:
        return 5
    else:
        raise AssertionError('illegal score ({0})'.format(score))

# calculateResult: function () {
# var e,
# t = this.result,
# n = 0;
# for (var i in t) t.hasOwnProperty(i) && (n += parseInt(t[i], 10));
# return n >= 4 && 7 >= n ? e = 'result5' : n >= 8 && 11 >= n ? e = 'result4' : n >= 12 && 17 >= n ? e = 'result3' : n >= 18 && 21 >= n ? e = 'result2' : n >= 22 && 25 >= n && (e = 'result1'),
# e
# }, 
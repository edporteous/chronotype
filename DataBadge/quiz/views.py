from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone

from quiz.models import *

class Question(object):
    def __init__(self, question, choices):
        self.question = question
        self.choices = choices
                
questions = [
    Question('What time would you get up if you were entirely free to plan your day?',
             ['Between 5am and 6.30am',
              'Between 6.30 and 8am',
              'Between 8am and 9.30am',
              'Between 9.30am and 11am',
              'Between 11am and noon',]),
    Question('During the first half hour after having woken in the morning, how tired do you feel?',
             ['Very tired',
              'Fairly tired',
              'Fairly refreshed',
              'Very refreshed',]),
    Question('At what time in the evening do you feel tired and, as a result, in need of sleep?',
             ['Between 8pm and 9pm',
              'Between 9pm and 10.30pm',
              'Between 10.30pm and 12.30am',
              'Between 12.30am and 2am',
              'Between 2am and 3am',]),
    Question('At what time of day do you think that you reach your "feeling best" peak?',
             ['Between 5am and 8am',
              'Between 8am and 10am',
              'Between 10am and 5pm',
              'Between 5pm and 10pm',
              'Between 10pm and 5am',]),
    Question('Which one of these types do you consider yourself to be?',
             ['Definitely a "morning" type',
              'Rather more a "morning" than "evening" type',
              'Rather more an "evening" than a "morning" type',
              'Definitely an "evening" type',]),
            ]

def index(request):
    context = {'questions': questions,
               'sectors': Delegate.SECTOR_CHOICES,}
    return render(request, 'quiz/index.html', context)

def submit(request):
    try:
        answers = []
        for answer_num in range(1, len(questions) + 1):
            answers.append(int(request.POST['question{0}'.format(answer_num)]))
        delegate = Delegate(first_name = request.POST['firstname'],
                            last_name = request.POST['lastname'],
                            organisation = request.POST['organisation'],
                            sector = request.POST['sector'],
                            quiz_answers = answers,
                            quiz_result = int(round(sum(answers)/len(answers))),
                            created = timezone.now(),)
        delegate.save()
    except (KeyError):
        return render(request, 'quiz/index.html', {
            'error_message': "Not all questions were answered",
            'questions': questions,
        })
    else:
        return HttpResponseRedirect(reverse('quiz:results'))
    
def results(request):
    context = {}
    return render(request, 'quiz/results.html', context)

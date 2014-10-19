import logging

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from quiz.models import *
from quiz.controller import *


logger = logging.getLogger(__name__)

def index(request):
    context = {'questions': QUESTIONS,
               'sectors': Delegate.SECTOR_CHOICES,}
    return render(request, 'quiz/index.html', context)

def about(request):
    context = {}
    return render(request, 'quiz/about.html', context)

def submit(request):
    try:
        answers = []
        for answer_num in range(1, len(QUESTIONS) + 1):
            answers.append(int(request.POST['question{0}'.format(answer_num)]))
        delegate = Delegate(first_name = request.POST['firstname'],
                            last_name = request.POST['lastname'],
                            organisation = request.POST['organisation'],
                            sector = request.POST['sector'],
                            quiz_answers = answers,
                            quiz_result = calculate_quiz_result(answers),
                            created = timezone.now(),
                            printed = False)
        delegate.save()
    except (KeyError):
        return render(request, 'quiz/index.html', {
            'error_message': "Not all questions were answered",
            'questions': QUESTIONS,
        })
    process_print_queue()
    return render(request, 'quiz/about.html',
                  {'chronotype': chronotype[delegate.quiz_result],
                   'bird_image': image_highres[delegate.quiz_result],
                   'delegate': delegate,})

def printbadge(request):
    message = process_print_queue()
    return render(request, 'quiz/printbadge.html', 
                      {'message': message})
    
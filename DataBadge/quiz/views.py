from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from quiz.models import *
from quiz.controller import QUESTIONS, calculate_quiz_result, print_badge, chronotype, image


def index(request):
    context = {'questions': QUESTIONS,
               'sectors': Delegate.SECTOR_CHOICES,}
    return render(request, 'quiz/index.html', context)

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
                            created = timezone.now(),)
        delegate.save()
    except (KeyError):
        return render(request, 'quiz/index.html', {
            'error_message': "Not all questions were answered",
            'questions': QUESTIONS,
        })
    print_badge(delegate)
    return render(request, 'quiz/results.html',
                  {'chronotype': chronotype[delegate.quiz_result],
                   'bird_image': image[delegate.quiz_result],})
    #return HttpResponseRedirect(reverse('quiz:results'))

def results(request):
    context = {'chronotype': None,
               'bird_image': None,}
    return render(request, 'quiz/results.html', context)

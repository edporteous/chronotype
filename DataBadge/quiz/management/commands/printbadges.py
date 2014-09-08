'''
Created on 1 Sep 2014

@author: Ed
'''

from django.core.management.base import BaseCommand, CommandError
from quiz.models import *

class Command(BaseCommand):
    args = ''
    help = 'Prints all badges'
    
    def handle(self, *args, **options):
        print('handler called')
        self.stdout.write('Not yet implemented')